from peewee import *
from flask_login import UserMixin
from datetime import datetime
import bcrypt

DATABASE = SqliteDatabase('chat.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class User(UserMixin, Model):
  username = CharField(unique = True)
  password = CharField(max_length = 100)
  joined_at = DateTimeField(default = datetime.now)
  is_admin = BooleanField(default = False)

  class meta:
    database = DATABASE
    order_by = ('-joined_at')


  @classmethod
  def create_user(cls, username, password, admin=False):
    initialize()
    try:
      cls.create(
        username = username,
        password = bcrypt.hashpw(password),
        is_admin = admin
        )
    except IntegrityError:
      raise ValueError("User with the same email exists!")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(User, safe=True)
    DATABASE.close()

