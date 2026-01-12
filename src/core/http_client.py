import requests

class HTTPClient:
#用__init__方便测试
    def __init__(self):
        self.response = None
        self.headers = {}#TODO:必要性现在还不知道。
#在HTTPClient函数中定义http_get方法
    def http_get(self,get_url):
        try:
            self.response = requests.get(get_url)
            self.response.raise_for_status()
            return self.response.text
#抛出异常处理，方便后期错误定位
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")

#测试函数
if __name__ == "__main__":
    http_client = HTTPClient()
    url = "http://httpbin.org/get"
    response = http_client.http_get(url)
    print(response)