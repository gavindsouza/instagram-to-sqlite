from .utils import create_zip


def test_create_zip():
    zf = create_zip()
    assert {
        "your_instagram_activity/messages/inbox/gavin_554997539236567/message_1.json"
    } == {f.filename for f in zf.filelist}
