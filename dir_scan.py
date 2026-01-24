import requests
from urllib.parse import urljoin

def scan_sensitive_paths(target_url):
    """
    敏感目标扫描
    """
    print(f"\n[+] 启动猎人直觉（Dictionary Scan） -> 目标：{target_url}")
    print("-" * 50)

    #1,定义一个小字典（测试用）
    #Juice Shop: 必杀路径: /ftp, /assets, /rest
    sensitive_paths = [
        '/admin',
        '/login',
        '/dashboard',
        '/config',
        '/backup',
        '/ftp',         #Juice Shop彩蛋
        '/assets',      #静态资源
        '/rest',        #api接口
        '/api',
        '/.env',        #配置环境
        '/robots.txt',
        'login.php'
    ]

    #2, 确保url格式正确（自动补齐http://）
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url


    #3, 循环扫描
    found_count = 0
    headers = {
        "User_Agent": "Aegis-Scanner/0.1"   #伪装身份
    }

    for path in sensitive_paths:
        #使用 urljoin智能拼接，防止多余的斜杠
        full_url = urljoin (target_url, path)

        try:
            #设置请求头和时间，防止卡死
            response = requests.get(full_url,headers= headers,timeout=3,allow_redirects=False)

            #核心判断逻辑是，只要返回状态不是404，都算是有东西
            if response.status_code != 404:
                print(f"[+] 发现路径：{path.ljust(15)} | 状态码： {response.status_code}" )
                found_count += 1
        except requests.exceptions.RequestException as e:
            #网络不通处理
            #print(f"[-] 连接失败：{full_url}")
            pass

    print("-" * 50)
    print(f"[*] 扫描结束，发现 {found_count} 个潜在风险路径。")

# --- 自测代码 ---
if __name__ == "__main__":
    target_url = "http://192.168.101.128/dvwa"
    scan_sensitive_paths(target_url)