import readExcel
import writeExcel
import random
import math
import tim
import time
C_NPOP = 100 #sl NST
C_MAXGENS = 300 #sl thế hệ
C_PXOVER = 0.8 #xác suất lai ghép
C_PMUTATION = 0.3 ##xác suất đột biến
W = 0.8
C1 = 0.1
C2 = 0.1
print("Run test in range (C_CTART,C_TEST) with:")
print("C_START = ")
C_START = int(input())
print("C_TEST = ")
C_TEST = int(input())
class NSTProfit():
    def __init__(self, profit,vt):
        self.profit = profit
        self.vt = vt
#--------danh gia do thich nghi------------
def TRC(y):
    tong = 0
    for i in range(M):
         tong = tong + H[i]*y[i]
    T = math.sqrt(2*A/tong)
    return A/T + tong*T/2
def evaluate(y): 
    Pc=0
    t = TRC(y)
    for i in range(M):
        Pc = Pc + a[i]*y[i]-b[i]*y[i]*y[i] - TRC(y) - Price[i]*y[i] 
    return Pc;
#---------Them NST ----------------------
def addNST(y):
    gen.append(y) 
    genProfit.append(NSTProfit(evaluate(y),len(gen)-1))
    return
#---------khoi tao-----------------------   
def initialize(): 
    for vt in range(C_NPOP):
        y = []
        for i in range(M):
            y.append(random.randint(ymin[i], ymax[i]))
        addNST(y)
    return C_NPOP
#---------tổ hợp lai ghép đột biến--------
#laighep
def crossover(i):
    i2 = random.randint(0,C_NPOP-1)
    
    x = random.randint(1,M-1)
    y = gen[i][:x] + gen[i2][x:M]
    addNST(y)
    #crossover2
    x = random.randint(0,M-1)
    y = gen[i][:len(gen[i])]
    ope = random.random()-0.5
    y[x] = int(ope*y[x] + (1-ope)*gen[i2][x])
    if (ymin[x]<=y[x] and ymax[x]>=y[x]):
         addNST(y)
    return
#dotbien
def sosanh(y,y1,x,y2,x2,t):
    maxprofit = tim.cal(y[x], -b[x], a[x]-Price[x], -t) + tim.cal(y[x2], -b[x2], a[x2]-Price[x2], -t)
    if ymin[x]>y1 or ymax[x]<y1:
        return 
    if ymin[x2]>y2 or ymax[x2]<y2:
        return 
    p = tim.cal(y1, -b[x], a[x]-Price[x], -t)
    p = p + tim.cal(y2, -b[x2], a[x2]-Price[x2], -t)
    if  p > maxprofit:
        y[x] = y1
        y[x2]=y2
    return
#
def mutationTest(i):
    y=[x for x in gen[i]]
    x = random.randint(0,M-2) 
    y[x]  = random.randint(ymin[x], ymax[x])
    addNST(y)
#laighep+dotbien
def evolutionTest():
    for nst in range(C_NPOP): 
        x = random.random()
        if x<C_PXOVER :
            crossover(nst)
        x = random.random()
        if x<C_PMUTATION :
            mutationTest(nst)
    return
#---------chon thế hệ tiếp theo ----------------
def sortOperator(x):
    return x.profit
def selection():
    genProfit.sort(key=sortOperator, reverse=True)
    gen2 = gen[:len(gen)]
    for i in range(C_NPOP):
        gen[i] = gen2[genProfit[i].vt]
        genProfit[i].vt=i
        
    del gen[C_NPOP:len(gen)]
    del genProfit[C_NPOP:len(genProfit)]
    return
#---------thuat toan di truyen -----------------
def GAnor():
    print("Da dung GA test cua buyer",j,"voi",M,"product")
    dem = 1
    timecount = 1
    for cnt in range(C_MAXGENS):
        gt = genProfit[0].profit;
        evolutionTest()
        selection()
        if (genProfit[0].profit-gt <= 0.001):
            dem = dem+1
            if dem == 20 :
                break
        else:
            gt = genProfit[0].profit
            dem = 1
        timeend = time.time()
        x = timeend - timestart
        if (x//10 == timecount):
            print(round(genProfit[0].profit)) 
            timecount = timecount +1
        #print(genProfit[0].profit) 
    print(timecount)
    print("Sau",cnt+1,"the he",genProfit[0].profit)   
    return(genProfit[0].profit)

#------------------GA----------------------------.
def mutation2(y,x,x2):
    tong = H[x]*y[x] + H[x2]*y[x2]
    xmin = max( ymin[x], (tong - H[x2]*ymax[x2])/H[x])
    xmax = min( ymax[x], (tong - H[x2]*ymin[x2])/H[x])
    w = H[x] / H[x2]
    w2= tong / H[x2]
    t = TRC(y)
    
    r1 = - b[x] - b[x2]*w*w
    r2 = a[x] - Price[x] - (a[x2]- Price[x2])*w + b[x2]*2*w*w2 
    r3 = (a[x2]-Price[x2])*w2-b[x2]*w2*w2-2*t
    y1 =  tim.timmax(xmin, xmax, r1, r2, r3) 
    y2 = (tong - H[x]*y1) / H[x2]
    sosanh(y, int(y1), x, int(y2), x2, t)
    sosanh(y, int(y1)+1, x, int(y2), x2, t)
    sosanh(y, int(y1), x, int(y2)+1, x2, t)
    sosanh(y, int(y1)+1, x, int(y2)+1, x2, t)
#
def mutation(i):
    y=[x for x in gen[i]]
    x = random.randint(0,M-2) 
    y[x]  = random.randint(ymin[x], ymax[x])
    addNST(y)
    #mutation2
    y=gen[i][:M]
    vt = [i for i in range(M)]
    random.shuffle(vt)
    for i in range(M//2):
        mutation2(y,vt[i*2],vt[i*2+1])
    addNST(y)
    return
#laighep+dotbien
def evolution():
    for nst in range(C_NPOP): 
        x = random.random()
        if x<C_PXOVER :
            crossover(nst)
        x = random.random()
        if x<C_PMUTATION :
            mutation(nst)
    return
def GA():
    print("Da dung GA cua buyer",j,"voi",M,"product")
    dem = 1;
    timecount =1 
    for cnt in range(C_MAXGENS):
        gt = genProfit[0].profit;
        evolution()
        selection()
        if (genProfit[0].profit-gt <= 0.001):
            dem = dem+1
            if dem == 20 :
                break
        else:
            gt = genProfit[0].profit
            dem = 1
        timeend = time.time()
        x = timeend-timestart
        if (x//10==timecount):
            print(round(genProfit[0].profit)) 
            timecount = timecount +1
    print(timecount)
    print("Sau",cnt+1,"the he",genProfit[0].profit)    
    return(genProfit[0].profit)
#------------------MAIN-----------------------------
for test in range(C_START,C_TEST):
    print("PROCESS WITH TEST",test)
    # N: number of buyers M: number of product
    (N,M) = readExcel.readData(test)
    Hv=[]       
    Price=[]
    Av=readExcel.readVendor(test,M,Hv,Price)
    H=[i for i in range(M)]
    A=0
    supplyProfit = 0
    for j in range(N):
        a=[]
        b=[]
        ymin=[]
        ymax=[]
        Hb=[]
        Ab = readExcel.readBuyer(test,M,j,a,b,ymin,ymax,Hb)
        for i in range(M):
            x = a[i]/b[i]
            ymax[i] = int(min(ymax[i],x))
            H[i]=Hb[i]+Hv[i]
        A=Ab+Av
        gen=[]
        genProfit=[]
        initialize()
        
        genSave = gen[:C_NPOP]
        genProfitSave = genProfit[:C_NPOP]
        timestart = time.time()
        GAnor()
        
        gen = genSave[:C_NPOP]
        genProfit = genProfitSave[:C_NPOP]
        timestart = time.time()
        GA()
        print("\n")
       # writeExcel.writeBuyer(test,j, gen[0], genProfit[0].profit)
    #print("Supply chain optimal profit =", supplyProfit)