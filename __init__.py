from .main import *

from os.path import realpath

from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Event,
    
    Message,
    MessageSegment,
)
from nonebot.params import CommandArg

__plugin_meta__ = PluginMetadata(
    name="fumo语言生成器",
    description="生成fumo语音，稍加改装之后可以自定义语速、语种",
    usage=(
        "fumo 说话 内容"
    ),
    type="application",
    homepage="https://github.com/hakunomiko/nonebot-plugin-add-friends",
    supported_adapters={"~onebot.v11"},
)

Talk = on_command("fumo 说话", priority=4, block=True)

@Talk.handle()
async def _YukkuriTalk(event: Event, arg: Message = CommandArg()):
    # 期望用户输入格式：说话内容 语速 语种
    user_input = arg.extract_plain_text()
    voice_speed = 110
    phont_num = 0
    try:
        YukkuriTalk(user_input, voice_speed, "output", int(phont_num))
        file_path = realpath('.')
    except Exception as e:
        await Talk.finish(f'错误：输入形式有误 - {e}')
    await Talk.send(MessageSegment.record(f'file:///{file_path}/output.wav'))