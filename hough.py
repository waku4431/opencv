import cv2
import numpy as np
import pandas as pd
import csv

camera = cv2.VideoCapture("1.avi")                    #インポート
camera_2 = cv2.VideoCapture("1.avi")

#動画ファイル保存用の設定
fps = int(camera.get(cv2.CAP_PROP_FPS))                     #FPS取得
count = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))           #フレーム数取得
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))               #横幅取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))              #縦幅取得
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')         #動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('video.avi', fourcc, fps, (w, h))   #動画の仕様（ファイル名、fourcc, FPS, サイズ）

#テキストファイルを作成し，開く
df_column = pd.DataFrame(columns=['f', 'x', 'y', 'r'])
with open('te.csv', 'a', encoding='UTF-8',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(df_column)

num = 0

df_all=[]

#画像処理を繰り返す
for j in range(10):
    
    std=100#標準偏差の初期値（初めはバカ大きくした）
            
    #撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
    for n in range(count):
        ret, frame = camera.read()                              #フレームを取得
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)         #モノクロ化
        #frame = cv2.medianBlur(frame, 5)                        #ぼかし
        #frame = cv2.Laplacian(frame, cv2.CV_8UC1, ksize=5)      #ラプラシアンフィルタ
        num += 1
        cimg = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)          #画像出力用カラー化
        ret, cimg_2 = camera_2.read()
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 200, param1=130, param2=25, minRadius=15, maxRadius=25)#ハフ変換
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(cimg_2, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
                cv2.circle(cimg_2, (i[0], i[1]), 2, (0, 0, 255), 3)

                #for文の中で，座標と半径の配列を作る
                data = [num,i[0],i[1],i[2]]         

                #テキストファイルに書き出し
                df_all.append(data)
        
        cv2.imshow('camera', cimg)                              # フレームを画面に表示
        cv2.imshow('Row', cimg_2)
        video.write(cimg_2)                                       # 動画を1フレームずつ保存する

        # キー操作があればwhileループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    df_all = pd.DataFrame(df_all, columns=['f', 'x', 'y', 'r'])

    # 撮影用オブジェクトとウィンドウの解放
    camera.release()
    camera_2.release()
    cv2.destroyAllWindows()

    # 標準偏差
    std_result = df_all['r'].std()
    if std>std_result:
         std=std_result

print(std)

