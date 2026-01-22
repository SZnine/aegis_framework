import sys
import os
import time
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

from src.modules.recon.port_scanner import PortScanner

#测试，添加本地主机的1-100端口作为扫描端口
scanner = PortScanner(timeout=1.0)
#多线程扫描
start = time.time()
results2 = scanner.scan_concurrent(target_host='127.0.0.1' , target_ports=list(range(49682,49699)),max_workers=50)
print(f"多线程扫描时间：{time.time()-start:.2f}秒")
#单线程扫描
start = time.time()
results = scanner.scan(target_host='127.0.0.1' , target_ports=list(range(49682,49699)),)
print(f"单线程测试时间为:{time.time()-start:.2f}秒")

