import cv2
import numpy as np

camera = cv2.VideoCapture("all.avi")                    #インポート

#動画ファイル保存用の設定
fps = int(camera.get(cv2.CAP_PROP_FPS))                     #FPS取得
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))               #横幅取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))              #縦幅取得
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')         #動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('lap.avi', fourcc, fps, (w, h))   #動画の仕様（ファイル名、fourcc, FPS, サイズ）

#撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
while True:
    ret, frame = camera.read()                              #フレームを取得
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)         #モノクロ化
    frame = cv2.Laplacian(frame, cv2.CV_8UC1, ksize=9)      #ラプラシアンフィルタ
    frame = cv2.medianBlur(frame, 9)                        #ぼかし
    cimg = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)          #画像出力用カラー化
    
    cv2.imshow('camera', cimg)                              # フレームを画面に表示
    video.write(cimg)                                       # 動画を1フレームずつ保存する

    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 撮影用オブジェクトとウィンドウの解放
#f.close()
camera.release()
cv2.destroyAllWindows()