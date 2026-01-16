import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

from src.modules.recon import SubdomainEnumerator

#默认字典
enumerator = SubdomainEnumerator()
results = enumerator.enumerate("example.com")
print(f"found:{len(results)}potential subdomains:")
for r in results:
    print(f" - {r}")

#从文件加载字典
try :
    enumerator2 = SubdomainEnumerator(wordlist_file = "test_wordlist.txt")
    results2 = enumerator2.enumerate("example.com")
    print(f"从文件加载字典，发现{len(results2)}个潜在子域名：")
    for r in results2:
        print(f" - {r}")
except FileNotFoundError as e:
    print(f"\n文件加载失败：{e}")
except ValueError as e:
    print(f"\n字典文件无效：{e}")
