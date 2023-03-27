import os
from typing import Optional

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_trace_database_uri() -> Optional[str]:
    username = os.getenv("TRACE_DB_USER")
    password = os.getenv("TRACE_DB_PASSWORD")
    host = os.getenv("TRACE_DB_HOST")
    db_name = "trace_db"

    if all(field is not None for field in [username, password, host]):
        return f"postgresql://{username}:{password}@{host}/{db_name}"

    return None


def get_inspect_database_uri():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    db_name = "mev_inspect"
    # print("TEST123: ", username, password, host, db_name)
    return f"postgresql://{username}:{password}@{host}/{db_name}"


def _get_engine(uri: str):
    return create_engine(uri)


def _get_session(uri: str):
    Session = sessionmaker(bind=_get_engine(uri))
    return Session()


def get_inspect_session() -> orm.Session:
    uri = get_inspect_database_uri()
    # print("uri for DB: ", uri)
    cred = credentials.Certificate(
        'mev-inspec-firebase-adminsdk-ooyw5-afc76e7b2b.json')
    app = firebase_admin.initialize_app(cred)
    global db
    db = firestore.client()
    return _get_session(uri)


def get_db():
    return db


def get_trace_session() -> Optional[orm.Session]:
    uri = get_trace_database_uri()

    if uri is not None:
        return _get_session(uri)

    return None
