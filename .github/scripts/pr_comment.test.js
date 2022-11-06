/*
This should be called via nodejs from the repo root folder.

node .github/scripts/pr_comment.test.js

This is just a poor man's testing code for the script.
Since the project is mostly python, is not easy to add nodeenv and a full
testing suite like jest.
*/
const process = require('process');

process.env.GITHUB_WORKSPACE = process.cwd()
process.env.COMMENT_BODY = '.github/scripts/pr_comment.test.body.txt'
process.env.REPORT_JSON = '.github/scripts/pr_comment.test.report.json'
process.env.COMMENT_MARKER = '<!--- comment-marker -->'

const script = require(process.cwd() + '/.github/scripts/pr_comment.js')
const retry_delay = 0.1

var github = {
    issues: {
        listComments: (options) => {
            console.log('Retrieving comments...')
            console.log(options)
            return {data: [
                {'id': 980, 'body': 'some-other-comment'},
                // Comment the line below to trigger creating a new comment.
                {'id': 456, 'body': 'comment marker\n<!--- comment-marker -->'},
                {'body': 'another-other-comment'},

            ]}
        },
        updateComment: (options) => {
            console.log('Updating existing comment...')
            console.log(options)
        },
        createComment: (options) => {
            console.log('Creating new comment...')
            console.log(options)
        },
    },
    pulls: {
        listReviews: (options) => {
            console.log('Listing existing reviews...')
            console.log(options)
            return {data: [
                {'id': 120, 'body': 'some-other-pr-review'},
                // Comment the line below to trigger creating a new comment.
                {'id': 156, 'body': 'review marker\n<!--- comment-marker -->'},
            ]}
        },
        listReviewComments: (options) => {
            console.log('Listing existing review comments...')
            console.log(options)
            return {data: [
                {'id': 120, 'body': 'some-other-pr-review'},
                // Comment the line below to trigger creating a new comment.
                {'id': 156, 'body': 'review marker\n<!--- comment-marker -->'},
            ]}
        },
        createReviewComment: (options) => {
            console.log('Creating new review comment...')
            console.log(options)
        },
        deleteReviewComment: (options) => {
            console.log('Deleting review comment...')
            console.log(options)
        },
        createReview: (options) => {
            console.log('Creating new review...')
            console.log(options)
        },
    },
}

var context = {
    eventName: 'pull_request',
    repo: {
        owner: 'dummy-org',
        repo: 'dummy-repo',
    },
    payload: {
        number: 123,
        after: '123abc567',
    }
}


script({github, context, process, retry_delay})
