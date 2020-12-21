from sys import stdin
import datetime

log = [] #走行ログを格納

while 1: 
    s = stdin.readline().rstrip() #入力の受け取り
    if not s: 
        break #入力が無くなったらbreak
    else:
        log.append(s.split()) #入力が存在したら受け取って走行ログに追加


def func(log_1,log_2): #二つの走行ログから, (深夜割増が適用されるか,低速か,(走行時間))を返す関数
    #走行ログから走行時間,走行距離を数値として取得
    time_1 = datetime.datetime(year=1, month=1, day=1, hour=int(log_1[0][:2]), minute=int(log_1[0][3:5]), second=int(log_1[0][6:8]), microsecond=int(log_1[0][9:]))
    time_2 = datetime.datetime(year=1, month=1, day=1+int(log_2[0][:2])//24, hour=int(log_2[0][:2])%24, minute=int(log_2[0][3:5]), second=int(log_2[0][6:8]), microsecond=int(log_2[0][9:]))
    distance = float(log_2[1]) 

    run_seconds = (time_2-time_1).total_seconds() #二つの走行ログに記録されている時間の差を, second単位に直す
    ave_v = (distance/run_seconds)*3.6 #二つの走行ログ間の平均時速(km/h)

    am_5_1 = datetime.datetime(year=1, month=1, day=1, hour=5) #乗車した日の5時
    pm_22_1 = datetime.datetime(year=1, month=1, day=1, hour=22) #乗車した日の22時
    am_5_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=5) #降車した日の5時
    pm_22_2 = datetime.datetime(year=1, month=1, day=time_2.day, hour=22) #降車した日の22時

    if am_5_1 <= time_1 < pm_22_1 or am_5_2 <= time_2 < pm_22_2: #昼に乗車する or 昼に降車する
        if ave_v > 10: #低速でないなら
            return (0,0)
        else: #低速なら
            return (0,1,run_seconds)
    else: #夜に乗車して夜に降車
        if ave_v > 10: #低速でないなら
            return (1,0)
        else: #低速なら
            return (1,1,run_seconds)
        
    return fare 

fare = 0 #運賃を初期化
distance = 0 #総走行距離を初期化

for i in range(len(log)-1): #次々と走行ログを取得して処理
    log_1 = log[i]
    log_2 = log[i+1]
    cond = func(log_1,log_2) 
    if cond[0]: #夜乗車&夜降車
        distance += float(log_2[1])*1.25/1000 #走行距離をkm単位に変換して加算(夜間補正1.25倍)
        if cond[1]: #低速
            fare += (int(cond[2]*1.25)//90)*80 #低速運賃を上乗せ(夜間補正1.25倍)
    else:
        distance += float(log_2[1])/1000 #走行距離をkm単位に変換して加算
        if cond[1]: #低速
            fare += (int(cond[2])//90)*80 #低速運賃を上乗せ


fare += 410 + (max(0,distance-1052)//237)*80 #初乗運賃 + 総走行距離に応じた加算運賃

print(fare) #運賃を出力


    



