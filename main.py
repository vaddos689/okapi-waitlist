from utils import logger
import helper
from multiprocessing.dummy import Pool
from pyuseragents import random as random_useragent

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru,en;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://www.okapi.xyz',
    'Referer': 'https://www.okapi.xyz/',
    'User-Agent': random_useragent(),
}

email_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.emailnator.com',
    'referer': 'https://www.emailnator.com/',
    'x-requested-with': 'XMLHttpRequest'
}


def main(_):
    for account in range(amount_accs):
        mail_session = helper.get_session(headers=email_headers)
        mail: str = helper.get_email(session=mail_session)
        session = helper.get_session(headers=headers)
        name: str = helper.generate_username()
        waitlist: str | bool = helper.create_waitlist(session=session, mail=mail)

        if not waitlist:
            logger.error(f'{mail} | error with create waitlist account')
        else:

            if helper.add_waitlist_username(user_name=name, session=session,  waitlist_nonce=waitlist):
                logger.success(f'{mail} | success add to waitlist')
                with open('accounts.txt', 'a') as file:
                    file.write(f'{mail}\n')
            else:
                logger.error(f'{mail} | error with create waitlist account')


if __name__ == '__main__':
    threads: int = int(input('Threads: '))
    amount_accs: int = int(input('Amount accounts for register: '))
    print('')

    with Pool(processes=threads) as executor:
        executor.map(main, [None for _ in range(threads)])
