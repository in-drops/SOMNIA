
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

    bot.ads.page.get_by_role('button', name='Participate').scroll_into_view_if_needed()
    random_sleep(3, 5)
    bot.ads.page.get_by_role('button', name='Participate').hover()
    bot.ads.page.get_by_role('button', name='Participate').click()
    random_sleep(10, 20)

    if bot.ads.page.get_by_role('button', name='Mint 1,000 sUSDT (Free)').is_visible():
        bot.ads.page.get_by_role('button', name='Mint 1,000 sUSDT (Free)').hover()
        bot.ads.page.get_by_role('button', name='Mint 1,000 sUSDT (Free)').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm(windows=2, buttons=2)
        random_sleep(10, 20)
    else:
        pass

    bot.ads.page.get_by_text('Tokens').scroll_into_view_if_needed()

    Somini = 'Somini'
    Somsom = 'Somsom'
    Somi = 'Somi'
    memetoken = random.choice([Somini, Somsom, Somi])
    sell_amount = random.choice(['250', '500', '750'])

    if memetoken == Somini:
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Buy').nth(0).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').nth(0).scroll_into_view_if_needed()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Max').nth(0).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').nth(0).click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Sell').nth(
            0).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name=sell_amount).nth(
            0).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve').nth(0).scroll_into_view_if_needed()
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Approve SOMI').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        bot.metamask.universal_confirm()
        random_sleep(10, 20)


    if memetoken == Somsom:
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Buy').click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').scroll_into_view_if_needed()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Max').click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Sell').click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name=sell_amount).click()
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Approve SMSM').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        bot.metamask.universal_confirm()
        random_sleep(10, 20)


    if memetoken == Somi:
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Buy').nth(1).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').nth(1).scroll_into_view_if_needed()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Max').nth(1).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button',
                                                                                        name='Approve sUSDT').nth(1).click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name='Sell').nth(
            1).click()
        random_sleep(3, 5)
        bot.ads.page.locator('div.flex.justify-center', has_text=memetoken).get_by_role('button', name=sell_amount).nth(
            1).click()
        random_sleep(3, 5)
        bot.ads.page.get_by_role('button', name='Approve SMI').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)
        bot.ads.page.get_by_role('button', name='Place Order').click()
        random_sleep(3, 5)
        bot.metamask.universal_confirm()
        random_sleep(10, 20)

    excel_report.increase_counter(f'Meme Contest')
    logger.success(f'Голосование прошло успешно! Данные записаны в таблицу SomniaActivity.xlsx.')



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')
