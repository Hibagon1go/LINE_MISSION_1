from sys import stdin
import datetime
import sys


def receive_input(): #入力受取り関数
    try:
        lines = sys.stdin.readlines()
        if len(lines) < 2: #ログが2行未満の場合の例外処理
            raise Exception("ログが2行未満しかありません.")

        return lines

    except IOError as e: #I/Oエラーの場合の例外処理
        print("catch IOError:", e)
        sys.exit()

    except Exception as e: #その他のエラーの場合の例外処理
        print(e)
        sys.exit()


def create_log(lines): #ログ作成関数
    log = [] #走行ログを格納する配列

    for i in range(len(lines)):
        if not lines[i].rstrip(): #空行がある場合の例外処理
            raise Exception("空行があります.")
        
        #<LF>, :, .を取り除く前処理       
        t = lines[i].rstrip()
        t = t.replace('<LF>','')
        t = t.replace(':',' ')
        t = t.replace('.',' ',1)

        if len(t.split()) != 5: #ログの形式が異常な場合の例外処理
            raise Exception("ログの形式が異常です.")

        log.append(t.split()) #走行ログ配列にログを追加
    
    if log[0][4] != '0.0': #ログの初期距離が0.0と書かれていない場合の例外処理
        raise Exception("初期距離が0.0となっていません.")

    return log


#=========運賃を計算するための準備をしてくれる関数を定義=========#

def log_info(log_1,log_2): #二つの走行ログを引数に, (ログ1の時刻, ログ2の時刻, 走行時間, 平均走行速度)を返す関数
    try:
        #以下13行, ログの情報を変数に格納(ただし右詰めゼロ埋め)
        Hour_1 = int(log_1[0].zfill(2))
        Hour_2 = int(log_2[0].zfill(2))
        day_1 = Hour_1//24
        day_2 = Hour_2//24
        hour_1 = Hour_1%24
        hour_2 = Hour_2%24
        minute_1 = int(log_1[1].zfill(2))
        minute_2 = int(log_2[1].zfill(2))
        second_1 = int(log_1[2].zfill(2))
        second_2 = int(log_2[2].zfill(2))
        microsecond_1 = int(log_1[3].zfill(3))
        microsecond_2 = int(log_2[3].zfill(3))
        distance = float(log_2[4])

        if distance < 0 or distance > 100: #走行距離が負or10000以上の場合の例外処理
            raise Exception('ログの走行距離が負か100以上になっています.')

        if Hour_1 > 99 or Hour_2 > 99: #ログのhour部分が100以上の場合の例外処理
            raise Exception('ログのhour部分が100以上になっています.')    

        if microsecond_1 > 999 or microsecond_2 > 999: #ログのmicrosecond部分が1000以上の場合の例外処理
            raise Exception('ログのmicrosecond部分が1000以上になっています.')        

        #ログの情報をdatetime型に変換
        time_1 = datetime.datetime(year=1, month=1, day=1+day_1, hour=hour_1, minute=minute_1, second=second_1, microsecond=microsecond_1)
        time_2 = datetime.datetime(year=1, month=1, day=1+day_2, hour=hour_2, minute=minute_2, second=second_2, microsecond=microsecond_2)
        
        if time_1 >= time_2: #時系列がおかしい場合の例外処理
            raise Exception('ログの時系列が正しくありません.')

        run_seconds = (time_2-time_1).total_seconds() #二つの走行ログに記録されている時間の差を, second単位に直す
        ave_v = (distance/run_seconds)*3.6 #二つの走行ログ間の平均時速(km/h)
    
        return (time_1, time_2, run_seconds, ave_v)
    
    except TypeError as e: #TypeErrorの場合の例外処理
        print('catch TypeError:', e)
        sys.exit()
    
    except ValueError as e: #ValueErrorの場合の例外処理
        print('catch ValueError:', e)
        sys.exit()

    except Exception as e: #その他のエラーの場合の例外処理
        print(e)
        sys.exit()


def judge_night(time_1, time_2): #夜間かどうかを判定する関数
    am_5_1 = datetime.datetime(year=1, month=1, day=time_1.day, hour=5) #ログ1の日の5時
    pm_22_1 = datetime.datetime(year=1, month=1, day=time_1.day, hour=22) #ログ1の日の22時
    am_5_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=5) #ログ2の日の5時
    pm_22_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=22) #ログ2の日の22時

    if am_5_1 <= time_1 < pm_22_1 or am_5_2 <= time_2 < pm_22_2: #ログ1またはログ2の記録が昼間なら
        return 0
    else: #ログ1の記録もログ2の記録も夜間なら
        return 1

def judge_lowspeed(run_seconds, ave_v): #低速かどうかを判定する関数
    if ave_v > 10: #低速でないなら
        return 0
    else: #低速なら
        return 1


#=========ここから実際に運賃を計算=========#

fare = 0 #運賃を初期化
total_distance = 0 #総走行距離を初期化
low_speed_runtime = 0 #総低速走行時間を初期化

lines = receive_input() #入力受取り
log = create_log(lines) #ログを作成

for i in range(len(log)-1): #次々と走行ログを取得して処理
    log_1 = log[i]
    log_2 = log[i+1]
    info = log_info(log_1, log_2)
    time_1 = info[0]
    time_2 = info[1]
    run_seconds = info[2]
    ave_v = info[3]
    isNight = judge_night(time_1, time_2)
    isLowspeed= judge_lowspeed(run_seconds, ave_v)
    distance = float(log_2[4]) 
    
    if isNight:
        total_distance += distance*1.25 #走行距離を加算(夜間補正1.25倍)
        if isLowspeed: 
            low_speed_runtime += run_seconds*1.25 #低速走行時間を加算(夜間補正1.25倍)

    else:
        total_distance += distance #走行距離を加算
        if isLowspeed: 
            low_speed_runtime += run_seconds #低速走行時間を加算

if total_distance == 0.0: #総走行距離が0.0mの場合の例外処理
    raise Exception("総走行距離が0mです.")

fare += 410 + int(max(0,total_distance-1052)//237)*80 + int(low_speed_runtime//90)*80 #初乗運賃 + 総走行距離に応じた加算運賃 + 総低速走行時間に応じた加算運賃

print(fare) #運賃を出力


    



