import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import cv2
# import numpy as np
# from datetime import datetime
# from tensorflow.keras.models import load_model

from image_process import Predict_Image # 自作モジュール

app = Flask(__name__)

# 画面で選択した画像ファイル格納用のフォルダを指定
# 存在しない場合は作成
SAVE_DIR = "images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

@app.route('/images/<path:filepath>')
def send_js(filepath):
    # 指定された画像ファイルを"images"に送る
    return send_from_directory(SAVE_DIR, filepath)

@app.route("/", methods=["GET","POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # 画像として読み込み
        file = request.files['image']
        if file:
            file_name = file.filename

        else: # エラー処理
            return render_template("index.html", err_message="ファイルを選択してください！")

        # 検出
        saved_path, results = Predict_Image(file, file_name, SAVE_DIR)

        if file_name.endswith(".mp4"):
            return  render_template("index2.html",
                                    filepath=os.path.basename(saved_path), result=results)
        else:
            return  render_template("index.html",
                                    filepath=os.path.basename(saved_path), result=results)

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=3333) 
    
