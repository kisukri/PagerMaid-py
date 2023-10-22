""" Module to automate message deletion. """

import traceback
from asyncio import sleep
from datetime import datetime, timezone, timedelta
from pagermaid.utils import pip_install

pip_install("emoji")

from emoji import emojize
from pagermaid import logs, scheduler, bot

auto_change_name_init = False
dizzy = emojize(":dizzy:", language='alias')
cake = emojize(":cake:", language='alias')
month_emojis = [month.capitalize() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
time_emoji_symb = [
    emojize(":clock12:", language='alias'),
    emojize(":clock1230:", language='alias'),
    emojize(":clock1:", language='alias'),
    emojize(":clock130:", language='alias'),
    emojize(":clock2:", language='alias'),
    emojize(":clock230:", language='alias'),
    emojize(":clock3:", language='alias'),
    emojize(":clock330:", language='alias'),
    emojize(":clock4:", language='alias'),
    emojize(":clock430:", language='alias'),
    emojize(":clock5:", language='alias'),
    emojize(":clock530:", language='alias'),
    emojize(":clock6:", language='alias'),
    emojize(":clock630:", language='alias'),
    emojize(":clock7:", language='alias'),
    emojize(":clock730:", language='alias'),
    emojize(":clock8:", language='alias'),
    emojize(":clock830:", language='alias'),
    emojize(":clock9:", language='alias'),
    emojize(":clock930:", language='alias'),
    emojize(":clock10:", language='alias'),
    emojize(":clock1030:", language='alias'),
    emojize(":clock11:", language='alias'),
    emojize(":clock1130:", language='alias')
]


@scheduler.scheduled_job("cron", minute="*")
async def change_name_auto():
    try:
        time_cur = datetime.now(timezone(timedelta(hours=8)))
        month = month_emojis[time_cur.month - 1]
        day = time_cur.day
        time_str = time_cur.strftime('%H:%M')
        shift = 1 if time_cur.minute > 30 else 0
        time_emoji = time_emoji_symb[(time_cur.hour % 12) * 2 + shift]

        _last_name = f"{month} {day}, {time_str} HKT {time_emoji}"
        await bot.update_profile(last_name=_last_name)

        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"自动修改失败! \n{trac}")
