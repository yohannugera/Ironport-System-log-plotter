import matplotlib.pyplot as plt
import datetime
# If matplotlib library not available in python 3
# py -m pip install <<package>>

##doc_list = ["status.log.@20190829T041725.s",
##            "status.log.@20190906T094515.s",
##            "status.log.@20190914T151238.s",
##            "status.log.@20190922T202623.s",
##            "status.log.@20191001T013708.s"]

##doc_list = ["status.log.@20191001T013708.s"]

doc_list = ["status.log.@20190829T041725.s",
            "status.log.@20190906T094515.s",
            "status.log.@20190914T151238.s",
            "status.log.@20190922T202623.s",
            "status.log.@20191001T013708.s"]

logs = {}

months = {"Jan":"01",
         "Feb":"02",
         "Mar":"03",
         "Apr":"04",
         "May":"05",
         "Jun":"06",
         "Jul":"07",
         "Aug":"08",
         "Sep":"09",
         "Oct":"10",
         "Nov":"11",
         "Dec":"12"}

# Sample Log ->
# Tue Oct  1 01:36:59 2019 Info: Status: CPULd 21 DskIO 0 RAMUtil 8 QKUsd 287990 QKFre 8100618 CrtMID 125895152 CrtICID 91744475 CrtDCID 38600282 InjMsg 67015298 InjRcp 94130749 GenBncRcp 2925136 RejRcp 24251370 DrpMsg 4034522 SftBncEvnt 4579222 CmpRcp 95660053 HrdBncRcp 5085738 DnsHrdBnc 381684 5XXHrdBnc 4624430 FltrHrdBnc 0 ExpHrdBnc 79624 OtrHrdBnc 0 DlvRcp 86704996 DelRcp 3869319 GlbUnsbHt 0 ActvRcp 191 UnatmptRcp 66 AtmptRcp 125 CrtCncIn 2 CrtCncOut 2 DnsReq 411694067 NetReq 42609825 CchHit 414532457 CchMis 39017509 CchEct 116639051 CchExp 22128219 CPUTTm 336714 CPUETm 4983467 MaxIO 43950 RAMUsd 342216196 MMLen 442 DstInMem 337 ResCon 0 WorkQ 0 QuarMsgs 5554 QuarQKUsd 1747734 LogUsd 20 SophLd 0 BMLd 0 CASELd 0 TotalLd 38 LogAvail 149G EuQ 0 EuqRls 0 CmrkLd 0 McafLd 0 SwIn 6671439 SwOut 6650224 SwPgIn 31348151 SwPgOut 50267442 RptLd 0 QtnLd 0 EncrQ 0 InjBytes 461907789256

ans = []

for x in doc_list:
    file = open(x,"r")
    content = file.readlines()
    for y in content:
        try:
            tmp = y.split()

            # Needed Stats
            CPULd = tmp[8]
            WorkQ = tmp[92]
            InjMsg = tmp[24]
            ActvRcp = tmp[56]
            CrtMID = tmp[18]

            # Date creation
            # In Epoch = (datetime.datetime(2012,04,01,0,0) - datetime.datetime(1970,1,1)).total_seconds()
            year = int(tmp[4])
            month = int(months[tmp[1]])
            day = int(tmp[2])
            tmplist = tmp[3].split(":")
            hour = int(tmplist[0])
            mint = int(tmplist[1])
            date = (datetime.datetime(year,month,day,hour,mint) - datetime.datetime(1970,1,1)).total_seconds()

            # Filling the Dictionary
            logs[date] = [eval(CPULd),eval(WorkQ),eval(InjMsg),eval(ActvRcp),eval(CrtMID)]
        except IndexError:
            print("Log: "+y)
    file.close()

print("No. of Entries: "+str(len(logs.keys())))
print("First Log date: "+str(list(logs.keys())[0]))
print("First Log date: "+str(list(logs.keys())[-1]))

x_axis = []
y_axis_CPU = []
y_axis_WorkQ = []
y_axis_InjMsg = []
y_axis_ActvRcp = []
y_axis_CrtMID = []

InjMsgs = 0
Max_InjMsgs = 0
CrtMID = 0
x_axis_t = min(logs.keys())

for key in sorted(logs.keys()):
    x_axis.append(key-x_axis_t)
    y_axis_CPU.append(logs[key][0])
    y_axis_WorkQ.append(logs[key][1])
    y_axis_InjMsg.append(logs[key][2]-InjMsgs)
    InjMsgs = logs[key][2]
    y_axis_ActvRcp.append(logs[key][3])
    y_axis_CrtMID.append(logs[key][4])
    

plt.axes([0, 0, 5, 1])
plt.plot(x_axis[1:],y_axis_ActvRcp[1:])
plt.xlabel('Time')
plt.ylabel('Active Recipients')
plt.grid()
plt.show(block=False)

##for x in logs.keys():
##    plt.scatter(x,logs[x][0])

##file = open("logs.csv","a+")
##for x in logs.keys():
##    file.write(str(x)+","+str(logs[x][0])+"\n")

