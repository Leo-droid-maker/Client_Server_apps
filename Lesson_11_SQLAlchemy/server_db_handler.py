from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from common.config import SERVER_DATABASE

current_time = datetime.datetime.now()


class ServerDatabase:
    Base = declarative_base()

    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        last_login_time = Column(DateTime)

        def __init__(self, username, last_login_time):
            self.username = username
            self.last_login_time = last_login_time

        # def __repr__(self):
        #     return f'<User({self.username}, {self.last_login})>'

    class UsersHistory(Base):
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'))
        login_time = Column(DateTime)
        ip_address = Column(String)
        port = Column(Integer)

        def __init__(self, user, login_time, ip_address, port):
            self.user = user
            self.login_time = login_time
            self.ip_address = ip_address
            self.port = port

        # def __repr__(self):
        #     return f'<UserHistory({self.user}, {self.login_time}, {self.ip_address}, {self.port})>'

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'), unique=True)
        ip_address = Column(String)
        port = Column(Integer)
        login_time = Column(DateTime)

        def __init__(self, user, ip_address, port, login_time):
            self.user = user
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

        # def __repr__(self):
        #     return f'<UserHistory({self.user}, {self.login_time}, {self.ip_address}, {self.port})>'

    def __init__(self):
        self.engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        self.Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        check_user = self.session.query(self.Users).filter_by(username=username)
        if check_user.count():
            user = check_user.first()
            user.last_login_time = current_time
        else:
            user = self.Users(username, current_time)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, current_time)
        self.session.add(new_active_user)

        history = self.UsersHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        self.session.commit()

    def user_logout(self, username):

        user = self.session.query(self.Users).filter_by(username=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def users_list(self):
        # return [user[0] for user in self.session.query(self.Users.username).all()]

        query = self.session.query(
            self.Users.username,
            self.Users.last_login_time,
        )

        return query.all()

    def active_users_list(self):

        query = self.session.query(
            self.Users.username,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.Users)

        return query.all()

        # return [user[0] for user in self.session.query(
        #     self.Users.username,
        #     self.ActiveUsers.ip_address,
        #     self.ActiveUsers.port,
        #     self.ActiveUsers.login_time
        # ).join(self.Users).all()]

    def login_history(self, username=None):

        query = self.session.query(
            self.Users.username,
            self.UsersHistory.login_time,
            self.UsersHistory.ip_address,
            self.UsersHistory.port
        ).join(self.Users)
        if username:
            query = query.filter(self.Users.username == username)
        return query.all()

        # return [user[0] for user in self.session.query(self.Users.username,
        #                            self.UsersHistory.login_time,
        #                            self.UsersHistory.ip_address,
        #                            self.UsersHistory.port
        #                            ).join(self.Users).all()]


if __name__ == '__main__':
    db = ServerDatabase()
    db.user_login('Leo', '192.168.1.4', 8888)
    db.user_login('Den', '192.168.1.5', 7777)

    print(db.active_users_list())

    db.user_logout('Leo')
    print(db.users_list())

    print(db.active_users_list())
    db.user_logout('Den')
    print(db.users_list())
    print(db.active_users_list())

    print(db.login_history('Leo'))

    print(db.users_list())
