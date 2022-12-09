from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "mysql://sample_user:Password#1@localhost/pandash_sample?charset=utf8", echo=False
)

session = orm.scoped_session(
    orm.sessionmaker(bind=engine, autoflush=True, autocommit=False)
)

USERNAME = ""  # PandAにログインするときのid
PASSWORD = ""  # PandAにログインするときのパスワード

Base = declarative_base()
