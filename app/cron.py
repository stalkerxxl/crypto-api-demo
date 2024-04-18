import asyncio
import time

import schedule

from app.services import utils, fmp_service

logger = utils.get_logger("cron")


def update_coins_task():
    asyncio.run(fmp_service.update_coins_from_api())


schedule.every(60).seconds.do(update_coins_task)

if __name__ == "__main__":
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logger.critical(e, exc_info=True)
