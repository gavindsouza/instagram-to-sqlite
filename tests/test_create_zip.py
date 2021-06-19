from .utils import create_zip


def test_create_zip():
    zf = create_zip()
    assert {"messages/inbox/gavin_osatf9tyla/message_1.json"} == {
        f.filename for f in zf.filelist
    }
