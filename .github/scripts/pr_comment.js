/*
Have a single comment on a PR, identified by a comment marker.

Create a new comment if no comment already exists.
Update the content of the existing comment.


https://octokit.github.io/rest.js/v19
*/
module.exports = async ({github, context, process, retry_delay}) => {
    // Create the namespace to make it easy to copy/paste example from the
    // octokit docs.
    const octokit = {rest: github}

    const comment_marker = '\n' + process.env.COMMENT_MARKER

    if (context.eventName != "pull_request") {
        // Only PR are supported.
        return
    }

    var sleep = (second) => {
        return new Promise(resolve => setTimeout(resolve, second * 1000))
    }

    /*
    Create or update the PR summary report as a single comment.
    */
    var doSummaryComment = async (body) => {
        var comment_id = null
        const comment_body = body + comment_marker

        const comments = await octokit.rest.issues.listComments({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.payload.number,
          })

        comments.data.forEach(comment => {
            if (comment.body.endsWith(comment_marker)) {
                comment_id = comment.id
            }
        })

        if (comment_id) {
            // We have an existing comment.
            // update the content.
            await octokit.rest.issues.updateComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                comment_id: comment_id,
                body: comment_body,
            })
            return
        }

        // Create a new comment.
        await octokit.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.payload.number,
            body: comment_body,
        })

    }

    /*
    Create or refresh the diff inline comments.
    */
    var doDiffComments = async (report) => {

        // Start by deleting any previous comments.
        const existing_comments = await octokit.rest.pulls.listReviewComments({
            owner: context.repo.owner,
            repo: context.repo.repo,
            pull_number: context.payload.number,
        });
        existing_comments.data.forEach(async (comment) => {
            if (! comment.body.endsWith(comment_marker)) {
                // Not our comment.
                return
            }
            await octokit.rest.pulls.deleteReviewComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                comment_id: comment.id,
              })
        })

        // Prepare inline comments.
        var comments = []
        Object.keys(report.src_stats).forEach((path) => {
            report.src_stats[path].violation_lines.forEach((line) => {
                comments.push({
                    path,
                    line,
                })
            })
          })

        comments.forEach(async (comment) => {
            await octokit.rest.pulls.createReviewComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                commit_id: context.payload.after,
                pull_number: context.payload.number,
                body: 'Missing coverage.' + comment_marker,
                path: comment.path,
                line: comment.line,
              })
            // Wait 1 second to avoid the mitigate the limit.
            await sleep(1)
        })

    }

    /*
    Perform the actual logic.

    This is wrapped so that we can retry on errors.
    */
    var doAction = async () => {

        console.log(context)

        fs = require('fs');

        const body = fs.readFileSync(
            process.env.GITHUB_WORKSPACE + "/" + process.env.COMMENT_BODY, 'utf8')
        await doSummaryComment(body)

        const report_json = fs.readFileSync(
            process.env.GITHUB_WORKSPACE + "/" + process.env.REPORT_JSON, 'utf8');
        await doDiffComments(JSON.parse(report_json))

    }

    try {
        await doAction()
    } catch (e) {
        await sleep(retry_delay)
        await doAction()
    }
}
