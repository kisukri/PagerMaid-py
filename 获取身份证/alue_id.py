#Alue制作，请勿用于非法用途
from pagermaid.listener import listener
from pagermaid.enums import AsyncClient, Message
from pagermaid.utils import lang

import requests
import re


@listener(command="sfz",
          description=lang("随机获取一个真实有效的身份证信息(cn/tw)"))
async def sfz(request: AsyncClient, message: Message):
    args = message.text.split()
    if len(args) > 1:
        country = args[1]
        if country in ['cn', 'tw']:
            url = f"https://api.aagtool.top/api/sjsfz?country={country}"
            response = await request.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == '0':
                    result = {"name": data["user"], "idcard": data["userid"]}
                    if country == 'tw':
                        gender_code = result['idcard'][1:2]
                        gender = '女' if gender_code == '2' else '男' if gender_code == '1' else '未知'
                        birthday = '未知'
                    else:
                        gender = get_gender(result['idcard'])
                        birthday = get_birthday(result['idcard'])
                    info = f"{lang('姓名')}：{result['name']}\n{lang('性别')}：{gender}\n{lang('出生日期')}：{birthday}\n{lang('身份证号')}：{result['idcard']}"
                    await message.edit(info)
                else:
                    await message.edit(lang("获取失败，请重试"))
            else:
                await message.edit(lang("请求接口失败", str(response.status_code)))
        else:
            await message.edit(lang("错误的地区"))
    else:
        await message.edit(lang("请指定地区"))


def get_gender(idcard: str) -> str:
    gender_code = idcard[-2]
    return '女' if int(gender_code) % 2 == 0 else '男'


def get_birthday(idcard: str) -> str:
    year = idcard[6:10]
    month = idcard[10:12].lstrip('0')
    day = idcard[12:14].lstrip('0')
    return f"{year}年{month}月{day}日"