#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add User to database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, *args, **kwargs) -> User:
        """Returns first User row as per kwargs filters
        """
        user_query = self._session.query(User)
        for column, value in kwargs.items():
            user_query = user_query.filter_by(**{column: value})
        user_object = user_query.first()
        if user_object is None:
            raise NoResultFound
        return user_object

    def update_user(self, user_id: int, *args, **kwargs) -> None:
        """Updates a User based on kwargs
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return None
        for column, value in kwargs.items():
            if column not in User.__table__.columns.keys():
                raise ValueError
            setattr(user, column, value)
        self._session.commit()
        return None
