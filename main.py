import datetime, base64, requests, json
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# 参考: https://doc.candyhouse.co/ja/SesameAPI

uuid = os.environ['UUID']
secret_key = os.environ['SECRET_KEY']
api_key = os.environ['API_KEY']

cmd = 88  # 88/82/83 = toggle/lock/unlock
history = 'SesameBot'
base64_history = base64.b64encode(bytes(history, 'utf-8')).decode()

print(base64_history)
headers = {'x-api-key': api_key}
cmac = CMAC.new(bytes.fromhex(secret_key), ciphermod=AES)

ts = int(datetime.datetime.now().timestamp())
message = ts.to_bytes(4, byteorder='little')
message = message.hex()[2:8]
cmac = CMAC.new(bytes.fromhex(secret_key), ciphermod=AES)

cmac.update(bytes.fromhex(message))
sign = cmac.hexdigest()
# 鍵の操作
url = f'https://app.candyhouse.co/api/sesame2/{uuid}/cmd'
body = {
    'cmd': cmd,
    'history': base64_history,
    'sign': sign
}
res = requests.post(url, json.dumps(body), headers=headers)
print(res.status_code, res.text)
