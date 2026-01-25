import requests
from urllib.parse import urljoin
import random
import string
import difflib

def get_random_string(length = 10):#这里是否可以认为是可以使用_来对函数名开头，代表自用函数
    """生成随机字符串，用于探测 404 特征页面"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_page_content(url):
    """获取页面的内容和状态码"""
    headers = {'User_Agent':'Aegis_Scanner/0.2'}
    try:
        response = requests.get(url, headers = headers,timeout = 5,allow_redirects = False)
        return response.status_code,response.content
    except:
        return None,None

def scan_smart(target_url):
    print(f"\n[*] 启动 Aegis 智能扫描: -> 目标 ：{target_url}")
    print("-" * 50)

    if not target_url.startswith("http"):
        target_url = "http://"+target_url

    #--- 阶段一: 学习什么是“不存在” ---
    random_path_1 = get_random_string()
    random_path_2 = get_random_string()

    code_1, content1 = get_page_content(urljoin(target_url,random_path_1))
    code_2, content2 = get_page_content(urljoin(target_url,random_path_2))

    if content1 is None or content2 is None:
        print("[-] 目标无法连接，任务中止")
        return

    #计算错误页面的指纹
    baseline_length = len(content1)
    print(f"[*] 基准测试完成。错误页面平均长度为: {baseline_length}")
    print(f"[*] 错误页面状态码: {code_1}")

    if code_1 == 200:
        print(f"[!] 警告：目标开启了'软404'，所有不存在的页面都会返回 200")
        print(f"[!] Aegis 开启智能过滤模式")

    print("-" * 50)

    #二阶段开始
    sensitive_path = [
        '/admin','/login','/robot.txt','/config','/api','/backup','/ftp','/dashboard'
    ]

    found_count = 0

    for path in sensitive_path:
        full_path = urljoin(target_url,path)
        code, content = get_page_content(full_path)
        #如果没有返回内容，则忽略
        if content is None:
            continue
        #如果状态码是404，则忽略
        if code == 404:
            continue
        similarity = difflib.SequenceMatcher(None,content1,content).ratio()

        if similarity > 0.9:
            continue
        print(f"[+] 发现真实资产：{path.ljust(15)} | 状态码： {code} | 内容差异度：{1-similarity:.2f}")
        found_count += 1
    print("-" * 50)
    print(f"[*] 扫描结束，剔除误报后，共发现{found_count}个有效路径")

# --- 自测代码 ---
if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com"
    scan_smart(target_url)