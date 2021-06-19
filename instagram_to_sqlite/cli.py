import click
import zipfile
import sqlite_utils
from instagram_to_sqlite import utils


@click.group()
@click.version_option()
def cli():
    "Convert data from Instagram Takeout to a SQLite database"


@cli.command(name="chats")
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "zip_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
def chats(db_path, zip_path):
    "Import all My Activity data from Takeout zip to SQLite"
    db = sqlite_utils.Database(db_path)
    zf = zipfile.ZipFile(zip_path)
    utils.save_my_chats(db, zf)
