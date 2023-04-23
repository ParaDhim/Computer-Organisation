reg = {'000': "0000000000000000",
       '001': "0000000000000000",
       '010': "0000000000000000",
       '011': "0000000000000000",
       '100': "0000000000000000",
       '101': "0000000000000000",
       '110': "0000000000000000",
       '111': "0000000000000000"}
def convert(a):
    b=[]
    k=""
    while a!=0:
        c = a%2
        d = a//2
        b.insert(0,c)
        a = d
    for i in range (0,len(b)):
        k=k+str(b[i])
    while (len(k) < 8) :
        k = "0" + k
    return (k) 

def convertTo16(a):
    b=[]
    k=""
    while a!=0:
        c = a%2
        d = a//2
        b.insert(0,c)
        a = d
    for i in range (0,len(b)):
        k=k+str(b[i])
    while (len(k) < 16) :
        k = "0" + k
    return (k)

def convertTo3(a):
    b=[]
    k=""
    while a!=0:
        c = a%2
        d = a//2
        b.insert(0,c)
        a = d
    for i in range (0,len(b)):
        k=k+str(b[i])
    while (len(k) < 3) :
        k = "0" + k
    return (k)

# To convert 1.5 i.e 1 and 0.5 
def fracTobin(fracPart):
    binary=""
    while (fracPart!=0.0):
        fracPart *= 2
        bit = int(fracPart)
        if (bit == 1) :   
            fracPart -= bit  
            binary += '1'
        else : 
            binary += '0'
    return binary

# returns the 8 bit of IEEE i.e 3 bit exponent and 5 bit mantissa
def decToIEEE(n):
    frac=n-int👎
    in_part=int👎

    s=convert(in_part)+"."+fracTobin(frac)
    i=s.find(".")
    i1=s.find("1")
    exp=convertTo3(i-i1-1)
    mantissa=""
    for i in range(i1,len(s)):
        if(s[i]!="."):
            mantissa+=s[i]
            if len(mantissa)==5:
                break
    if len(mantissa)<5:
        while len(mantissa)<5:
            mantissa+="0"
    return exp+mantissa

def binTOfrac(s):
    f=0
    for i in range(1,len(s)):
        f=f+((int(s[i-1]))(2((-1)(i))))
    return f

def IEEEtodec(s):
    exp=s[0:3]
    mantissa=s[4:]
    e=int(exp,2)
    m=binTOfrac(mantissa)
    dec=(1+m)(2*e)
    return dec

def move_floatingdigit(line,pc):
    R1=int(reg[line[5:8]],2)
    reg[line[5:8]]='00000000'+decToIEEE(R1)
    return convert(int(pc, 2)+1)
    
def add_floatingdigit(line, pc):
    R1 = int(reg[line[7:10]], 2)
    R2 = int(reg[line[10:13]], 2)
    R3 = int(reg[line[13:]], 2)
    R3 = R2+R1
    flag_list = reg['111']
    if(R3 > 31.5):
        flag_list[-3] = "1"

    reg[line[13:1]] = '00000000' + decToIEEE(R3)
    return convert(int(pc, 2)+1)


def sub_floatingdigit(line, pc):
    reg['111'] = '0000000000000000'
    R1 = int(reg[line[7:10]], 2)
    R2 = int(reg[line[10:13]], 2)
    R3 = int(reg[line[13:]], 2)
    R3 = R2-R1
    flag_list = reg['111']
    if(R3 > 0):
        flag_list[-3] = "1"
    reg[line[13:1]] = '00000000' + decToIEEE(R3)
    return convert(int(pc, 2)+1)