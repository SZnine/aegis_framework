#!/usr/bin/env python3
"""
Aegis-Framework 综合侦察演示脚本
目标：展示从单个域名到子域名以及端口开放情况的完整侦察流程
"""
import sys
import time
import json
from pathlib import Path

#确保能导入到项目模块：
sys.path.insert(0,str(Path(__file__).parent.parent))

from src.modules.recon.port_scanner import PortScanner
from src.modules.recon.subdomain_enumerator import SubdomainEnumerator

def main(target_domain:str,ports_to_scan:list = None):
    """
    主侦察流程
    :param target_domain: 目标主域名
    :param ports_to_scan: 扫描端口范围
    :return:
    """
    print(f"启动对目标域名的综合侦察：{target_domain}")
    results = {
        'target':target_domain,
        'start_time':time.time(),
        'subdomain':[],
        'scan_results':{}
    }

    #1：子域名枚举阶段：
    print(f"\n[阶段一]子域名枚举")
    enumerator = SubdomainEnumerator(
        #此处添加字典文件
        #未添加使用默认字典
    )
    found_subdomains = enumerator.enumerate(target_domain)
    print(f"发现{len(found_subdomains)}个子域名")
    results['subdomain'] = found_subdomains

    if not found_subdomains:
        print("    未发现有效子域名，流程结束。")
        save_results(results)
        return

    #2：端口扫描阶段：
    print(f"\n[阶段二]端口扫描")
    if ports_to_scan is None:
        ports_to_scan = [80, 443, 8080, 22, 21]
    scanner = PortScanner(timeout=2.0)

    for subdomain in found_subdomains:
        print(f"    扫描{subdomain}的端口{ports_to_scan}...")
        #Port.scanner.scan()返回的是Dict[int,str]
        scan_results = scanner.scan_concurrent(target_host = subdomain, target_ports = ports_to_scan,max_workers=50)
        #过滤开放的端口，便于阅读
        open_ports = {port:status for port,status in scan_results.items() if status == 'open'}
        results['scan_results'][subdomain] = {
            'all':scan_results,
            'open':open_ports,
        }
        if open_ports:
            print(f"    发现开放端口：{list(open_ports.keys())}")

    #流程结束
    results['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[+] 侦察流程完成")
    save_results(results)
    return results

def save_results(data:dict,format:str = 'both'):
    """
    保存结果到文件
    :param data: 记录日志所用的字典输入
    :param format: 格式类型
    :return:
    """
    base_name =f"recon_report_{data['target'].replace('.','-')}_{int(time.time())}"
    if format in ('json','both'):
        json_file = f"{base_name}.json"
        with open(json_file,'w') as f:
            json.dump(data,f,indent= 2,ensure_ascii=False)
        print(f"完整的JSON报告保存至：{json_file}")
    if format in ('text','both'):
        text_file = f"{base_name}.txt"
        with open(text_file,'w') as f:
            f.write(f"目标：{data['target']}\n")
            f.write(f"开始时间：{data['start_time']}\n")
            f.write(f"结束时间：{data['end_time']}\n")
            f.write(f"发现子域名总数{len(data['subdomain'])}\n")
            for sub in data['subdomain']:
                f.write(f" - {sub}\n")
            f.write(f"\n端口扫描摘要:\n")
            for sub,scans in data.get('scan_results',{}).items():
                open_ports = scans.get('open',{})
                if open_ports:
                    f.write(f"  {sub}开放端口：{list(open_ports.keys())}\n")
                else:
                    f.write(f"  {sub}没有开放端口\n")
        print(f"txt格式扫描报告已经保存至：{text_file}")

if __name__ == "__main__":
    TARGET = "example.com"
    PORTS = [80, 443, 8080, 22, 21]
    main(TARGET,PORTS)