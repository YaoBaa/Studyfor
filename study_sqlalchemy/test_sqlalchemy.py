#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/10/1 23:12 
# @Author : liyaoyao
# @Email : yao72396@sina.com
# @File : test_sqlalchemy.py 
# @Software: PyCharm

# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased

# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接:
# echo打印结果
engine = create_engine("mysql+mysqlconnector://root:H3c@12500@192.168.243.3:3306/test_btc", encoding="utf-8",
                       echo=False,max_overflow=5)


# 定义User对象
class User(Base):
    # 表的名字
    __tablename__ = "user"

    # 表的结构
    id = Column(Integer, primary_key=True)  # 主键
    user_name = Column(String(32))
    user_password = Column(String(64))

    def __repr__(self):
        return "<User(id='%s', user_name='%s', user_password='%s')>" % (self.id, self.user_name, self.user_password)

# 再定义一个类
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))

    def __repr__(self):
        return "<Admin(id='%s', username='%s', password='%s')>" % (self.id, self.username, self.password)


# Base.metadata.create_all(engine)  # 创建表结构

# # 创建DBSession类型
# DBSession = sessionmaker(bind=engine)
# 如果还没有定义Engine模块级对象
DBSession = sessionmaker()
# 然后可以用coonfigure连接
DBSession.configure(bind=engine)
# 创建seesion对象：
session = DBSession()
# 创建新User对象：
new_user = User(id=0, user_name="lyy-0", user_password="H3c12500")
new_user_list = [
    User(id=2, user_name="lyy-1", user_password="H3c12500"),
    User(id=3, user_name="lyy-2", user_password="H3c12500"),
    User(id=4, user_name="lyy-3", user_password="H3c12500"),
]
new_user.id = 1
# # 添加到seesion：
# session.add(new_user)
# session.add_all(new_user_list)

# # 回滚，需要在add之后，
# session.rollback()
# print(session.query(User).all())

# 提交即保存到数据库：
session.commit()
# 关闭session
session.close()

# 查询
# A Query 对象是使用 query() 方法对 Session .
# 此函数接受可变数量的参数，这些参数可以是类和类插入描述符的任意组合。
# 下面，我们指出 Query 哪些负载 User 实例。当在迭代上下文中进行评估时， User 返回存在的对象
for instance in session.query(User).order_by(User.id):
    print(instance.id, instance.user_name, instance.user_password)
# 这个 Query 还接受ORM插入描述符作为参数。当多个类实体或基于列的实体表示为 query() 函数，返回结果表示为元组：
for name, password in session.query(User.user_name, User.user_password):
    print(name, password)
#返回的元组 Query 是 已命名 元组，由 KeyedTuple 类，并且可以像普通的Python对象一样进行处理。这些名称与属性的名称和类的类名相同：
for row in session.query(User, User.id).all():
    print(row.User, row.id, row.User.user_name)  # 只能是id
# 可以使用 label() 构造，可从任何 ColumnElement -派生对象以及映射到一个对象的任何类属性（例如 User.name ）：
for row in session.query(User.user_name.label('name_label')).all():
    print(row.name_label)
# 给予完整实体的名称，如 User ，假设调用中存在多个实体 query() ，可以使用 aliased() ：
user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.user_name).all():
    print(row.user_alias)
# 基本操作 Query 包括发布限制和偏移，最方便地使用python数组切片，通常与order by结合使用：
for u in session.query(User).order_by(User.id)[1:3]:
    print(u.user_name)
# 以及过滤结果 filter_by() ，使用关键字参数：
for name, in session.query(User.user_name).filter_by(id=2):
    print(name)
# 或… filter() ，它使用更灵活的SQL表达式语言构造。这些允许您在映射类上使用具有类级属性的常规python运算符：
for name, in session.query(User.user_name).filter(User.id==3):
    print(name)
# 这个 Query 对象完全 生成的 ，这意味着大多数方法调用都返回一个新的 Query 对象，在此对象上可以添加其他条件。例如，要查询名为“ed”且全名为“ed jones”的用户，可以调用 filter() 两次，使用 AND ：
for user in session.query(User).filter(User.user_name=='lyy-3').filter(User.id==4):
    print(user)
