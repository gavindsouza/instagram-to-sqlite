from setuptools import setup
import os

VERSION = "0.0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="instagram-to-sqlite",
    description="Convert data from Instagram Takeout to a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Gavin D'souza",
    url="https://github.com/gavindsouza/instagram-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["instagram_to_sqlite"],
    entry_points="""
        [console_scripts]
        instagram-to-sqlite=instagram_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils>=3.30"],
    extras_require={"test": ["pytest"]},
    tests_require=["instagram-to-sqlite[test]"],
)
