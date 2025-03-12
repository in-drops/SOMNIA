import random
from loguru import logger
from config import config, Chains
from core.bot import Bot
from core.excel import Excel
from core.onchain import Onchain
from models.account import Account
from models.amount import Amount
from utils.inputs import input_pause
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, get_user_agent)


def main():

    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)
    pause = input_pause()

    for i in range(config.cycle):
        random.shuffle(accounts_for_work)
        for account in accounts_for_work:
            worker(account)
            random_sleep(pause)
        logger.success(f'Цикл {i + 1} завершен, обработано {len(accounts_for_work)} аккаунтов!')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд!')
        random_sleep(*config.pause_between_cycle)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot):

    get_user_agent()
    excel_report = Excel(bot.account, file='SomniaActivity.xlsx')
    excel_report.set_cell('Address', f'{bot.account.address}')
    bot.onchain.change_chain(Chains.SOMNIA_TESTNET)
    conft_nft_address = '0xFC79f0EaC5bEcf21fDcf037bAdb977b2b43DE497'
    amount = Amount(0.1)
    somnia_balance = bot.onchain.get_balance().ether
    if somnia_balance < amount:
        logger.error(f'Баланс в сети {Chains.SOMNIA_TESTNET} недостаточный: {somnia_balance:.4f}! Сумма покупки: {amount:.4f}.')
        return
    tx = bot.onchain._prepare_tx(value=amount, to_address=conft_nft_address)
    tx['data'] = '0x1249c58b'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена! Данные занесены в таблицу SomniaActivity.xlsx! Hash: {tx_hash}')
    excel_report.increase_counter(f'Conft NFT')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')