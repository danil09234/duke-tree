import click


@click.group()
def cli():
    pass


@cli.group()
def save_study_programmes():
    pass


@save_study_programmes.command()
@click.argument("url")
def by_field_of_study(url):
    ...


@save_study_programmes.command()
@click.argument("url")
def by_faculty(url):
    ...


if __name__ == "__main__":
    cli()
