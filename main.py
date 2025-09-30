import pyautogui
import asyncio
import json
import math
import socket
import qrcode
import os
import sys
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 获取正确的静态文件路径（处理打包后的情况）
def get_static_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序
        return os.path.join(sys._MEIPASS, 'static')
    else:
        # 如果是开发环境
        return 'static'

# 获取正确的文件路径（处理打包后的情况）
def get_file_path(filename):
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序
        return os.path.join(sys._MEIPASS, filename)
    else:
        # 如果是开发环境
        return filename

static_path = get_static_path()

# 挂载静态文件
app.mount('/static', StaticFiles(directory=static_path), name='static')

@app.get("/")
async def get_web_index():
    index_path = os.path.join(static_path, 'index.html')
    return FileResponse(index_path)

# 鼠标灵敏度调节
SENSITIVITY = 12

def get_local_ip():
    """获取本地内网IP地址"""
    try:
        # 创建一个UDP socket来获取本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def generate_qr_code(ip_address, port=8000):
    """生成包含服务器地址的二维码"""
    server_url = f"http://{ip_address}:{port}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(server_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img, server_url


@app.websocket("/ws/mouse_move")
async def mouse_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            msg_type = msg["type"]
            payload = msg["payload"]
            print(data)
            if msg_type == "mouse_move":
                dx = payload.get("dx", 0) * SENSITIVITY
                dy = payload.get("dy", 0) * SENSITIVITY
                pyautogui.move(dx, dy)

    except Exception as e:
        print("鼠标Websocket断开连接",e);


@app.websocket("/ws/action")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("手机客户端已经连接")

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            msg_type = msg["type"]
            payload = msg.get("payload", {})
            print(data)

            if msg_type == "mouse_click":
                if payload.get("button") == "left":
                    pyautogui.click()
                elif payload.get("button") == "right":
                    pyautogui.rightClick()

            if msg_type == "keyboard_press":
                pyautogui.press(payload.get("key"))
    except Exception as e:
        print("WebSocket 连接断开",e)

if __name__ == '__main__':
    # 获取本地IP地址
    local_ip = get_local_ip()
    port = 8000
    
    # 生成二维码
    qr_img, server_url = generate_qr_code(local_ip, port)
    
    # 在终端中显示二维码
    print("\n" + "="*50)
    print("服务器启动信息:")
    print(f"IP地址: {local_ip}")
    print(f"端口: {port}")
    print(f"完整地址: {server_url}")
    print("\n请使用手机扫描下方二维码进行连接:")
    print("="*50)
    
    # 在终端中打印二维码（使用ASCII字符）
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(server_url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    
    print("="*50)
    print("二维码已生成，请用手机扫描后访问网页\n")
    
    # 启动服务器
    uvicorn.run(app, host='0.0.0.0', port=port)