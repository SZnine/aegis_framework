from urllib.parse import urlparse

print("DEBUG: Aegis System Loading...")
import argparse
import sys
import time
from datetime import datetime

#引入主文件和模块文件

try:
    from src.core.http_client import HTTPClient
    from src.modules.recon.port_scanner import PortScanner
    from src.modules.recon.fingerprint import WebFingerprint
except ImportError as e:
    print(f"[-] 模块导入失败，请检查目录结构： {e}")
    sys.exit(1)

def banner():
    """
    面子工程
    """
    print(r"""
    ___              _     
   /   |  ___  ____ (_)____
  / /| | / _ \/ __ `/ / ___/
 / ___ |/  __/ /_/ / (__  ) 
/_/  |_|\___/\__, /_/____/  
            /____/          
    Aegis Framework v1.0
    [Builder: 3dot14]
    """)

def main():
    banner()

    #配置参数
    parser = argparse.ArgumentParser(description="Aegis - 自动化渗透测试框架")

    #添加 -u / --url 参数
    parser.add_argument("-u","--url",help = "目标 URL (例如：http://example.com)"),

    #添加 --scan 参数，选择扫描模式
    parser.add_argument("--scan",help = "扫描模式",choices = ["port","web","all"]),

    #解析用户输入的命令
    args = parser.parse_args()

    target = args.url

    parsed = urlparse(target)
    host = parsed.hostname
    if not host:
        host = target

    port = parsed.port

    print(f"清洗后的主机名:{host}")
    print(f"清洗后的端口:{port}")

    start_time = time.time()

    print(f"[*] 任务启动：{datetime.now()}")
    print(f"[*] 目标锁定：{host}")
    print("-" * 50)

    #--- A: 端口扫描 ---
    if args.scan in ["port","all"]:
        print(f"[+] 正在启动端口扫描...")

        #处理一下host
        domain = host.replace("http://","").replace("https://","").split("/")[0]
        scanner = PortScanner()

        #PortScanner中支持线程扫描
        open_ports = scanner.scan_concurrent(domain, target_ports=list(range(2999,3002)))
        print(f"[*] 发现端口：{list(open_ports.keys())}")

    #--- B: 指纹识别 ---
    if args.scan in ["web","all"]:
        print(f"\n[+] 正在启动指纹识别...")
        fingerprint = WebFingerprint()
        results = fingerprint.scan(target)

        if results:
            for tech in results:
                print(f"    [!] 识别到技术：{tech['name']}({tech['description']})")
        else:
            print ("    [-] 未识别到已知指纹")

    duration = time.time() - start_time
    print("-" * 50)
    print(f"[*] 本次扫描完成，耗时：{duration:.2f} 秒")

if __name__ == "__main__":
    main()