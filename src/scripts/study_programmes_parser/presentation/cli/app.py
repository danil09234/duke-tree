import click


@click.group()
def cli():
    pass


@cli.command()
def save_study_programmes():
    pass


if __name__ == "__main__":
    cli()
