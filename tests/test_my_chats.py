from instagram_to_sqlite.utils import save_my_chats
from sqlite_utils import Database

from .utils import create_zip


def test_my_chats():
    zf = create_zip()
    db = Database(memory=True)
    save_my_chats(db, zf)

    assert {
        "chats_meta", "chats_messages", "chats_reactions"
    } == set(db.table_names())
