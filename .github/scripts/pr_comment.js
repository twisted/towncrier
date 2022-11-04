/*
Have a single comment on a PR, identified by a comment marker.

Create a new comment if no comment already exists.
Update the content of the existing comment.


https://octokit.github.io/rest.js/v19
*/
module.exports = async ({octokit_rest, context, process}) => {
    if (context.eventName != "pull_request") {
        // Only PR are supported.
        return
    }

    var sleep = function(second) {
        return new Promise(resolve => setTimeout(resolve, second * 1000))
    }

    /*
    Perform the actual logic.

    This is wrapped so that we can retry on errors.
    */
    var doAction = async function() {

        await octokit_rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.event.number,
            body: process.env.COMMENT_BODY,
          });

    }

    try {
        await doAction()
    } catch (e) {
        await sleep(5)
        await doAction()
    }
}
