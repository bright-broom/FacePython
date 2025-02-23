import os
import sys
import cv2
import time
import threading
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# backend ディレクトリを Python パスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# カメラモジュールのインポート
from camera import capture_image

# Flask アプリの作成
app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

# 画像保存ディレクトリ
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route("/")
def index():
    """APIの起動確認"""
    return jsonify({"message": "カメラAPIが起動しています"})

@app.route("/capture", methods=["GET"])
def capture():
    """カメラで画像を撮影し、保存"""
    filename = os.path.join(STATIC_DIR, "captured.jpg")

    # カメラの起動は遅いため、スレッドで撮影処理を実行
    def capture_thread():
        capture_image(filename)

    thread = threading.Thread(target=capture_thread)
    thread.start()
    thread.join()  # 撮影完了を待つ

    return jsonify({"message": "撮影完了", "image_url": "/static/captured.jpg"})

@app.route("/static/<filename>")
def serve_static(filename):
    """撮影した画像を取得"""
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
