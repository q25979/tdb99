# -*- coding: utf-8 -*-
import random
import decimal

from flask import current_app
from flask_restful import abort
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from app.model import db, UuidBase

from app.model.currency import Currency
from app.model.setting import Setting
from app.model.pin_code import EmailPinCode, SmsPinCode
from app.model.assets import Assets, AssetsBalanceRecord, g_assets_record_type, g_assets_type

from app.type.typedef_const import TypedefConst

g_user_state_type = TypedefConst()
g_user_state_type.UNCOMPLETED_DATA = 0  # 未完善资料
g_user_state_type.COMPLETED_DATA = 1  # 已经完善资料，未通过测评
g_user_state_type.EVALUATION = 2  # 完善资料并通过了测评

g_user_transaction_level = TypedefConst()
g_user_transaction_level.NORMAL = 0  # 普通级别
g_user_transaction_level.PRIORITY = 1  # 优先级别
g_user_transaction_level.ULTIMATE = 2  # 极优级别


class UserBase(UuidBase):
    __abstract__ = True

    uid = db.Column(db.String(32), unique=True)  # 用户ID
    country_code = db.Column(db.String(16))  # 国际电话区号
    mobile = db.Column(db.String(16), unique=True)  # 手机号
    login_email = db.Column(db.String(100), unique=True)  # 登录邮箱
    password = db.Column(db.String(256), nullable=False)  # 密码
    security_password = db.Column(db.String(256))  # 安全密码
    token = db.Column(db.String(256))  # 访问令牌
    source = db.Column(db.String(64), default='')  # 来源
    locked = db.Column(db.SmallInteger, default=0)  # 是否锁定: 0 未锁定  1 锁定  2 已经删除用户

    @property
    def has_security_password(self):
        return 1 if self.security_password else 0

    def set_uid(self):
        if self.uid:
            return
        try_times = 5
        code = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', 3))
        while try_times:
            try_times -= 1
            code += str(random.randint(100000, 999999))
            if not User.query.filter(User.uid == code).first():
                self.uid = code
                return True

        try_times = 5
        while try_times:
            try_times -= 1
            code += str(random.randint(10000000, 99999999))
            if not User.query.filter(User.uid == code).first():
                self.uid = code
                return True

        abort(400, code=1011, message={'uid': 'uid already exists'})

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_security_password(self, password):
        self.security_password = generate_password_hash(password)

    def verify_security_password(self, password):
        if self.security_password is None:
            return False
        return check_password_hash(self.security_password, password)

    def generate_random_password(self):
        self.set_password(str(random.randint(100000, 999999)))

    def generate_auth_token(self, expiration=5 * 24 * 60 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        self.token = s.dumps({'id': self.id})

    def bind_id(self, unique_id, pin_code, country_code):
        # 带有 @ 用 login_email
        # 首位字符为数字用 mobile
        if '@' in unique_id:
            if self.login_email:
                abort(400, code=1011, message={'login_email': 'login_email already exists'})
            EmailPinCode.flask_check(unique_id, pin_code)
            self.login_email = unique_id
        elif len(unique_id) and unique_id[0].isdigit():
            if self.mobile:
                abort(400, code=1011, message={'mobile': 'mobile already exists'})
            SmsPinCode.flask_check(unique_id, pin_code)
            self.mobile = unique_id
            self.country_code = country_code

    def rebind_id(self, unique_id, pin_code, new_unique_id, new_pin_code, country_code):
        # 带有 @ 用 login_email
        # 首位字符为数字用 mobile
        if '@' in unique_id:
            if self.login_email != unique_id:
                abort(400, code=1002, message={'unique_id': 'login_email does not match'})
            EmailPinCode.flask_check(unique_id, pin_code)
            EmailPinCode.flask_check(new_unique_id, new_pin_code)
            self.login_email = new_unique_id
        elif len(unique_id) and unique_id[0].isdigit():
            if self.mobile != unique_id:
                abort(400, code=1002, message={'unique_id': 'mobile does not match'})
            SmsPinCode.flask_check(unique_id, pin_code)
            SmsPinCode.flask_check(new_unique_id, new_pin_code)
            self.mobile = new_unique_id
            self.country_code = country_code

    @classmethod
    def verify_auth_token(cls, token):
        if not token:
            return None
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = cls.query.get(data['id'])
        if user and not user.locked and user.token == token:
            return user
        return None

    @classmethod
    def get_user(cls, unique_id):
        # 带有 @ 用 login_email
        # 首位字符为数字用 mobile
        # 其它用 uid
        if '@' in unique_id:
            user = cls.query.filter_by(login_email=unique_id).first()
        elif len(unique_id) and unique_id[0].isdigit():
            user = cls.query.filter_by(mobile=unique_id).first()
        else:
            user = cls.query.filter_by(uid=unique_id).first()
        return user

    @classmethod
    def reset_password(cls, unique_id, pin_code, password):
        # 带有 @ 用 login_email
        # 首位字符为数字用 mobile
        user = None
        if '@' in unique_id:
            EmailPinCode.flask_check(unique_id, pin_code)
            user = cls.query.filter_by(login_email=unique_id).first()
        elif len(unique_id) and unique_id[0].isdigit():
            SmsPinCode.flask_check(unique_id, pin_code)
            user = cls.query.filter_by(mobile=unique_id).first()
        if user:
            user.set_password(password)
            user.generate_auth_token()
        return user

    @classmethod
    def reset_security_password(cls, unique_id, pin_code, password):
        # 带有 @ 用 login_email
        # 首位字符为数字用 mobile
        user = None
        if '@' in unique_id:
            EmailPinCode.flask_check(unique_id, pin_code)
            user = cls.query.filter_by(login_email=unique_id).first()
        elif len(unique_id) and unique_id[0].isdigit():
            SmsPinCode.flask_check(unique_id, pin_code)
            user = cls.query.filter_by(mobile=unique_id).first()
        if user:
            user.set_security_password(password)
        return user


class User(UserBase):
    VIRTUAL_ID = '00000000-0000-0000-0000-000000000000'

    name = db.Column(db.String(64))  # 姓名
    avatar = db.Column(db.String(512))  # 头像 URL
    order_mobile = db.Column(db.String(16))
    nickname = db.Column(db.String(64))  # 昵称
    gender = db.Column(db.SmallInteger, default=0)  # 性别: 0 未填  1 男  2 女
    sponsor_id = db.Column(db.String(36), db.ForeignKey('user.id'))  # 推荐人
    active = db.Column(db.SmallInteger, default=0)  # 是否激活: 0 未激活  1 激活
    left_id = db.Column(db.Integer, default=0)  # 用于推荐网络图子节点的查询
    right_id = db.Column(db.Integer, default=0)

    wechat = db.Column(db.String(64))  # 微信

    state = db.Column(db.Integer, default=0)  # 资料和测评状态，参见 g_user_state_type
    allow_transaction = db.Column(db.Integer, default=0)  # 允许交易 0 不允许 1 允许
    transaction_level = db.Column(db.Integer, default=0)  # 交易级别 参见 g_user_transaction_level

    buy_order_cnt = db.Column(db.Integer, default=0)  # 买进的单数

    continuous_buy_cnt = db.Column(db.Integer, default=0)  # 持续购买天数
    today_have_transaction = db.Column(db.SmallInteger, default=0)  # 今天是否拥有一次买卖交易 0 没有 1 有

    team_qualified_cnt = db.Column(db.Integer, default=0)  # 团队合格用户人数

    is_community_node = db.Column(db.SmallInteger, default=0)  # 是否为社区节点 0 不是 1 是

    # relationship
    sponsor = db.relationship('User', foreign_keys=[sponsor_id], remote_side="User.id")
    assets = db.relationship('Assets', uselist=False)

    def is_virtual(self):
        return self.id == User.VIRTUAL_ID

    def is_active(self):
        return self.active == 1

    def activate(self):
        from app.model.schedule_task import RegisterScheduleTask
        self.active = 1
        task = RegisterScheduleTask(user_id=self.id)
        db.session.add(task)

        from app.model.assets import Assets
        assets = Assets(user_id=self.id)
        db.session.add(assets)
        db.session.flush()  # 保证顺序

    def update_state(self, state):
        from app.model.schedule_task import RecommendScheduleTask
        rows_changed = User.query.filter(User.id == self.id, User.state != state).update(dict(state=state))
        if rows_changed:
            if state == g_user_state_type.EVALUATION:
                task = RecommendScheduleTask.query.filter(RecommendScheduleTask.user_id == self.id).first()
                if task is None:
                    task = RecommendScheduleTask(user_id=self.id)
                    db.session.add(task)
                    db.session.flush()  # 保证顺序

    def update_left_right_id(self):
        if self.left_id or self.right_id:
            return False
        parent = User.query.get(self.sponsor_id)
        new_user_left = parent.right_id
        User.query.filter(User.left_id > new_user_left).update(dict(left_id=User.left_id + 2))
        User.query.filter(User.right_id >= new_user_left).update(dict(right_id=User.right_id + 2))
        self.left_id = new_user_left
        self.right_id = new_user_left + 1
        db.session.flush()
        return True

    def update_team_qualified_cnt(self):
        sponsor = self.sponsor
        # 自己也算
        User.query.filter(User.id == self.id).update(
            dict(team_qualified_cnt=User.team_qualified_cnt + 1))
        while sponsor:
            User.query.filter(User.id == sponsor.id).update(
                dict(team_qualified_cnt=User.team_qualified_cnt + 1))

            sponsor = sponsor.sponsor

    def update_recommend_reward(self):
        option = Setting.get_json('general_option')
        recommend_reward_amount = [decimal.Decimal(x) for x in option['recommend_reward_amount']]
        evaluation_reward_amount = decimal.Decimal(option['evaluation_reward_amount'])

        # 先赠送本用户
        usd_price = Currency.get_price()
        if usd_price == 0:
            abort(400, code=1002, message={'usd_price': 'usd_price is invaild'})

        amount = evaluation_reward_amount / usd_price

        assets = Assets.get_assets(self.id)
        details = {
            'message': u'完成评测奖励'
        }
        assets.update_total_balance(amount, g_assets_record_type.EVALUATION, details)

        # 再赠送每一代推荐
        layer = 0
        layer_max = len(recommend_reward_amount)
        sponsor = self.sponsor

        while sponsor and layer < layer_max:

            details = {
                'message': '被推荐人：{}， 第几代：{}'.format(self.uid, layer + 1)
            }
            if sponsor.state == g_user_state_type.EVALUATION:
                assets = Assets.get_assets(sponsor.id)
                assets.update_total_balance(recommend_reward_amount[layer], g_assets_record_type.SPONSOR, details)
            layer += 1
            sponsor = sponsor.sponsor

    def update_transaction_free(self):
        option = Setting.get_json('general_option')
        transaction_free_generation = option['transaction_free_generation']
        transaction_free_amount = option['transaction_free_amount']
        community_free_generation = option['community_free_generation']
        community_free_amount = option['community_free_amount']

        # 加速释放每一代
        layer = 0
        sponsor = self.sponsor
        while sponsor and layer < community_free_generation:

            if sponsor.is_community_node == 0 and layer < transaction_free_generation:
                amount = transaction_free_amount
            elif sponsor.is_community_node == 1:
                amount = community_free_amount
            else:
                amount = 0

            if amount != 0:
                details = {
                    'message': '交易加速释放，交易完成者：{}， 第几代：{}'.format(self.uid, layer + 1)
                }
                assets = Assets.get_assets(sponsor.id)
                # amount = min(assets.total_balance, amount)
                if assets.update_total_balance(-amount, g_assets_record_type.ACCELERATE_FREE, details):
                    assets.update_transaction_balance(amount, g_assets_record_type.ACCELERATE_FREE, details)

            layer += 1
            sponsor = sponsor.sponsor

    # def update_buy_order_cnt(self, delta_amount):
    #     rows_changed = User.query.filter(
    #         User.id == self.id,
    #         User.buy_order_cnt >= -delta_amount).update(
    #         dict(buy_order_cnt=User.buy_order_cnt + delta_amount))
    #     if rows_changed == 1:
    #         return True
    #     return False

    @staticmethod
    def update_continuous_buy_cnt():
        rows_changed = User.query.filter(User.today_have_transaction == 1).update(
            dict(continuous_buy_cnt=User.continuous_buy_cnt + 1))
        if rows_changed:
            User.query.filter(User.today_have_transaction == 0).update(dict(continuous_buy_cnt=0))
            User.query.update(dict(today_have_transaction=0))
            return True
        return False

    def update_today_have_transaction(self):
        rows_changed = User.query.filter(User.id == self.id).update(dict(today_have_transaction=1))
        if rows_changed:
            return True
        return False

    @property
    def cal_team_count(self):

        count = db.session.query(db.func.count(User.id)).filter(
            User.left_id > self.left_id,
            User.locked != 2,
            User.right_id < self.right_id).first()[0]

        if count is None:
            count = 0

        return count

    def update_is_community_node(self):
        rows_changed = User.query.filter(User.id == self.id).update(dict(is_community_node=1))
        if rows_changed:
            return True
        return False

    @property
    def node_profit(self):
        amount = db.session.query(db.func.sum(AssetsBalanceRecord.delta_amount)).filter(
            AssetsBalanceRecord.user_id == self.id,
            AssetsBalanceRecord.record_type == g_assets_record_type.DIVIDEND).first()[0]
        return amount if amount else 0

    @staticmethod
    def initialize():
        virtual_user = User.query.get(User.VIRTUAL_ID)
        if virtual_user is None:
            # 生成虚拟用户
            virtual_user = User(id=User.VIRTUAL_ID,
                                mobile='13288888888',
                                left_id=1,
                                right_id=2,
                                active=1,
                                transaction_level=g_user_transaction_level.ULTIMATE)
            virtual_user.set_password('8RBcdxlofE8F')
            virtual_user.set_security_password('8RBcdxlofE8F')
            virtual_user.uid = 'root'
            db.session.add(virtual_user)
            db.session.flush()
            virtual_user.activate()
            virtual_user.update_state(g_user_state_type.COMPLETED_DATA)
            db.session.commit()


class LoginInfo(UuidBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    client_ip = db.Column(db.String(50), nullable=False)  # 登录IP

    # relationship
    user = db.relationship(User)
