from http.cookiejar import Cookie
import requests
from requests.cookies import RequestsCookieJar

cookie = Cookie(version=0, name='session', value='53616c7465645f5f0cd6dfab079f628349c0080f63558a4ab4ed293e0bdb58486b4a3bd6e42ecd761b3359145a522ead', port=None, port_specified=False, domain='.adventofcode.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=True, expires=1937364316, discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cookiejar = RequestsCookieJar()
cookiejar.set_cookie(cookie)

def download(year, day):
    response = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookiejar)
    return response.text
