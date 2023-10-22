#Alue制作，请勿用于非法用途
import json
import requests
from pagermaid.listener import listener
from pagermaid.enums import AsyncClient, Message
from pagermaid.utils import lang

@listener(command="get_warp",
          description=lang("自动获取warp配置文件\n可选择输入：\nwireguard，wgcf，warp-go，official，clash-meta，xray，sing-box"))
async def get_warp(request: AsyncClient, message: Message):
    try:
        format = message.arguments.lower()
        url = f"https://api.zeroteam.top/warp?format={format}"
        
        if not format:
            await message.edit(lang("请指定配置：\nwireguard，wgcf，warp-go，official，clash-meta，xray，sing-box"))
            return

        if format == "official" or format == "wgcf":
            await message.edit(lang(f"复制链接进入浏览器下载：\n{url}"))
            return

        if format not in ["wireguard", "wgcf", "warp-go", "official", "clash-meta", "xray", "sing-box"]:
            await message.edit(lang("错误的选项，请选择：\nwireguard，wgcf，warp-go，official，clash-meta，xray，sing-box"))
            return

        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            
            try:
                json_data = json.loads(text)
                formatted_json = json.dumps(json_data, indent=4)
                await message.edit(formatted_json)
            except json.JSONDecodeError:
                await message.edit(text)
    

            # await message.edit(formatted_json.replace('\t', '    '))

        elif response.status_code == 429:
            await message.edit(lang("请求过快，请稍后重试"))
        elif response.status_code == 503:
            await message.edit(lang("无可用池，请稍后重试"))
        else:
            await message.edit(lang("请求错误，请稍后重试"))

    except requests.exceptions.RequestException:
        await message.edit(lang("请求异常，请检查网络连接和URL路径"))