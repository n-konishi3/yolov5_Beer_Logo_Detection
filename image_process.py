from PIL import Image
import numpy as np
from datetime import datetime
import os
import shutil
import detect
import cv2

def Predict_Image(file, file_name, save_dir):
    # 一時フォルダを作成
    temp_dir = os.path.join(save_dir, "temp")
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
    # 一時フォルダの保存先
    saved_temp_path = os.path.join(temp_dir, datetime.now().strftime("%Y%m%d%H%M%S")+ "_" + file_name)

    line_thick = 2     # bounding box thickness
    if not file_name.endswith(".mp4"):
        # 画像の場合リサイズ
        # 学習したサイズが640*640だったのでそれに合わせてリサイズする
        img = Image.open(file)
        IMAGE_WIDTH=640
        IMAGE_HEIGHT=640
        IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)  
        img = img.resize(IMAGE_SIZE)

        # 一時フォルダに保存
        img.save(saved_temp_path)
    else:
        # 動画の場合
        file.save(saved_temp_path)
        line_thick = 3

    # w = "best_beer.pt" # モデルを指定
    w = "best_beer_yolov5s.pt" # モデルを指定
    
    saved_path, results = detect.run(weights=w, source=saved_temp_path, line_thickness=line_thick, 
                                     project=save_dir, name="", exist_ok=True)
  
    # 一時フォルダを削除
    shutil.rmtree(temp_dir)

    return saved_path, results

