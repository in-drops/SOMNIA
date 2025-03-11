
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
    init_logger()
    if not config.is_browser_run:
        config.is_browser_run = True

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
        logger.info(f'Ожидание перед следующим циклом {cycle_pause} секунд!')
        random_sleep(cycle_pause)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot):

    excel_report = Excel(bot.account, file='SomniaActivity.xlsx')
    excel_report.set_cell('Address', f'{bot.account.address}')
    excel_report.set_date('Date')
    bot.metamask.auth_metamask()
    bot.metamask.select_chain(Chains.SOMNIA_TESTNET)
    bot.ads.open_url('https://testnet.somnia.network')
    random_sleep(10, 20)
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

    random_sleep(5, 10)

    bot.ads.page.get_by_role('button', name='Swap').scroll_into_view_if_needed()
    random_sleep(3, 5)
    bot.ads.page.get_by_role('button', name='Swap').hover(timeout=5000)
    bot.ads.page.get_by_role('button', name='Swap').click()
    random_sleep(20, 30)

    if bot.ads.page.get_by_role('button', name='Mint $PONG').is_enabled(timeout=100000) and bot.ads.page.get_by_role(
            'button',
            name='Mint $PING').is_enabled(timeout=100000):
        bot.ads.page.get_by_role('button', name='Mint $PONG').hover(timeout=5000)
        bot.ads.page.get_by_role('button', name='Mint $PONG').click()
        random_sleep(5, 10)

        for _ in range(50):
            metamask_page = bot.ads.catch_page(['notification'])
            if metamask_page:
                metamask_page.wait_for_load_state('load')
                bot.metamask.universal_confirm()
                break
            random_sleep(5, 10)
        else:
            logger.error(f'Проблема вызова окна Metamask при подтверждении транзакции!')
            return

        random_sleep(5, 10)

        for _ in range(50):
            if not bot.ads.page.get_by_role('button', name='Minting...').is_visible():
                break
            random_sleep(5, 10)
        else:
            logger.error(f'Проблема получения токенов после подтверждении транзакции!')
            return

        bot.ads.page.get_by_role('button', name='Mint $PING').hover(timeout=5000)
        bot.ads.page.get_by_role('button', name='Mint $PING').click()
        random_sleep(5, 10)

        for _ in range(50):
            metamask_page = bot.ads.catch_page(['notification'])
            if metamask_page:
                metamask_page.wait_for_load_state('load')
                bot.metamask.universal_confirm()
                break
            random_sleep(5, 10)
        else:
            logger.error(f'Проблема вызова окна Metamask при подтверждении транзакции!')
            return

        random_sleep(5, 10)

        for _ in range(50):
            if not bot.ads.page.get_by_role('button', name='Minting...').is_visible():
                break
            random_sleep(5, 10)
        else:
            logger.error(f'Проблема получения токенов после подтверждении транзакции!')
            return

    else:
        logger.error('Проблема загрузки элементов страницы!')

    amount = random.randint(10, 300)
    swaps = 0
    random_count = random.randint(2, 5)

    while swaps < random_count:
        bot.ads.page.locator("input[name='amountIn']").click()
        random_sleep(3, 5)
        bot.ads.page.keyboard.type(f'{amount}', delay=500)
        random_sleep(3, 5)

        if bot.ads.page.get_by_role('button', name='Approve').count():
            bot.ads.page.get_by_role('button', name='Approve').click()

            for _ in range(50):
                metamask_page = bot.ads.catch_page(['notification'])
                if metamask_page:
                    metamask_page.wait_for_load_state('load')
                    bot.metamask.universal_confirm()
                    break
                random_sleep(5, 10)
            else:
                logger.error(f'Проблема вызова окна Metamask при подтверждении транзакции!')
                return

            random_sleep(5, 10)

        if bot.ads.page.get_by_role('button', name='Swap').is_enabled():
            bot.ads.page.get_by_role('button', name='Swap').hover(timeout=5000)
            bot.ads.page.get_by_role('button', name='Swap').click()
            for _ in range(50):
                metamask_page = bot.ads.catch_page(['notification'])
                if metamask_page:
                    metamask_page.wait_for_load_state('load')
                    bot.metamask.universal_confirm()
                    break
                random_sleep(5, 10)
            else:
                logger.error(f'Проблема вызова окна Metamask при подтверждении транзакции!')
                return
            random_sleep(5, 10)
            excel_report.increase_counter(f'Swaps')
            swaps += 1
            bot.ads.page.get_by_alt_text('swap').click()
        else:
            bot.ads.page.get_by_alt_text('swap').click()

        if swaps >= random_count:
            logger.success(f'Выполнено {random_count} свапов! Данные записаны в таблицу SomniaActivity.xlsx')
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')
