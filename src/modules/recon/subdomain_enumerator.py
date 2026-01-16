import asyncio
from typing import List
from src.core.http_client import HTTPClient

class SubdomainEnumerator:
    """子域名枚举器"""

    def __init__(self,http_client:HTTPClient = None,wordlist_file : str = None):
        self.http_client = http_client or HTTPClient()
        #根据是否存在有效的wordlist_file来判断是否需要使用默认字典
        if wordlist_file:
            self.wordlist = self._load_wordlist_from_file(wordlist_file)
        else:
            self.wordlist = ["www","api","dev","test"]#默认字典

    def _load_wordlist_from_file(self,file_path) -> List[str]:
        """
        从文件加载子域字典
        格式：每行一个子域前缀，支持#注释，忽略空行。
        返回：子域名前缀列表
        """
        wordlist = []
        try:
            with open(file_path,"r",encoding="utf-8") as f:
                for line in f:
                    line = line.strip()#跳过首尾空白符和换行符
                    if not line or line.startswith("#"):
                        continue
                    wordlist.append(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"字典未找到：{file_path}")
        #对是否是空字典进行判断:
        if not wordlist:
            raise ValueError(f"字典为空或找不到子域：{file_path}")

        return wordlist


    def enumerate(self,domain:str) -> List[str]:
        """
        枚举指定域名的子域名
        返回：发现域名的子域名列表
        """
        found = []
        for sub in self.wordlist:
            candidate = f"{sub}.{domain}"
            try:
                resp = self.http_client.get(f"http://{candidate}",timeout = 5)
                if resp.status_code < 400:
                    found.append(candidate)
            except Exception:
                pass
        return found

    async def enumerate_async(self,domain:str):
        pass