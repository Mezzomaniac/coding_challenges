import requests, bs4
payload = {"busynothing":"12345"}
for i in range(400):
	res = requests.get("http://www.pythonchallenge.com/pc/def/linkedlist.php", params=payload)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	print(soup.body)
	nothing = ""
	for c in soup.get_text()[-20:]:
		if c.isdigit():
			nothing += c
	payload["busynothing"] = nothing
print(payload[nothing])
