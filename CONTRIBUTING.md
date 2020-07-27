# Contributing to reprohack_site

This outlines how to propose a change to reprohack_site. 

### Fixing typos

Small typos or grammatical errors in documentation may be edited directly using
the GitHub web interface, so long as the changes are made in the _source_ file.

### Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it’s a problem. If you’ve found a
bug, create an associated issue and illustrate the bug with a minimal 
demo.

### Pull request process


####  [Fork](https://the-turing-way.netlify.app/reproducible-research/vcs/vcs-github.html#a-workflow-to-contribute-to-others-github-projects-via-git) the repository to your profile


Make sure to [keep your fork up to date](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork) with the master repository, otherwise you can end up with lots of dreaded [merge conflicts](https://the-turing-way.netlify.app/reproducible-research/vcs/vcs-git-merge.html#merge-conflicts).

#### Make the changes you've discussed

Please make a [new branch][github-branches] for any changes. [This blog](https://nvie.com/posts/a-successful-git-branching-model/) details the different Git branching models.

Try to keep the changes focused.
If you submit a large amount of work all in one go it will be much more work for whomever is reviewing your pull request.

While making your changes, commit often and write good, detailed commit messages.
[This blog](https://chris.beams.io/posts/git-commit/) explains how to write a good Git commit message and why it matters.
It is also perfectly fine to have a lot of commits - including ones that break code.
A good rule of thumb is to push up to GitHub when you _do_ have passing tests then the continuous integration (CI) has a good chance of passing everything. 😸



Please do not re-write history!
That is, please do not use the [rebase](https://help.github.com/en/articles/about-git-rebase) command to edit previous commit messages, combine multiple commits into one, or delete or revert commits that are no longer necessary.

Are you new to Git and GitHub or just want a detailed guide on getting started with version control? Check out the [Version Control chapter](https://the-turing-way.netlify.com/version_control/version_control.html) in the Turing Way Book!

#### Submit a pull request

We encourage you to open a pull request as early in your contributing process as possible.
This allows everyone to see what is currently being worked on.
It also provides you, the contributor, feedback in real time from both the community and the continuous integration as you make commits (which will help prevent stuff from breaking).

When you are ready to submit a pull request, you will automatically see the [Pull Request Template](https://github.com/reprohack/reprohack_site/blob/master/.github/PULL_REQUEST_TEMPLATE.md) contents in the pull request body.
It asks you to:

- Describe the problem you're trying to fix in the pull request, reference any related issue and use fixes/close to automatically close them, if pertinent.
- List of changes proposed in the pull request.
- Describe what the reviewer should concentrate their feedback on.

By filling out the "_Lorem ipsum_" sections of the pull request template with as much detail as possible, you will make it really easy for someone to review your contribution!

If you have opened the pull request early and know that its contents are not ready for review or to be merged, add "[WIP]" at the start of the pull request title, which stands for "Work in Progress".
When you are happy with it and are happy for it to be merged into the main repository, change the "[WIP]" in the title of the pull request to "[Ready for review]".

A member of the ReproHack  team will then review your changes to confirm that they can be merged into the main repository.
A [review][github-review] will probably consist of a few questions to help clarify the work you've done.
Keep an eye on your GitHub notifications and be prepared to join in that conversation.

You can update your fork of the ReproHack site repository and the pull request will automatically update with those changes.
You don't need to submit a new pull request when you make a change in response to a review.


### Code of Conduct

Please note that the reprohack_site project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this
project you agree to abide by its terms.


