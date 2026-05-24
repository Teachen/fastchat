from fastapi import APIRouter, HTTPException, status, Request
from . import scheams, models
from applicaton.utils import wechat_tools
from applicaton.utils.jwt_tool import JwtToken


app = APIRouter()


@app.post('/register', response_model=scheams.UserRegisterResponse)
async def register(request: Request, user_info: scheams.UserRegisterRequest):
    """处理用户注册请求"""
    # 1. 验证用户账号是否重复注册[mobile]
    user = await models.User.filter(mobile=user_info.mobile).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='当前手机已注册，不能重复注册！')

    # 判断验证码是否正确
    redis = request.app.state.redis
    redis_sms = await redis.get(f'sms_{user_info.mobile}')
    if redis_sms is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='验证码已过期！')
    if redis_sms != user_info.sms_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='验证码不正确！')

    # 2. 通过小程序提交的code授权码到微信官方获取当前微信用户的openid和session_key
    wechat_user = wechat_tools.get_wechat_info(user_info.code)

    # 验证微信是否重复注册多个账号
    user = await models.User.filter(openid=wechat_user['openid']).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='当前微信已绑定其他账号，不能重复注册！')

    # 3. 添加用户数据
    user = await models.User.create(
        **dict(user_info),
        username=user_info.mobile,
        avatar=user_info.avatarUrl,
        nickname=user_info.nickName,
        sex=user_info.gender,
        openid=wechat_user['openid']
    )

    # 删除redis中保存的验证码，防止一码多用
    await redis.delete(f'sms_{user_info.mobile}')

    # 4. 返回结构
    return {
        'id': user.id,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'code': status.HTTP_200_OK,
        'err_msg': '用户注册成功',
        'status': 'Success',
        'token': JwtToken.create_token({
            'id': user.id
        }),
    }


@app.get('/login')
async def login():

    return {'methods': 'login'}