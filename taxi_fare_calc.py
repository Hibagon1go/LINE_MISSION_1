from sys import stdin
import datetime
import sys

#=========まず, 入力を受け取る=========#

log = [] #走行ログを格納する配列

try:
    lines = sys.stdin.readlines()
except IOError as e:
    print("catch IOError:", e)
    sys.exit()
except Exception as e:
    print(e)
    sys.exit()

for i in range(len(lines)-1):
    if not lines[i].rstrip(): #空行がある場合の例外処理
        raise Exception("空行があります.")

    t = lines[i].rstrip()
    t = t.replace('<LF>','')
    t = t.replace(':',' ')
    t = t.replace('.',' ',1)
    log.append(t.split()) #走行ログに追加

if log[0][4] != '0.0': #ログの初期距離が0でない場合の例外処理
    raise Exception("初期距離が0ではありません.")

if len(log) < 2: #ログが2行未満の場合の例外処理
    raise Exception("ログが2行未満しかありません.")

#=========運賃を計算するための準備をしてくれる関数を定義=========#

def func(log_1,log_2): #二つの走行ログを引数に, (深夜割増が適用されるか,低速か,(走行時間<-低速の場合のみ)) のタプルを返す関数
    try:
        #以下13行, ログの情報を変数に格納
        Hour_1 = int(log_1[0].zfill(2))
        Hour_2 = int(log_2[0].zfill(2))
        day_1 = Hour_1//24
        day_2 = Hour_2//24
        hour_1 = Hour_1%24
        hour_2 = Hour_2%24
        minute_1 = int(log_1[1].zfill(2))
        minute_2 = int(log_2[1].zfill(2))
        second_1=int(log_1[2].zfill(2))
        second_2=int(log_2[2].zfill(2))
        microsecond_1=int(log_1[3].zfill(3))
        microsecond_2=int(log_2[3].zfill(3))
        distance = float(log_2[4])

        if distance < 0 or distance > 100: #走行距離が負or10000以上の場合の例外処理
            raise Exception('ログの走行距離が負か100以上になっています.')

        if Hour_1 > 99 or Hour_2 > 99: #ログのhour部分が100以上の場合の例外処理
            raise Exception('ログのhour部分が100以上になっています.')    

        if microsecond_1 > 999 or microsecond_2 > 999: #ログのmicrosecond部分が1000以上の場合の例外処理
            raise Exception('ログのmicrosecond部分が1000以上になっています.')        

        #ログをdatetime型に変換
        time_1 = datetime.datetime(year=1, month=1, day=1+day_1, hour=hour_1, minute=minute_1, second=second_1, microsecond=microsecond_1)
        time_2 = datetime.datetime(year=1, month=1, day=1+day_2, hour=hour_2, minute=minute_2, second=second_2, microsecond=microsecond_2)

        if time_1 >= time_2: #時系列がおかしい場合の例外処理
            raise Exception('ログの時系列が正しくありません.')

        run_seconds = (time_2-time_1).total_seconds() #二つの走行ログに記録されている時間の差を, second単位に直す
        ave_v = (distance/run_seconds)*3.6 #二つの走行ログ間の平均時速(km/h)
        
        am_5_1 = datetime.datetime(year=1, month=1, day=time_1.day, hour=5) #ログ1の日の5時
        pm_22_1 = datetime.datetime(year=1, month=1, day=time_1.day, hour=22) #ログ1の日の22時
        am_5_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=5) #ログ2の日の5時
        pm_22_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=22) #ログ2の日の22時
        
        if am_5_1 <= time_1 < pm_22_1 or am_5_2 <= time_2 < pm_22_2: #ログ1またはログ2の記録が昼間 
            if ave_v > 10: #低速でないなら
                return (0,0)
            else: #低速なら
                return (0,1,run_seconds)
    
        else: #ログ1の記録もログ2の記録も夜間(この場合に夜間割増発生)
            if ave_v > 10: #低速でないなら
                return (1,0)
            else: #低速なら
                return (1,1,run_seconds)
    
    except TypeError as e:
        print('catch TypeError:', e)
        sys.exit()
    
    except ValueError as e:
        print('catch ValueError:', e)
        sys.exit()

    except Exception as e:
        print(e)
        sys.exit()

#=========ここから実際に運賃を計算=========#

fare = 0 #運賃を初期化
total_distance = 0 #総走行距離を初期化

for i in range(len(log)-1): #次々と走行ログを取得して処理
    log_1 = log[i]
    log_2 = log[i+1]
    cond = func(log_1,log_2)
    distance = float(log_2[4]) 
    
    if cond[0]: #ログ1の記録もログ2の記録も夜間
        total_distance += distance*1.25 #走行距離を加算(夜間補正1.25倍)
        if cond[1]: #低速なら
            fare += (int(cond[2]*1.25)//90)*80 #低速運賃を上乗せ(夜間補正1.25倍)

    else:
        total_distance += distance #走行距離を加算
        if cond[1]: #低速なら
            fare += (int(cond[2])//90)*80 #低速運賃を上乗せ

if total_distance == 0.0:
    raise Exception("総走行距離が0mです.")

fare += 410 + int(max(0,total_distance-1052)//237)*80 #初乗運賃 + 総走行距離に応じた加算運賃

print(fare) #運賃を出力


    



