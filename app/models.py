#coding:utf-8

from app import db
ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls, user_name):
        user = cls.query.filter(db.or_(
            User.nickname == user_name, User.email == user_name)).first()

        if not user:
            return None

        return user

    def __repr__(self):
        return '<User %r>' % (self.nickname)


'''
is_authenticated 方法有一个具有迷惑性的名称。一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证。

is_active 方法应该返回 True，除非是用户是无效的，比如因为他们的账号被禁止。

is_anonymous 方法应该返回 True，除非是伪造的用户不允许登录系统。

最后，get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式返回我们使用数据库生成的唯一的id。
'''



class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        