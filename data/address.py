import sqlalchemy

from .db_session import SqlAlchemyBase


class Address(SqlAlchemyBase):
    __tablename__ = 'address'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coordinate_x = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    coordinate_y = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
