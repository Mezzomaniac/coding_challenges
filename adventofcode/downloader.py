from http.cookiejar import Cookie
from os.path import exists
import requests
from requests.cookies import RequestsCookieJar

cookie = Cookie(version=0, name='session', value='53616c7465645f5f4816c9ab84913b0a940d3243e151cf357e20448c24e6044725b148f57b2136bdd45685df50bcb10bbfe672e0225782b33a1474e73d7dae42', port=None, port_specified=False, domain='.adventofcode.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=True, expires=1953553997, discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cookiejar = RequestsCookieJar()
cookiejar.set_cookie(cookie)

def download(year, day, force_download=False):
    filename = f'aoc{year}_{day}input.txt'
    if exists(filename) and not force_download:
        return
    text = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookiejar).text
    with open(filename, 'w') as input_file:
        input_file.write(text)


def get_cookie():
    import werkzeug
    try:
        werkzeug.cached_property = werkzeug.utils.cached_property
    except AttributeError:
        pass
    # Above is to handle version conflicts
    import robobrowser
    browser = robobrowser.RoboBrowser(parser='html5lib')
    browser.open('https://adventofcode.com/')
    browser.follow_link(browser.get_link('[Log In]'))
    browser.follow_link(browser.get_link('[GitHub]'))
    form = browser.get_form()
    form['login'].value = input('login?')
    form['password'].value = input('password?')
    browser.submit_form(form)
    form2 = browser.get_form()
    form2['otp'].value = input('otp?')
    browser.submit_form(form2)
    cookies = browser.session.cookies
    #print(cookies)
    for cookie in cookies:
        #print(cookie, '\n')
        cookiejar = RequestsCookieJar()
        cookiejar.set_cookie(cookie)
        if 'differ' not in requests.get('https://adventofcode.com/2020/day/10/input', cookies=cookiejar).text:
            found = cookie
            print(found)

if __name__ == '__main__':
    get_cookie()
