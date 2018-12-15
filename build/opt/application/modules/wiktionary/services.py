# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, BigInteger, BLOB, Float, Binary, VARBINARY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()


class Page(Base):
    __tablename__ = 'page'
    page_id = Column(Integer, primary_key=True, autoincrement=True)
    page_namespace = Column(BigInteger)
    page_title = Column(String(255))
    page_restrictions = Column(BLOB)
    page_is_redirect = Column(Integer)
    page_is_new = Column(Integer)
    page_random = Column(Float)
    page_touched = Column(Binary(14))
    page_links_updated = Column(VARBINARY(14))
    page_links_updated = Column(VARBINARY(14))
    page_latest = Column(Integer)
    page_len = Column(Integer)
    page_content_model = Column(VARBINARY(32))
    page_lang = Column(VARBINARY(35))
    page_counter = Column(Integer)
    revision = relationship("Revision", uselist=False, back_populates="page", lazy='joined')


class Text(Base):
    __tablename__ = 'text'
    old_id = Column(Integer, primary_key=True, autoincrement=True)
    old_text = Column(BLOB)
    old_flags = Column(BLOB)
    revision = relationship("Revision", uselist=False, back_populates="text")


class Revision(Base):
    __tablename__ = 'revision'
    rev_id = Column(Integer, primary_key=True, autoincrement=True)
    rev_page = Column(Integer, ForeignKey('page.page_id'))
    rev_text_id = Column(Integer, ForeignKey('text.old_id'))
    rev_comment = Column(Binary(767))
    rev_user = Column(Integer)
    rev_user_text = Column(String(255))
    rev_timestamp = Column(Binary(14))
    rev_minor_edit = Column(Integer)
    rev_deleted = Column(Integer)
    rev_len = Column(Integer)
    rev_parent_id = Column(Integer)
    rev_sha1 = Column(Binary(32))
    rev_content_model = Column(Binary(32))
    rev_content_format = Column(Binary(64))
    text = relationship("Text", back_populates="revision", lazy='joined')
    page = relationship("Page", back_populates="revision")


class Wiktionary(object):
    _engine = None

    def __init__(self, host, port, name, user, password):
        """

        :param host: 
        :param port: 
        :param name: 
        :param user: 
        :param password: 
        """
        self._engine = create_engine('mysql://%s:%s@%s:%s/%s' % (
            user, password, host, port, name,
        ), convert_unicode=False)

        session = self.session_create(self._engine)
        Base.query = session.query_property()
        Base.metadata.create_all(bind=self._engine)
        session.commit()

    def session_create(self, engine):
        """
        Create session instance 

        :param engine: 
        :return: 
        """
        return scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        ))

    def find(self, string):
        """
        
        :param string: 
        :return: 
        """

        return self.session_create(self._engine) \
            .query(Page) \
            .filter(Page.page_title == string) \
            .one()

    def all(self):
        """
        
        :return: 
        """
        return self.session_create(self._engine)\
            .query(Page) \
            .filter() \
            .all()
