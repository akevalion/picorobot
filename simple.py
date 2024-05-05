import requests

headers = {
	"Content-Type": "application/json;charset=UTF-8",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
req = {'someKey': 'somevalue clau claudia'}
try:
	res = requests.post("http://192.168.1.36", json=req, headers=headers)
	print(res.text)
except Exception as e:
	print(e)
	pass

