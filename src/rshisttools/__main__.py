import click


@click.group
def main() -> None:
    """Keeps the reposity up-to-date with my account and goals."""


@main.command
@click.pass_context
def update_public(ctx) -> None:
    """Update all files so they are ready for the public to read.

    This should be called before/on pushing to GitHub, so that the
    online public reposity is up-to-date.

    To-Do list:
    - Update README.md
    - Update current minimum-skill-front
    - Update end of year minimum-skill-fronts
    """
    ctx.invoke(update_readme)
    ctx.invoke(update_current_skill_front)
    ctx.invoke(end_of_year_skill_front)


@main.command
def update_readme() -> None:
    """Update the README.md file so it reflects current state of the account."""
    click.echo("Update ~/README.md")
    ...


@main.command
def update_current_skill_front() -> None:
    """Update the current skill front in the 'minimum-skill-front.md' file in repository root."""
    click.echo("Update ~/minimum-skill-front.md")
    ...


@main.command
def end_of_year_skill_front() -> None:
    """Make end-of-year skill-front for every completed year in the repository.

    Each front is described in a markdown file with with a name generated from
    the 'filename_template' argument and and is saved in its respective completed year folder.
    """
    click.echo("Update minimum skill front for all completed years:")
    click.echo("--------------------------------------------------")
    for year in range(2001, 2027):
        click.echo(f"- Update end-of-year skill front of year {year}.")
        ...


if __name__ == '__main__':
    main()
