from http.cookiejar import Cookie
from os.path import exists
import requests
from requests.cookies import RequestsCookieJar

cookie = Cookie(version=0, name='session', value='53616c7465645f5fcb4e4c1852c10cea28e6646bf583e480b524aa14eb2d633a68a0da42d255c951f40c80fada553de6c425db9803cde79a5bd707fea7336fb7', port=None, port_specified=False, domain='.adventofcode.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=True, expires=2014865467, discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cookiejar = RequestsCookieJar()
cookiejar.set_cookie(cookie)

USER_AGENT = {"User-Agent": "github.com/Mezzomaniac/coding_challenges/adventofcode/downloader.py by themezj@hotmail.com"}

def download(year, day, force=False):
    filename = f'aoc{year}_{day}input.txt'
    if exists(filename) and not force:
        return
    text = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookiejar, headers=USER_AGENT).text
    with open(filename, 'w') as input_file:
        input_file.write(text)


def get_cookie():
    import werkzeug
    try:
        werkzeug.cached_property = werkzeug.utils.cached_property
    except AttributeError:
        pass
    import re
    re._pattern_type = re.Pattern
    # Above is to handle version conflicts
    import robobrowser
    browser = robobrowser.RoboBrowser(parser='html5lib')
    browser.open('https://adventofcode.com/')
    browser.follow_link(browser.get_link('[Log In]'))
    browser.follow_link(browser.get_link('[GitHub]'))
    form = browser.get_form()
    form['login'].value = input('Github login?')
    form['password'].value = input('Github password?')
    browser.submit_form(form)
    form2 = browser.get_form()
    form2['app_otp'].value = input('Github 2FA OTP?')
    browser.submit_form(form2)
    cookies = browser.session.cookies
    #print(cookies)
    for cookie in cookies:
        #print(cookie, '\n')
        cookiejar = RequestsCookieJar()
        cookiejar.set_cookie(cookie)
        if 'differ' not in requests.get('https://adventofcode.com/2020/day/10/input', cookies=cookiejar).text:
            print(repr(cookie))
            return browser

if __name__ == '__main__':
    browser = get_cookie()
