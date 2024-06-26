#!/usr/bin/env python3
"""
DB module for handling database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    Database class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    
    @property
    def _session(self) -> Session:
        """
        Memorized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()

        return self.__session


    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self.__session.add(new_user)
        self.__session.commit()

        return new_user


    def find_user_by(self, **kwargs) -> User:
        """
        Find and return the first user matching the keyword arg
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise InvalidRequestError


    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user attr based on the provided kwargs
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.commit()
        