import requests

class HTTPClient:
    #用__init__方便测试
    def __init__(self):
        self.headers = {}#自定义请求头
    #将headers合并到**kwargs中
    def get(self,url,**kwargs):
        if self.headers:
            self.headers.update(kwargs)
        kwargs['headers'] = self.headers

        try:
            response = requests.get(url,**kwargs)
            return response #必须要返回一个值
        except requests.exceptions.RequestException:
            #暂时抛出异常，以后进行调整
            raise
