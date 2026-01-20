import json
import os
from typing import List, Dict, Optional
import requests


class WebFingerprint:
    """
    web指纹识别引擎 v0.1
    负责加载规则库，并对目标URL进行特征匹配
    """

    def __init__(self,rule_file: str ="assets/fingerprints.json"):
        """
        初始化指纹识别器
        :param rule_file:规则文件路径：相对路径
        """
        self.rules = self._load_rules(rule_file)
    def _load_rules(self, rule_file: str) -> List[Dict]:
        """
        加载 JSON 规则库
        :param rule_file:规则文件路径（相对路径）
        """
        #先倒退四级到根目录，再添加规则目录，就是目标路径
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        abs_path = os.path.join(base_dir, rule_file)

        try:
            with open(abs_path,"r",encoding = "utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[!] 警告：指纹库文件未找到：{abs_path}")
            return []
        except json.JSONDecodeError:
            print(f"[!] 警告：指纹库文件格式错误")
            return []

    def scan(self,url:str) -> List[Dict]:
        """
        对目标 URL 进行指纹识别
        """
        results = []

        try:
            #暂时先用requests快速验证
            resp = requests.get(url,timeout = 10,headers = {'User-Agent':'Aegis-Scanner/1.0'})

            #预处理操作
            header_str = str(resp.headers).lower()
            body_str = resp.text.lower()

            #主要逻辑：遍历规则
            for app in self.rules:
                for rule in app.get("rules",[]):
                    matched = False

                    #检查Header
                    if rule['location'] == 'header':
                        #简单的包含匹配
                        target_key = rule.get('key','').lower() #这句话没有被引用的原因是方便测试，下面逻辑判断省略
                        target_value = rule.get('value','').lower()

                        #实际上真正情况应该是header字典与这里一一对应
                        #方便检测，这里只做简单判断
                        if target_value in header_str:
                            matched = True
                    #检查body
                    elif rule['location'] == 'body':
                        target_value = rule.get('value','').lower()
                        if target_value in body_str:
                            matched = True

                    if matched:
                        results.append({
                            "name":app["name"],
                            "description":app["description"],
                            "trigger":rule
                        })
                        break

        except Exception as e:
            print(f"[-] 扫描出错：{e}")

        return results

#--测试--
if __name__ == "__main__":

    scanner = WebFingerprint()

    target = "https://www.wordpress.org"

    print(f"[+] 正在扫描：{target}")
    techs = scanner.scan(target)

    print(f"[+] 扫描结果：{json.dumps(techs, indent=2, ensure_ascii=False)}")

