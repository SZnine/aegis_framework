import requests
class AegisNetworkError(Exception):
    """网络异常，如连接失败，请求失败等"""
    pass
class AegisResponseError(Exception):
    """响应异常，如状态码错误"""
    pass

class HTTPClient:
    #用__init__方便测试
    def __init__(self,default_header = None):
        self.session = requests.Session()#创建session
        if default_header:
            self.session.headers.update(default_header)
    #将headers合并到**kwargs中
    def get(self,url,**kwargs):
        try:
            response = self.session.get(url,**kwargs)
            response.raise_for_status()
            return response #必须要返回一个值
        except requests.exceptions.HTTPError as e:
            raise AegisResponseError(f"Response Error:{e}") from e
        except requests.exceptions.RequestException as e:
            # 暂时抛出异常，以后进行调整
            raise AegisNetworkError(f"Network Error:{e}") from e


    def post(self,url,data = None,json = None,**kwargs):
        try:
            response = self.session.post(url,data = data,json = json,**kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            raise AegisResponseError(f"Response Error:{e}") from e
        except requests.exceptions.RequestException as e:
            # 暂时抛出异常，以后进行调整
            raise AegisNetworkError(f"Network Error:{e}") from e