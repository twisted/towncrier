# Description

Fixes #<!-- add the associated GitHub Issue ID>

<!-- add a short summary if necessary; mention issue numbers -->


# Checklist
<!-- add a "X" inside the brackets to confirm -->
* [ ] Make sure changes are covered by existing or new tests.
* [ ] For at least one Python version, make sure test pass on your local environment.
* [ ] Create a file in `src/towncrier/newsfragments/`. Briefly describe your
  changes, with information useful to end users. Your change will be included in the public release notes.
* [ ] Make sure all GitHub Actions checks are green (they are automatically checking all of the above).
* [ ] Ensure `docs/tutorial.rst` is still up-to-date.
* [ ] If you add new **CLI arguments** (or change the meaning of existing ones), make sure `docs/cli.rst` reflects those changes.
* [ ] If you add new **configuration options** (or change the meaning of existing ones), make sure `docs/configuration.rst` reflects those changes.
* [ ] I have not directly included the output of any generative AI system in this pull request, as per our [policy on generative AI](https://docs.twisted.org/en/latest/development/ai-policy.html).
  Our bot will trigger the review process, by applying the pending review label
  and requesting a review from the Twisted dev team.
