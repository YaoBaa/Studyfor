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
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接:
# echo，是否打印结果
engine = create_engine("mysql+mysqlconnector://root:H3c@12500@192.168.243.3:3306/test_btc", encoding="utf-8",
                       echo=True, max_overflow=5)

print("\n\n     Step1:初始化表格，创建表格¶")
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


Base.metadata.create_all(engine)  # 创建表结构、


print("\n\n     Step2:添加表格数据¶")
# # 创建DBSession类型
# DBSession = sessionmaker(bind=engine)
# 如果还没有定义Engine模块级对象
DBSession = sessionmaker()
# 然后可以用coonfigure连接
DBSession.configure(bind=engine)
# 创建seesion对象：
session = DBSession()
# 创建新User对象：
new_user = User(id=0, user_name="lyy-1a", user_password="H3c12500aaabc")
new_user_list = [
    User(id=2, user_name="lyy-2b", user_password="H3c12500bbbcd"),
    User(id=3, user_name="lyy-3c", user_password="H3c12500cccde"),
    User(id=4, user_name="lyy-4d", user_password="H3c12500dddef"),
    User(id=5, user_name="lyy-2b", user_password="H3c12500bbbcd"),
    User(id=6, user_name="lyy-3c", user_password="H3c12500cccde"),
    User(id=7, user_name="lyy-4d", user_password="H3c12500dddef"),
]
new_user.id = 1

# # 添加到seesion：
# session.add(new_user)
# session.add_all(new_user_list)

# # 回滚，需要在add之后，
# session.rollback()
# print(session.query(User).all())

# # 提交即保存到数据库：
# session.commit()
# # 关闭session
# session.close()


print("\n\n     Step3:表格数据常规查询¶")
# 查询
# A Query 对象是使用 query() 方法对 Session .
# 此函数接受可变数量的参数，这些参数可以是类和类插入描述符的任意组合。
# 下面，我们指出 Query 哪些负载 User 实例。当在迭代上下文中进行评估时， User 返回存在的对象
for instance in session.query(User).order_by(User.id):
    print(instance.id, instance.user_name, instance.user_password)
# 这个 Query 还接受ORM插入描述符作为参数。当多个类实体或基于列的实体表示为 query() 函数，返回结果表示为元组：
for name, password in session.query(User.user_name, User.user_password):
    print(name, password)
# 返回的元组 Query 是 已命名 元组，由 KeyedTuple 类，并且可以像普通的Python对象一样进行处理。这些名称与属性的名称和类的类名相同：
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
for name, in session.query(User.user_name).filter(User.id == 3):
    print(name)
# 这个 Query 对象完全 生成的 ，这意味着大多数方法调用都返回一个新的 Query 对象，在此对象上可以添加其他条件。
# 例如，要查询名为“ed”且全名为“ed jones”的用户，可以调用 filter() 两次，使用 AND ：
for user in session.query(User).filter(User.user_name == 'lyy-3').filter(User.id == 4):
    print(user)


print("\n\n     Step4:表格数据模糊查询¶")
# 返回列表和标量
# all() 返回一个列表：
query = session.query(User).filter(User.user_name.like('%c')).order_by(User.id)
print(query.all())

# first() 应用一个限制并以标量形式返回第一个结果：
print(query.first())

# # one() 完全获取所有行，如果结果中不存在一个对象标识或复合行，则会引发错误。找到多行时：
# user = query.one()  # MultipleResultsFound: Multiple rows were found for one()
# print(user)

# # 找不到行：
# user = query.filter(User.id == 99).one()  # 这个 one() 对于希望处理“未找到项目”和“找到多个项目”不同的系统来说，方法是很好的；
# 例如RESTful Web服务，它可能希望在未找到结果时引发“404未找到”，但在找到多个结果时引发应用程序错误。
# print(user)  # sqlalchemy.orm.exc.NoResultFound: No row was found for one()

# # one_or_none() 就像 one() ，但如果没有找到结果，则不会引发错误；它只是返回 None . 喜欢 one() 但是，如果发现多个结果，则会引发错误。
# # scalar() 调用 one() 方法，并在成功时返回行的第一列：
# query = session.query(User.id).filter(User.user_name == 'lyy-1a').order_by(User.id)
# print(query.scalar())


print("\n\n     Step5:使用文本SQL¶")
# 使用文本SQL
# 文字字符串可以灵活地用于 Query ，通过指定它们与 text() 构造，这是最适用的方法所接受的。例如， filter() 和 order_by() ：
for user in session.query(User).filter(text("id<4")).order_by(text("id")).all():
    print(user.user_name)
# 可以使用基于字符串的SQL，使用冒号指定绑定参数。要指定值，请使用 params() 方法：
print(session.query(User).filter(text("id<:value and user_name=:name")).
      params(value=7, name="lyy-3c").order_by(User.id))
# 换成.all()就可以了，但是不知道为啥

# 要使用完全基于字符串的语句，请 text() 无法将表示完整语句的构造传递给 from_statement() .
# 如果没有其他说明符，则字符串SQL中的列将与基于名称的模型列匹配，例如下面我们仅使用星号表示加载所有列
print(session.query(User).from_statement(text("select * from user where user_name=:name")).params(name="lyy-3c").all())


print("\n\n     Step6:计数¶")
# Query 包括一个方便的计数方法调用 count() ：
print(session.query(User).filter(User.user_name.like("lyy%")).count())
# 这个 count() 方法用于确定SQL语句将返回多少行。查看上面生成的SQL，sqlAlchemy总是将我们正在查询的内容放入子查询中，然后计算其中的行数。
# 在某些情况下，这可以简化为 SELECT count(*) FROM table
# 但是，现代版本的SQLAlchemy并不试图猜测这是什么时候合适，因为可以使用更明确的方法发出准确的sql。

# 对于需要特别指出“要计数的东西”的情况，我们可以直接使用表达式指定“count”函数。
# func.count() ，可从 func 构建。下面我们使用它返回每个不同用户名的计数：
print(session.query(func.count(User.user_name), User.user_name).group_by(User.user_name).all())
# 为了实现我们的简单 SELECT count(*) FROM table 我们可以将其应用于：
print(session.query(func.count('*')).select_from(User).scalar())
# 用法 select_from() 如果我们用 User 主键直接：
print(session.query(func.count(User.id)).scalar())


print("\n\n     Step7:建立关系¶")
# 让我们考虑第二个表如何与 User ，可以进行映射和查询。我们系统中的用户可以存储与其用户名关联的任意数量的电子邮件地址。
# 这意味着从 users 到存储电子邮件地址的新表，我们将调用该表 addresses . 使用声明性，我们定义这个表及其映射类， Address ：


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(60), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

Base.metadata.create_all(engine)


print("\n\n     Step8:使用相关对象¶")
# 现在，当我们创建一个 User 一片空白 addresses 将出现集合。这里可以使用各种集合类型，如集合和字典,但默认情况下，集合是一个python列表。
lyy = User(user_name="liyaoyao", user_password="H3c@12500")
lyy.addresses = [
    Address(email_address="1085865354@qq.com"),
    Address(email_address="yao72396@sina.com"),
    Address(email_address="YS.liyaoyao@h3c.com")
]
session.add(lyy)
session.rollback()
session.commit()
