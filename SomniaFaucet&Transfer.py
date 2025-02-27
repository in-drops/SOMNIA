
import random
from loguru import logger
from config import config, Chains
from core.bot import Bot
from core.excel import Excel
from models.account import Account
from utils.inputs import input_pause, input_cycle_pause, input_cycle_amount
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles)


def main():

    if not config.is_browser_run:
        config.is_browser_run = True
    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)
    pause = input_pause()
    cycle_amount = input_cycle_amount()
    cycle_pause = input_cycle_pause()

    for i in range(cycle_amount):
        random.shuffle(accounts_for_work)
        for account in accounts_for_work:
            worker(account)
            random_sleep(pause)

        logger.success(f'Цикл {i + 1} завершен, обработано {len(accounts_for_work)} аккаунтов!')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд!')
        random_sleep(cycle_pause)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot):

    excel_report = Excel(bot.account, file='SonniaActivity.xlsx')
    excel_report.set_cell('Address', f'{bot.account.address}')
    excel_report.set_date('Date')
    bot.metamask.auth_metamask()
    bot.metamask.select_chain(Chains.SOMNIA_TESTNET)
    bot.ads.open_url('https://testnet.somnia.network')
    random_sleep(5, 10)
    connect_button = bot.ads.page.get_by_role('button', name='Connect')
    if connect_button.count():
        bot.ads.page.get_by_role('button', name='Connect').click()
        random_sleep(2, 3)
        bot.ads.page.get_by_text('MetaMask').click()
        bot.metamask.universal_confirm()
        random_sleep(2, 3)

    if bot.ads.page.locator('.text-green-500', has_text='Live').count():
        pass
    else:
        logger.error('Сайт на данный момент не активен! Попробуйте позже.')
        return

    for _ in range(3):
        bot.ads.page.reload(wait_until='load')
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Request Tokens').scroll_into_view_if_needed()
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Request Tokens').hover(timeout=10000)
        bot.ads.page.get_by_role('button', name='Request Tokens').click()
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Get STT').hover(timeout=10000)
        bot.ads.page.get_by_role('button', name='Get STT').click()
        random_sleep(20, 30)

    bot.ads.page.locator('button', has_text='Close').click()

    random_sleep(5, 10)
    bot.ads.page.get_by_role('button', name='Send Tokens').hover(timeout=10000)
    bot.ads.page.get_by_role('button', name='Send Tokens').click()
    random_sleep(3, 5)

    bot.ads.page.get_by_role('button', name='0.001').hover(timeout=10000)
    bot.ads.page.get_by_role('button', name='0.001').click()
    random_sleep(3, 5)

    bot.ads.page.get_by_role('button', name='Random Address').hover(timeout=10000)
    bot.ads.page.get_by_role('button', name='Random Address').click()
    random_sleep(3, 5)

    bot.ads.page.get_by_role('button', name='Send STT').hover(timeout=10000)
    bot.ads.page.get_by_role('button', name='Send STT').click()
    bot.metamask.universal_confirm()
    random_sleep(10, 15)

    if bot.ads.page.locator('button', has_text='Close').count():
        bot.ads.page.locator('button', has_text='Close').click()

    bot.ads.page.get_by_role('button', name='Send Tokens').hover(timeout=10000)
    bot.ads.page.get_by_role('button', name='Send Tokens').click()

    if bot.ads.page.get_by_role('dialog').get_by_text('Transfer successful!').count():
        logger.success('Transfer токенов произведён успешно! Данные записаны в таблицу SomniaActivity.xlsx')
        excel_report.increase_counter(f'Transfer Site')
    else:
        logger.error('Transfer токенов не удался! Возможно нехватка баланса или ошибка сайта / блокчейна.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')