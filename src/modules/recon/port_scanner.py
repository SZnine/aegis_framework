import concurrent.futures
import socket
from typing import List, Dict

class PortScanner:
    """Aegis端口扫描器（1.0 TCP全连接）"""

    def __init__(self,target_host:str,target_port:list[int] = None,timeout:float=2.0):
        self.target_host = target_host
        self.ports = target_port if target_port else list(range(1,1025))
        self.timeout = timeout

    def scan_port(self,port:int) -> str:
        """
        扫描单个端口，方便抛出异常
        返回 'open','closed','filtered'
        """

        #使用socket的connect_ex方法
        #返回错误码，而非抛出异常，便于控制
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            #connect_ex 返回0表示成功，否则为错误码
            result = sock.connect_ex((self.target_host,port))
            sock.close()

            if result == 0:
                return "open"#todo这里为何不将此端口赋值给一个数组用于保存有效端口呢？
            else:
                #这里其实根据错误码的不同需要细分对应错误类型与不同的返回状态
                #而考虑到现在是1.0版本，所以将其统一以`closed`状态返回
                return "closed"
        except socket.timeout:
            #意味着数据包丢弃或无响应，一般是被防火墙过滤
            return "filtered"
        except Exception as e:
            #捕获其他类型错误
            #返回错误信息，便于调试
            return f"error:{e}"
    def scan(self) -> Dict[int, str]:
        """扫描所有端口，返回正确{端口：状态}字典"""
        results = {}
        for port in self.ports:
            status = self.scan_port(port)
            results[port] = status#这一步就相当于是添加了port进入results吗
            print(f"{port}:{status}")
        return results
    def scan_concurrent(self, max_workers :int = 50) ->Dict[int,str]:
        """
        使用线程池进行并发扫描
        :param max_workers:最大工作线程数
        :return:端口状态字典
        """
        results = {}
        #线程池管理线程
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            #提交一个扫描任务到线程池
            #建立未来对象到端口的映射
            futures_to_port = {
                executor.submit(self.scan_port,port):port for port in self.ports
            }
            for future in concurrent.futures.as_completed(futures_to_port):
                port = futures_to_port[future]
                try:
                    status = future.result()#获取单个端口的扫描结果状态码
                    results[port] = status
                    print(f"{port}:{status}")#形成正反馈
                except Exception as exc:
                    print(f"扫描异常：{exc}")
        return results