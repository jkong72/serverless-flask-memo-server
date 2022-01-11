from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from config import Config
from resources.logout import LogoutResource, jwt_blacklist
from resources.memo import MemoListResource
from resources.memo_change import MemoChangeResource
from resources.register import UserRegisterResource
from resources.login import UserLoginResource

app = Flask(__name__)

app.config.from_object(Config)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader  # 로그아웃 된 (블락리스트에 포함된)
                                # id 인지 확인함
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)
# api.add_resource(,'')
api.add_resource(UserRegisterResource, '/user/register') #가입
api.add_resource(UserLoginResource,'/user/login') #로그인
api.add_resource(LogoutResource,'/user/logout') #로그아웃
api.add_resource(MemoListResource,'/memo') #메모 불러오기와 작성
api.add_resource(MemoChangeResource,'/memo/<int:memo_id>') #메모 수정, 삭제


if __name__ == "__main__":
    app.run()