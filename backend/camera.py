import cv2
import time

def capture_image(output_path):
    """カメラを起動し、画像を撮影して保存"""
    cap = cv2.VideoCapture(0)  # カメラを開く
    if not cap.isOpened():
        raise RuntimeError("カメラを開けませんでした")

    time.sleep(2)  # 🔹 カメラの露光調整のために 2 秒待機

    # 🔹 カメラのウォームアップ用に数フレーム読み込む
    for _ in range(5):
        ret, frame = cap.read()

    ret, frame = cap.read()  # 🔹 最後のフレームを取得
    cap.release()

    if ret:
        cv2.imwrite(output_path, frame)
        print(f"画像を保存しました: {output_path}")
    else:
        raise RuntimeError("画像のキャプチャに失敗しました")
