import os
import asyncio
import getpass

import aiohttp
import yarl
import lxml.html


DOMAIN = 'lms.nthu.edu.tw'
LOGIN_URL = 'https://lms.nthu.edu.tw/sys/lib/ajax/login_submit.php'
LOGIN_STATE_URL = 'http://lms.nthu.edu.tw/home.php'


class LoginFailed(Exception):
    pass


class ILMSClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

        self.data_dir = os.path.abspath('ilmsdump.d')
        os.makedirs(self.data_dir, exist_ok=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    log = staticmethod(print)

    async def ensure_authenticated(self):
        cred_path = os.path.join(self.data_dir, 'credentials.txt')
        try:
            cred_file = open(cred_path)
        except FileNotFoundError:
            await self.interactive_login()
            with open(cred_path, 'w') as file:
                print(self.session.cookie_jar.filter_cookies(LOGIN_STATE_URL)['PHPSESSID'].value, file=file)
            self.log('Saved credentials to', cred_path)
        else:
            with cred_file:
                self.log('Using existing credentials in', cred_path)
                phpsessid = cred_file.read().strip()
                await self.login_with_phpsessid(phpsessid)

    async def interactive_login(self):
        username = input('iLMS username (leave empty to login with PHPSESSID): ')
        if username:
            password = getpass.getpass('iLMS password: ')
            await self.login_with_username_and_password(username, password)
        else:
            phpsessid = getpass.getpass('iLMS PHPSESSID: ')
            await self.login_with_phpsessid(phpsessid)

    async def login_with_username_and_password(self, username, password):
        login = self.session.get(
            LOGIN_URL,
            params={'account': username, 'password': password}
        )
        async with login as response:
            response.raise_for_status()
            json_body = await response.json(
                content_type=None,  # to bypass application/json check
            )
        json_ret = json_body['ret']
        if json_ret['status'] != 'true':
            raise LoginFailed(json_ret)
        self.log('Logged in as', json_ret['name'])

    async def login_with_phpsessid(self, phpsessid):
        self.session.cookie_jar.update_cookies(
            {'PHPSESSID': phpsessid},
            response_url=yarl.URL(DOMAIN),
        )
        name = await self.get_login_state()
        if name is not None:
            self.log('Logged in as', name)
            return
        raise LoginFailed('cannot login with provided PHPSESSID')

    async def get_login_state(self):
        async with self.session.get(LOGIN_STATE_URL) as response:
            response.raise_for_status()
            body = await response.read()
            html = lxml.html.fromstring(body)

            if not html.xpath('//*[@id="login"]'):
                return None

            name_node = html.xpath('//*[@id="profile"]/div[2]/div[1]/text()')
            assert name_node
            return ''.join(name_node).strip()


async def main():
    async with ILMSClient() as client:
        await client.ensure_authenticated()


asyncio.run(main())
