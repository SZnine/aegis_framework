import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'src'))

from http_client import HTTPClient,AegisNetworkError,AegisResponseError

def test_post_json():
    """测试JSON POST请求"""
    client = HTTPClient(default_header={'User-Agent':'Aegis-HTTPClient/1.0'})
    test_url = 'http://httpbin.org/post'

    json_data = {"project":"Aegis","version":"1.0","status":"building"}
    print("1.测试POST JSON中......")
    try:
        resp = client.post(test_url,json = json_data)
        print(f"状态码：{resp.status_code}")
        returned = resp.json()
        assert returned['json'] == json_data
        print("     ✅JSON数据验证通过")
    except Exception as e:
        print(f"    ❌失败：{e}")

def test_post_form():
    """测试表单 POST请求"""
    client = HTTPClient()
    test_url = 'http://httpbin.org/post'

    form_data = {"key1":"value1","key2":"value2"}
    print("\n2.测试POST 表单中......")#添加\n使得格式更好看
    try:
        resp = client.post(test_url,data = form_data)#此处原本是form_data = form_data，修改为data，可能post中无对应参数名
        print(f"状态码：{resp.status_code}")
        returned = resp.json()#这里为什么用json而不是form
        assert returned['form'] == form_data
        print("     ✅表单数据验证通过")
    except Exception as e:
        print(f"    ❌失败:{e}")

def test_session_and_headers():
    """测试SESSION会话保持以及默认headers"""
    print("\n3.测试会话保持和默认headers......")
    client = HTTPClient(default_header = {'X-Custom-Header':'Test'})
    test_url = "http://httpbin.org/headers"

    try:
        resp = client.get(test_url)
        headers = resp.json()['headers']
        assert 'X-Custom-Header' in headers
        print(f"默认Headers生效：{headers['X-Custom-Header']}")
        print(f"    ✅对话Headers测试通过")
    except Exception as e:
        print(f"    ❌失败：{e}")

if __name__ == '__main__':
    print("开始测试http_client核心功能...")
    test_post_json()
    test_post_form()
    test_session_and_headers()
    print("\n===基础功能测试完成===")
