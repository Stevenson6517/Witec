# Guidelines

Thank you for wanting to help.

We imagine you are reading this because you fall into one of two categories of
people:

1. You work in this lab and are tasked with extending this project.
2. You found this project online in hopes that it meets your needs. You then
   fixed something for yourself and want to let us know about it.

This is to remind contributors in the first camp to take care in crafting
changes that can be used by people in the second camp, but also to remind users
in the second camp that this project is developed with specific needs in mind.

If you find a bug, [open an issue][github-issues]. If you have a suggestion
about a new feature, draft it as a discussion in a [pull
request][github-pull-requests]. Keeping these discussions online helps log
progress and allows future users to benefit from the gained insight.

[github-issues]: https://docs.github.com/en/issues/tracking-your-work-with-issues/quickstart
[github-pull-requests]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

## Code

To make it easier for changes to be inspected, we ask that contributors adhere
to [PEP-8][pep8] standards. Submitting code that has already been
PEP-8-sanitized at commit time means there will be fewer changes that deal with
formatting, thereby making differences between versions easier to manage.

In cases where PEP-8 is ill-defined, the following rules supersede convention:

- Avoid lines longer than 80-ish characters.
- Prefer double quotes for all strings.

We consider a fixed line length sometimes obtrusive in cases where it makes sense
to extend it a few characters beyond the recommended 79 characters. Use
judgement when necessary.

The easiest way to conform to these standards is to use a code formatter. We
recommend [Black][black], which will re-write your file to be PEP-8 complaint,
but with a modified 88-character line limit and with all quotes converted to
double quotes. If you follow the guidelines in [Enforcing standards with
hooks](hooks.md), you will have Black enabled on commit.

[black]: https://black.readthedocs.io/en/stable/
[pep8]: https://pep8.org


## Commits

Aim for commits that are small and atomic; that is, group changes into the least
divisible unit that are congruent in scope.

Keep the following guidelines in mind when you develop and document changes:

1. Commit related changes
2. Commit often
3. Don't commit half-done work
4. Write good commit messages

Help make commit messages useful to your future self and to others. There are
many useful guidelines on how to write a good commit message[^1][^2][^3]. The
most important point is that you have a useful body in the commit message, which
means you should **never** craft your message the following way:

```bash
git commit -m "A title message only"
```

If you follow the guidelines in [Enforcing standards with hooks](hooks.md), sane
commit messages will be enforced automatically.

[^1]: https://github.blog/2022-06-30-write-better-commits-build-better-projects/
[^2]: https://cbea.ms/git-commit/
[^3]: https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/
