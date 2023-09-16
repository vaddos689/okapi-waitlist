import tls_client
import tls_client.sessions
from random import choice
from faker import Faker
import random
import urllib.parse


def get_session(headers: dict) -> tls_client.sessions.Session:
    session = tls_client.Session(client_identifier=choice(['chrome_103',
                                                           'chrome_104',
                                                           'chrome_105',
                                                           'chrome_106',
                                                           'chrome_107',
                                                           'chrome_108',
                                                           'chrome109',
                                                           'Chrome110',
                                                           'chrome111',
                                                           'chrome112',
                                                           'firefox_102',
                                                           'firefox_104',
                                                           'firefox108',
                                                           'Firefox110',
                                                           'opera_89',
                                                           'opera_90']),
                                 random_tls_extension_order=True)
    session.headers.update(headers)

    return session


def send_get_request(url: str, session: tls_client.sessions.Session) -> str | None:
    try:
        response = session.get(
            url=url,
            headers=session.headers,
        )

        if response.status_code == 200:

            return response.json()

    except Exception as ex:
        return None


def send_post_request(url: str, json: dict, session: tls_client.sessions.Session) -> str | None:
    try:
        response = session.post(
            url=url,
            headers=session.headers,
            json=json,
        )

        if response.status_code == 200:

            return response.json()

    except Exception as ex:
        return None


def get_email_csrf_token(url: str, session: tls_client.sessions.Session):
    r = session.get(url=url,
                         headers={
                             **session.headers,
                             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                                       'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                             'accept-language': 'ru,en;q=0.9'
                         })

    return r.cookies['XSRF-TOKEN']


def get_email(session: tls_client.sessions.Session) -> str:
    xsrf_token: str = get_email_csrf_token(session=session, url='https://www.emailnator.com/')

    r = session.post('https://www.emailnator.com/generate-email',
                          json={
                              'email': ['dotGmail']
                          },
                          headers={
                              **session.headers,
                              'x-xsrf-token': urllib.parse.unquote(string=xsrf_token)
                          })
    return r.json()['email'][0]


def generate_username() -> str:
    fake = Faker()
    full_name = fake.unique.first_name().lower().split()
    first_letter = full_name[0][0]
    three_letters_surname = full_name[-1][:3].rjust(3, 'x')
    number = '{:03d}'.format(random.randrange(1, 999))
    username = '{}{}{}'.format(first_letter, three_letters_surname, number)
    return username


def add_waitlist_username(user_name: str, session: tls_client.sessions.Session, waitlist_nonce: str) -> bool | None:
    json = {
        'user_name': user_name,
        'waitlist_nonce': waitlist_nonce,
    }

    response = send_post_request(session=session, json=json, url='https://www.okapi.xyz/api/userdata/waitlist/update')

    if response['error_code'] == 0:
        return True

    else:
        return None


def create_waitlist(mail: str, session: tls_client.sessions.Session) -> str | bool:
    json = {
        'email': mail
    }

    response = send_post_request(session=session, json=json, url='https://www.okapi.xyz/api/userdata/waitlist/create')

    if response['error_code'] == 0:
        return response['payload']['waitlist_nonce']

    else:
        return False
