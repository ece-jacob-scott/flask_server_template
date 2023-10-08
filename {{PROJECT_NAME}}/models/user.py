import sqlalchemy as sa

from .. import db


users_table = db.Table(
    "users",
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("email", sa.String(255), nullable=False),
    sa.Column("clerk_id", sa.String(255), nullable=False),
)
