from http_client import HTTPClient

http_client = HTTPClient()
url = "http://baidu.com11"
response = http_client.http_get(url)
print(response)