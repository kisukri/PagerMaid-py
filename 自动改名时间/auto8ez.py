""" Module to automate message deletion. """
from asyncio import sleep
from datetime import datetime, timezone, timedelta
from pagermaid import logs, scheduler, bot

auto_change_name_init = False

@scheduler.scheduled_job("cron", minute="*")
async def change_name_auto():
    try:
        time_cur = datetime.now(timezone(timedelta(hours=8)))
        time_str = time_cur.strftime('%H:%M')

        _last_name = f"{time_str} HKT"
        await bot.update_profile(last_name=_last_name)

        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"自动修改失败! \n{trac}")
