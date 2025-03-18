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
    bot.onchain.change_chain(Chains.SEPOLIA_TESTNET)
    contract_address = '0x2a0f1C1cE263202f629bF41FA7Caa3D5F8FD52C4'
    sepolia_balance = bot.onchain.get_balance().ether
    if sepolia_balance == 0:
        logger.error(f'Баланс в сети {Chains.SOMNIA_TESTNET} недостаточный: {sepolia_balance:.4f}!')
        return
    tx = bot.onchain._prepare_tx(to_address=contract_address)
    tx['data'] = '0x1249c58b'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена! Данные занесены в таблицу SomniaActivity.xlsx! Hash: {tx_hash}')
    excel_report.increase_counter(f'Avatar NFT')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')