import os

from fastapi import APIRouter, HTTPException, Request
from applicaton.utils import tools, aliyunclound, logs
from applicaton import settings

logger = logs.getLogger(os.environ.get('APP_NAME'))

app = APIRouter()


@app.get('/api')
async def api() -> dict:
    """
    测试api接口
    :return:
    """
    return {'title': 'fastchat test api'}


# @app.get('/exception')
# async def exception(name: str) -> dict:
#     """
#     测试异常的接口
#     :param name:
#     :return:
#     """
#     try:
#         print(username)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return {'title': 'exception'}


@app.get('/sms/{mobile}')
async def sms(request: Request, mobile: str) -> dict:
    """发送验证码"""
    redis = request.app.state.redis
    print("视图中：", id(redis))
    # 1. 生成指定长度随机验证码[纯数字]
    sms_code = tools.genint(settings.SMS['length'])
    # 2. 调用redis保存验证码和手机号
    ret = await redis.setex(f'sms_{mobile}', settings.SMS['expire'], sms_code)
    # 3. 发送验证码短信
    aliyun = aliyunclound.AliYunClound(settings.ALIYUN['key'], settings.ALIYUN['secret'])
    data = {
        'code': sms_code
    }

    result = await aliyun.sms_async(mobile, data, settings.ALIYUN['sms']['sign_name'], settings.ALIYUN['sms']['template_code'])
    if result.code != 'OK':
        logger.error(f'短信发送失败！{result.message}')
        raise HTTPException(status_code=500, detail='短信发送失败！')

    # 4. 返回操作结果
    return {
        'code': 200,
        'err_msg': '短信已发送，请留意手机',
        'status': 'Success',
    }