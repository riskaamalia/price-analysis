import hashlib
import hmac
import httplib
import json
import time

# Globals
import urllib

import http

http_timeout = 10

class trade_api:
	def __init__(self):
		self.api_key    = ''
		self.api_secret = ''
		self.api_nonce  = ''

	def signature(self, params):
		sig = hmac.new(self.api_secret.encode(), params.encode(), hashlib.sha512)
		return sig.hexdigest()

	def api_call(self, method, params):
		self.api_nonce = '9223372036854775809'
		params['method'] = method
		params['nonce']  = str(self.api_nonce)
		params  = urllib.urlencode(params)
		headers = {'Content-type':'application/x-www-form-urlencoded', 'Key':self.api_key, 'Sign':self.signature(params)}
		conn    = httplib.HTTPSConnection('vip.bitcoin.co.id', timeout=http_timeout)
		conn.request('POST', '/tapi', params, headers)
		response = conn.getresponse().read().decode()
		data     = json.loads(response)
		conn.close()
		return data

	def getInfo(self):
		return self.api_call('getInfo',{})

pbj = trade_api()
print str(pbj.getInfo())