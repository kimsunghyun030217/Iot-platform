import requests

url = 'http://203.253.128.177:7579/Mobius/sch20221309/ledm'
headers =	{
				'Accept':'application/json',
				'X-M2M-RI':'12345',
				'X-M2M-Origin':'sch20221309', # change to your aei
				'Content-Type':'application/vnd.onem2m-res+json; ty=4'
			}

data =	{
			"m2m:cin": {
				"con": "1"
			}
		}

r = requests.post(url, headers=headers, json=data)

try:
	r.raise_for_status()
	print(r)
except Exception as exc:
	print('There was a problem: %s' % (exc))
