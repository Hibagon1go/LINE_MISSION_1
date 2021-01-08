import datetime
import random
lst=[]
time = datetime.datetime(year=2021,month=1,day=8,hour=9,minute=46,second=0,microsecond=416)
time_delta = datetime.timedelta(seconds=1)

for i in range(50000):
    time += time_delta
    lst.append(str(time.hour)+":"+str(time.minute)+":"+str(time.second)+"."+str(time.microsecond)+' '+str(random.randint(0,200)/10)+' '+'<LF>')
    
with open('large_sample.txt', 'w') as f:
    for i in range(50000):
        f.write(lst[i])
        f.write("\n")    