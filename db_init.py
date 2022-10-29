from datetime import datetime
from enum import IntEnum

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from db_models import Algorithms, Users, Base
import sqlalchemy as sq
from sqlalchemy import create_engine, insert
from sqlalchemy_utils import database_exists, create_database
import logging
import yaml
import bcrypt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


with open("configs/config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


class Database:
    """A class for interactions with database."""
    session: Session
    current_user: str
    engine: Engine

    def __init__(self):
        self.current_user = ''
        self.engine = self.create_engine()
        self.session = Session(bind=self.engine)

    @staticmethod
    def create_engine() -> Engine:
        """Creating Engine object for working with database.
        :rtype: Engine.
        """
        connection = cfg['postgres']['connection']
        engine = create_engine(connection)
        if not database_exists(engine.url):
            create_database(engine.url)
        if not sq.inspect(engine).has_table("Algorithm"):
            Base.metadata.create_all(engine)

        return engine

    def insert_data_to_db(self, data: list) -> None:
        """Inserting data to database.
        :param: list data: Parsed data for database.
        :rtype: None.
        """
        table_filled = self.session.query(Algorithms).first()

        if table_filled:
            self.session.query(Algorithms).delete()
            self.session.commit()

        for d in data:
            ins_data = insert(Algorithms).values(operation=d['operation'],
                                                 complexity=d['complexity'],
                                                 example=d['example'],
                                                 type=Types[d['type']])
            self.engine.execute(ins_data)

        logging.info(f"Data updated: {datetime.utcnow()}")

    def is_user_exist(self, user_login: str) -> bool:
        """Check if user login exists in database
        :param str user_login: User login.
        :rtype: bool.
        """
        is_exist = self.session.query(Users).filter_by(
            login=user_login).first() is not None

        return is_exist

    def check_password(self, user_login: str,
                       user_password: str) -> bool or None:
        """Encode user password and check if it matches with password
           in database
        :param str user_login: User login
        :param str user_password: User password
        :rtype: bool or None.
        """
        user = self.session.query(Users).filter_by(
            login=user_login).first()
        if bcrypt.checkpw(user_password.encode('utf8'),
                              user.password.encode('utf8')):
            self.current_user = user_login
            return True
        else:
            logging.info(f"Wrong password authorization: {datetime.utcnow()}")

    def insert_user_to_db(self, user_login: str, user_password: str,
                          user_created_at: datetime) -> None:
        """Create new user in database
        :param str user_login: User login
        :param str user_password: User password
        :param datetime user_created_at: Time of first user authoriztion
        :rtype: None.
        """
        pw_hash = bcrypt.hashpw(user_password.encode('utf8'), bcrypt.gensalt())
        pw_hash_decoded = pw_hash.decode('utf8')
        ins_user = insert(Users).values(login=user_login,
                                        password=pw_hash_decoded,
                                        created_at=user_created_at)
        self.engine.execute(ins_user)
        logging.info(f"Added new user: {datetime.utcnow()}")
        self.current_user = user_login

    def update_user_request_time(self, request_time: datetime) -> None:
        """
        Update user request time in database
        :param datetime request_time: Last user request for data
        :rtype: None.
        """
        self.session.query(Users).filter(
            Users.login == self.current_user).update(
            {"last_request": request_time})

        self.session.commit()
        logging.info(f"Request time updated: {datetime.utcnow()} "
                     f"for {self.current_user}")

    def get_table_data(self) -> dict:
        """
        Returns whole data from table.
        :rtype: dict.
        """
        session = Session(bind=self.engine)
        table_data = session.query(Algorithms).all()
        row_dicts = []
        for t_d in table_data:
            row_dict = {"id": t_d.id,
                        "operation": t_d.operation,
                        "example": t_d.example,
                        "type": cfg['data_types'][t_d.type - 1]}
            row_dicts.append(row_dict)
        data = {"data": row_dicts, "total": len(row_dicts)}
        logging.info(f"Table data requested: {datetime.utcnow()}")
        return data


class Types(IntEnum):
    """IntEnum class for data types"""
    list = 1
    set = 2
    dict = 3


if __name__ == '__main__':
    tp = Database()
    logging.info(f"Databases are created: {datetime.utcnow()}")


