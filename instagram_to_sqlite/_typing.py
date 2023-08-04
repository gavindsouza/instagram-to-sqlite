from typing import TypedDict, Any, Iterable  # noqa


class InstagramChatReaction(TypedDict):
    reaction: str
    actor: str


class InstagramMessage(TypedDict):
    sender_name: str
    timestamp_ms: int
    content: str
    reactions: list[InstagramChatReaction]
    share: dict[str, str] | None


class InstagramParticipant(TypedDict):
    name: str


class InstagramChat(TypedDict):
    title: str
    thread_type: str | None
    magic_words: str | None
    thread_path: str
    is_still_participant: bool
    participants: list[InstagramParticipant]
    messages: list[InstagramMessage]
