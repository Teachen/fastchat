import asyncio
import os

import requests
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from applicaton.utils import tools, aliyunclound, logs
from applicaton import settings

logger = logs.getLogger(os.environ.get('APP_NAME'))

app = APIRouter()


class ChatMessage(BaseModel):
    role: str = Field(description='消息角色')
    content: str = Field(min_length=1, description='消息内容')


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description='当前用户输入')
    history: list[ChatMessage] = Field(default_factory=list, description='历史消息')


def call_deepseek_api(messages: list[dict]) -> dict:
    url = f"{settings.DEEPSEEK['base_url'].rstrip('/')}/chat/completions"
    headers = {
        'Authorization': f"Bearer {settings.DEEPSEEK['api_key']}",
        'Content-Type': 'application/json',
    }
    payload = {
        'model': settings.DEEPSEEK['model'],
        'messages': messages,
        'stream': False,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=settings.DEEPSEEK['timeout'],
    )
    return response.json(), response.status_code


@app.get('/api')
async def api() -> dict:
    """
    测试api接口
    :return:
    """
    return {'title': 'fastchat test api'}


@app.post('/chat')
async def chat(chat_data: ChatRequest) -> dict:
    """调用 DeepSeek 官方 API 返回对话结果"""
    if not settings.DEEPSEEK['api_key']:
        raise HTTPException(status_code=500, detail='请先在环境变量中配置 DEEPSEEK_API_KEY')

    messages = [{
        'role': 'system',
        'content': settings.DEEPSEEK['system_prompt']
    }]

    for item in chat_data.history:
        if item.role not in {'user', 'assistant', 'system'}:
            continue
        messages.append({
            'role': item.role,
            'content': item.content.strip()
        })

    messages.append({
        'role': 'user',
        'content': chat_data.message.strip()
    })

    try:
        result, status_code = await asyncio.to_thread(call_deepseek_api, messages)
    except requests.RequestException as exc:
        logger.error(f'DeepSeek 接口请求失败：{exc}')
        raise HTTPException(status_code=500, detail='DeepSeek 接口请求失败，请稍后重试')

    if status_code >= 400:
        logger.error(f'DeepSeek 接口返回异常：{result}')
        err_msg = result.get('error', {}).get('message', 'DeepSeek 接口调用失败')
        raise HTTPException(status_code=status_code, detail=err_msg)

    try:
        reply = result['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError, AttributeError):
        logger.error(f'DeepSeek 返回数据格式异常：{result}')
        raise HTTPException(status_code=500, detail='DeepSeek 返回数据格式异常')

    return {
        'code': 200,
        'err_msg': '对话成功',
        'status': 'Success',
        'model': settings.DEEPSEEK['model'],
        'reply': reply,
    }


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
