import requests
import hashlib


BASE_URL = 'https://www.gogozhifu.com/createOrder'
APP_ID = '8228d49a499aadd9'
APP_SECRET = '8228d49a499aadd9432d6dd578367d0c'

def getOrderInfo(pay_id, p_type, price, content, notifyUrl=None, returnUrl=None):
	param = 'Quanfita'
	print(str(APP_ID+pay_id+p_type+price+APP_SECRET))
	data = {
		"payId": pay_id,
		"type": p_type,
		"price": price,
		"param": param,
		'isHtml' : 1,
		'sign': hashlib.md5(str(APP_ID+pay_id+param+p_type+price+APP_SECRET).encode(encoding='UTF-8')).hexdigest(),
		'content': content
	}
	if notifyUrl is not None:
		data['notifyUrl'] = notifyUrl
	if returnUrl is not None:
		data['returnUrl'] = returnUrl
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
		"content-type": "application/json",
		"charset": "utf-8",
		"App-Id": APP_ID,
		# "App-Secret": APP_SECRET
		"App-Sign": hashlib.md5(str(APP_ID+APP_SECRET).encode(encoding='UTF-8')).hexdigest()
	}
	response = requests.post(BASE_URL,json=data,headers=headers)
	res = response.text
	print(data)
	print(res)
	# 存储数据
	return res

def checkCallback(pay_id, param, p_type, price, reallyPrice, sign):
	# payId=1547130349673&param=gump994&type=2&price=0.10&reallyPrice=0.10&sign=28943820b95019b6a63598a13c46f93f
	if hashlib.md5(str(APP_ID+pay_id+param+p_type+price+reallyPrice+APP_SECRET).encode(encoding='UTF-8')).hexdigest() == sign:
		return True
	else:
		return False

if __name__ == '__main__':
	getOrderInfo(2, 0.01, 'Iphone 7')