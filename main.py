import pyautogui
import asyncio
import json
import math
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 挂载静态文件
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get("/")
async def get_web_index():
    return FileResponse("static/index.html")

# 鼠标灵敏度调节
SENSITIVITY = 12


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
    uvicorn.run(app, host='0.0.0.0', port=8000)