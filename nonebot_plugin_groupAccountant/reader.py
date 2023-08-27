import json, re, datetime, os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot import require
from nonebot.rule import to_me

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

#start
reader = on_command('reader', aliases={'结账', '清算', '结算'}, priority=13, block=True)

@reader.handle()
async def handle_function(event: MessageEvent, msg: Message = CommandArg()):
    print('start')
    if text := msg.extract_plain_text():
        if text == 'final' or 'clear':
            resp = await readBook(True)
            await reader.finish(resp)
        elif text == 'help':
            await reader.finish('使用方式为：@bot /结算 (可选的)clear')
    else:
        resp = await readBook(False)
        await reader.finish(resp)
        
async def readBook(clear: bool):
    jsonFile = store.get_data_file('accountant', 'accountant book.json')
    if os.path.getsize(jsonFile) == 0:
        resp = '当前无账目信息'
        return resp
    jsonFileData = jsonFile.read_text()
    dataDic = json.loads(jsonFileData)
    resp = ''
    for key in dataDic:
        resp += str(key + '在' + dataDic[key]['location'] + '，' + dataDic[key]['person'] + '人，消费了' + dataDic[key]['price'] + '元，由'+dataDic[key]['by']+'记录\n')
    if clear == True:
        jsonFile.write_text('')
        resp += '账目已最终清算，账本清除'
    return resp
        