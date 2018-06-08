import math
dictd={
    'a':0.08167,
    'b':0.01492,
    'c':0.02782,
    'd':0.04253,
    'e':0.12702,
    'f':0.02228,
    'g':0.02015,
    'h':0.06094,
    'i':0.06966,
    'j':0.00153,
    'k':0.00772,
    'l':0.04025,
    'm':0.02406,
    'n':0.06749,
    'o':0.07507,
    'p':0.01929,
    'q':0.00095,
    'r':0.05987,
    's':0.06327,
    't':0.09056,
    'u':0.02758,
    'v':0.00978,
    'w':0.02360,
    'x':0.00150,
    'y':0.01974,
    'z':0.00074,
}

dictA=[0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,
   0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,
   0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074,]


a=[]            #编码数组
enca=[]         #解码数组
a.append(0.0000001)
sum=0;
for i in range(len(dictA)):
    a.append(sum+dictA[i])
    sum=sum+dictA[i]
    #print(a[i])

for i in range(len(a)):
    enca.append(a[i])
    #print(enca[i])
dict=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
        'u', 'v', 'w', 'x', 'y', 'z']
decode=[]


def encoding(c,begin,end):
    pos=ord(c)-ord('a');
    interval=end-begin
    if(interval== 0):
        raise ValueError("string is too big")
        return
    end = begin + interval * a[pos + 1]
    begin = begin+interval*a[pos]
    #print(begin,end)
    return begin,end


def decoding(begin):
    for i in range(len(enca)):
        if(enca[i]>begin):
            pos=i-1
            break

    #print("pos:%f",pos)

    newbegin=enca[pos]
    newend=enca[pos+1]
    decode.append(dict[pos])
    #print(dict[pos])
    if begin==newbegin:
        return
    #print("newbegin:",newbegin,"  newend:",newend)
    interval = newend-newbegin
    #print("interval:",interval)
    for i in range(len(enca)):
        enca[i]=a[i]*interval+newbegin
        #print(i,":",a[i],"  ",enca[i],"  ",begin)
    decoding(begin)
    return

if __name__=="__main__":
    print("友情提示：输入编码字符串超过10位即会溢出！")
    begin=0
    end=1
    #str = "babbaaab"
    str=input("please input a string:")
    if(len(str)>10):
        raise ValueError("String is too long!")

    for i in str:
        begin,end=encoding(i,begin,end)

    print(str,":" ,begin)

    decoding(begin)
    print(decode)
