import requests
payload = {'nothing':'63579'}
for i in range(400):
    res = requests.get('http://www.pythonchallenge.com/pc/def/linkedlist.php', params=payload)
    res.raise_for_status()
    print(res.text)
    if not res.text.startswith('and the next nothing is '):
        break
    nothing = ''
    for c in res.text[-20:]:
        if c.isdigit():
            nothing += c
    payload['nothing'] = nothing
