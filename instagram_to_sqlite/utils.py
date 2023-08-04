import json
import os
from types import SimpleNamespace
from typing import Any

import click
from sqlite_utils.utils import hash_record


class Namespace(SimpleNamespace):
    def __init__(self, *args, **kwargs: Any) -> None:
        if args and isinstance(args[0], dict):
            kwargs.update(**args[0])

        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = Namespace(**v)

        super().__init__(**kwargs)


def _(text: Any) -> Any:
    if isinstance(text, str):
        try:
            # ref: https://stackoverflow.com/a/66443662/10309266
            return text.encode("latin-1").decode("utf-8")
        except UnicodeEncodeError:
            return text
    if isinstance(text, list):
        return [_(t) for t in text]
    if isinstance(text, dict):
        for k, v in text.items():
            text[k] = _(v)
    return text


CHAT = Namespace(
    {
        "meta": {
            "column_order": [
                "chat_room",
                "title",
                "thread_type",
                "thread_path",
                "is_still_participant",
            ]
        },
        "messages": {
            "column_order": [
                "id",
                "chat_room",
                "is_unsent",
                "type",
                "sender_name",
                "users",
                "content",
                "photos",
                "call_duration",
                "share",
                "timestamp_ms",
                "videos",
                "audio_files",
            ]
        },
        "reactions": {"column_order": ["id", "message_id", "reaction", "actor"]},
    }
)


def save_my_chats(db, zf):
    """Generates 3 tables for: meta, messages & reactions"""
    all_chats = [
        f.filename
        for f in zf.filelist
        if f.filename.startswith("messages") and f.filename.endswith(".json")
    ]
    tables_to_setup = filter(
        lambda x: x not in db.table_names(),
        ["chats_meta", "chats_messages", "chats_reactions"],
    )
    with click.progressbar(all_chats, label="Saving Chats") as all_chats:
        for filename in all_chats:
            reaction_rows = []
            path = os.path.splitext(filename)[0]

            try:
                chat_room = path.split(os.sep)[2]
            except Exception:
                # if the path doesnt fit the pattern, skip it - added while secret
                # groups came in. but i had no data to test it with
                continue

            chat_content = json.load(zf.open(filename))

            # 1. transform and insert meta data
            meta_row = _(
                {
                    "chat_room": chat_room,
                    "title": chat_content["title"],
                    "thread_type": chat_content.get("thread_type"),
                    "magic_words": chat_content.get("magic_words"),
                    "thread_path": chat_content["thread_path"],
                    "is_still_participant": chat_content["is_still_participant"],
                }
            )

            db["chats_meta"].upsert(
                meta_row,
                pk="chat_room",
                alter=True,
                column_order=CHAT.meta.column_order,
            )

            # 2. transform and insert messages data
            for x in chat_content["messages"]:
                x.update({"chat_room": chat_room})
            chat_rows = _(chat_content["messages"])

            reactioned_messages = list(filter(lambda x: x.get("reactions"), chat_rows))
            for rm in reactioned_messages:
                rm["id"] = hash_record(rm)
                reactions = rm.pop("reactions", [])
                for reaction in reactions:
                    reaction_rows.append({"message_id": rm["id"], **reaction})

            db["chats_messages"].upsert_all(
                reactioned_messages,
                pk="id",
                foreign_keys=[("chat_room", "chats_meta", "chat_room")],
                column_order=CHAT.messages.column_order,
                alter=True,
            )

            non_reactioned_messages = list(
                filter(lambda x: not x.get("reactions"), chat_rows)
            )
            for nrm in non_reactioned_messages:
                nrm["id"] = hash_record(nrm)

            db["chats_messages"].upsert_all(
                non_reactioned_messages,
                pk="id",
                foreign_keys=[("chat_room", "chats_meta", "chat_room")],
                column_order=CHAT.messages.column_order,
                alter=True,
            )

            # 3. insert messages' reactions data
            db["chats_reactions"].upsert_all(
                reaction_rows,
                hash_id="id",
                foreign_keys=[("message_id", "chats_messages", "id")],
                column_order=CHAT.reactions.column_order,
                alter=True,
            )

        generate_indexes(db, tables_to_setup)


def generate_indexes(db, tables_to_setup):
    if not tables_to_setup:
        return

    print("\nBuilding indexes", end="\x1b[1K\r")

    if "chats_meta" in tables_to_setup:
        db["chats_meta"].create_index(["chat_room"])

    if "chats_messages" in tables_to_setup:
        db["chats_messages"].create_index(["id", "chat_room", "sender_name"])
        db["chats_messages"].enable_fts(["share", "content"])

    if "chats_reactions" in tables_to_setup:
        db["chats_reactions"].create_index(["id", "message_id"])

    print("Indexes built")
