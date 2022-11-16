## Contributing to Tasties project

---

Hello and welcome to Tasties project. 
Please read these guidelines carefully. Following them will help us make
the contribution process easy and effective for everyone involved.



### Quicklinks

---

- [Pre-Requirements](#pre-requirements)
- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Testing](#testing)


### Pre Requirements

---

To contribute to our project please download and install the following:

- git, recommended version: 2.38.1;
   git can be downloaded from: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- Vagrant, recommended version: 2.3.2;
   Vagrant can be downloaded from: https://developer.hashicorp.com/vagrant/downloads
- VirtualBox(or other VM that works with "Vagrant"), recommended version: 6.1.38;
   VirtualBox can be downloaded from: https://www.virtualbox.org/wiki/Downloads

IMPORTANT NOTES:

- Not all versions of Vagrant and VirtualBox may work together as expected (especially the latest versions).
Finding a different combination of versions for Vagrant and VirtualBox may solve some issues that may arise in loading up
a Vagrant VM.
- Also note that Vagrant may not work on some machines (such as Apple M1-based machines), so please make sure that
you can find a suitable solution.

### Issues

---

Issues should be used to report problems in the main branch, request a new feature, or to propose potential changes.

Guidelines to creating a new issue:

1. Before you create a new issue, please make sure that there is no existing issue which addresses the same purpose.
2. Every issue should have a meaningful and concise title that clearly describes its purpose (do not include issue or line numbers).
3. Every issue should have a meaningful and concise description that provides relevant information on the issue.


### Pull Requests

---

To create a pull request (PR) please follow these instructions:

1. Create an [issue](#Issues), if an issue relevant to your PR wasn't created yet.
2. If you have not already done so, create a fork of the main repository https://github.com/redhat-beyond/tasties in the GitHub account you intend to contribute from.
3. If you already have your own fork, please make sure it is synced with the redhat-beyond/tasties repository.
4. Clone or Pull your up-to-date fork to the main branch on your local repository.
5. Make sure you have set up https://github.com/redhat-beyond/tasties.git in your working directory as the "upsream" remote, and your 
   fork of it as the "origin" remote.
6. Create a new branch from the up-to-date main branch in your local repository for your changes.
7. Make your desired changes in your local repository.
8. Commit your changes with a concise and accurate commit message.
9. Make sure you have commited all your desired changes, and push your branch to "origin".
10. Open a new PR for your changes (it's recommended that you follow the link git provides on pushing).
11. Link your PR to a relevant issue. This can be done as [follows](#https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/using-keywords-in-issues-and-pull-requests).
    Issues can also help the team and mentors know what every member of the team is working on.

### Pull Requests Standards

---
Our standards for pull requests (PRs) are:

PR mergeability:

1. Only submit Python code that was created on a Vagrant VM through pipenv (make sure to update pipfiles if you introduced new dependencies, and commit your changes).
   This ensures proper version control.
2. Test your created code locally (with flake8 running through pipenv on a Vagrant VM); Please submit code that passes CI tests locally,
   to avoid as much as possible a PR that fails CI tests.
3. Make every effort to only sumbit PRs that do not break currently working programs and features or introduce bugs.
4. Make every effort so that the commits in your PR will not cause conflicts with the branch that you want you PR to be merged with.

PR documentation and visibility:

1. Every PR should have a meaningful and concise title that clearly describes its purpose (do not include issue or line numbers).
2. Every PR should have a meaningful and concise description that provides relevant information on the PR.
3. Every PR should be linked to an issue (or issues), to make its purpose clear and increase its visibility (see [Issues](#issues)).
4. Assign other teammates as well as mentors as reviewers on your PR.

PR code review:

1. Each PR requires the approval of at least two team members. 
2. Examine the PR carefully, and with respect to what it is supposed to achieve.
3. If you want to request changes to specific lines in a file please use the "Start a review" button.
4. If you want to request changes, mark your review as "Request changes" - please do not use a generic comment.
5. Use polite, respectful and clear language when commenting on or reviewing a PR.
6. If your PR recieved a request for changes or a comment, please notify the reviewer about your actions
   (what changes you made, or if you don't think they're necessary - why you think so).


### Testing

---

Every PR will be tested by:
1. A flake8 workflow to make sure the PR conforms to proper Python syntax and coding standards.
2. Automatically checked by a CI system.


### Maintainers 

---

The maintainers are: 
Lior Noy, Nati Fridman, Shay Vatarescu and Kasem Alem.
