from datetime import time
import time
import requests
from urllib.parse import urljoin
import random
import string
import difflib
import concurrent.futures

headers = {'User_Agent': 'Aegis_Scanner/0.2'}
baseline_content = None #所有进程共享

def get_random_string(length = 10):#这里是否可以认为是可以使用_来对函数名开头，代表自用函数
    """生成随机字符串，用于探测 404 特征页面"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_page_content(url):
    """获取页面的内容和状态码"""
    try:
        response = requests.get(url, headers = headers,timeout = 3,allow_redirects = False)
        return response.status_code,response.content
    except:
        return None,None

def check_one_path(target_url, path):
    """单兵作战，不负责循环"""
    full_url = urljoin(target_url, path)
    code, content = get_page_content(full_url)

    if content is None:
        return

    if code == 404:
        return
    if baseline_content:
        similarity= difflib.SequenceMatcher(baseline_content,content).ratio()
        if similarity > 0.9:
            return
        print(f"[+] 发现：{path.ljust(15)} | 状态：{code} | 差异度 | {1-similarity:.2f}")


def scan_concurrent(target_url, tread_count = 10):
    global baseline_content #使用全局变量

    print(f"\n[*] 启动 Aegis 并发扫描: -> 目标 ：{target_url}")
    print(f"[*] 线程数：{tread_count}")
    print("-" * 50)

    if not target_url.startswith("http"):
        target_url = "http://"+target_url

    # --- 做单线程基准： ---
    print("[*] 正在校验基准...")
    random_path = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    base_code,baseline_content = get_page_content(urljoin(target_url,random_path))

    if baseline_content is None:
        return

    print(f"[*] 基准校验完成。基准状态码：{base_code} | 长度：{len(baseline_content)}")
    print("-" * 50)
    # --- 多线程开发：---
    sensitive_path = [
        '/admin', '/login', '/robot.txt', '/config', '/api',
        '/backup', '/ftp', '/dashboard', '/user', '/images',
        '/static', '/uploads', '/search', '/data', '/db',
        '/sql', '/install', '/test', '/temp', '/cache'
    ] * 5

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers = tread_count) as executor:
        futures = [executor.submit(check_one_path, target_url, path)for path in sensitive_path]
        concurrent.futures.wait(futures)

    end_time = time.time()

    print('-' * 50)
    print(f"[*] 扫描结束")
    print(f"[*] 扫描耗时：{end_time - start_time :.2f}秒")
# --- 自测代码 ---
if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com"
    scan_concurrent(target_url, 20)