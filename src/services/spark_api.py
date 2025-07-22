import json
import base64
import hmac
import hashlib
import websocket
import threading
import time
from datetime import datetime
from urllib.parse import urlencode, quote
import ssl

class SparkAPI:
    def __init__(self, app_id, api_key, api_secret):
        # 检查环境变量是否为空
        if not app_id or not api_key or not api_secret:
            raise ValueError("讯飞星火API配置不完整，请检查.env文件中的SPARK_APP_ID、SPARK_API_KEY、SPARK_API_SECRET配置")
        
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.host = "spark-api.xf-yun.com"
        self.path = "/v1/x1"
        self.url = f"wss://{self.host}{self.path}"
        
    def create_url(self):
        """生成带认证信息的WebSocket URL"""
        # 生成RFC1123格式的时间戳
        now = datetime.utcnow()
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # 拼接字符串
        signature_origin = f"host: {self.host}\n"
        signature_origin += f"date: {date}\n"
        signature_origin += f"GET {self.path} HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'), 
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_str = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_str}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.url + '?' + urlencode(v)
        return url

    def generate_request_data(self, messages):
        """生成请求数据"""
        data = {
            "header": {
                "app_id": self.app_id,
                "uid": "user_001"
            },
            "parameter": {
                "chat": {
                    "domain": "x1",
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        return json.dumps(data)

    def send_message(self, content, system_prompt=""):
        """发送消息到星火API"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": content})
        
        url = self.create_url()
        
        # 用于存储响应
        response_data = {"content": "", "error": None, "finished": False}
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                code = data['header']['code']
                if code != 0:
                    response_data["error"] = f"API错误: {data['header']['message']}"
                    response_data["finished"] = True
                    ws.close()
                    return
                
                # 获取响应内容
                choices = data.get("payload", {}).get("choices", {})
                status = data.get("header", {}).get("status", 0)
                content = choices.get("text", [{}])[0].get("content", "")
                
                response_data["content"] += content
                
                # 如果status为2，表示数据传输完毕
                if status == 2:
                    response_data["finished"] = True
                    ws.close()
                    
            except Exception as e:
                response_data["error"] = f"解析响应失败: {str(e)}"
                response_data["finished"] = True
                ws.close()

        def on_error(ws, error):
            response_data["error"] = f"WebSocket错误: {str(error)}"
            response_data["finished"] = True

        def on_open(ws):
            def run():
                data = self.generate_request_data(messages)
                ws.send(data)
            
            thread = threading.Thread(target=run)
            thread.start()

        # 创建WebSocket连接
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            url, 
            on_message=on_message, 
            on_error=on_error, 
            on_open=on_open
        )
        
        # 运行WebSocket
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        # 等待响应完成
        while not response_data["finished"]:
            time.sleep(0.1)
        
        if response_data["error"]:
            raise Exception(response_data["error"])
            
        return response_data["content"]