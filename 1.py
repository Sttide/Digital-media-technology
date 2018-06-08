#对应词典
dict=['A','B','C','D','E']
dictd={
    'A':0.1,
    'B':0.4,
    'C':0.2,
    'D':0.3
}

dictA=[0.1,0.4,0.2,0.3]
a=[]            #编码数组
enca=[]         #解码数组
a.append(0.001) #给左区间加上一个无穷小量

#定义初始化的概率区间
sum=0
for i in range(len(dictA)):
    a.append(sum+dictA[i])
    sum=sum+dictA[i]

#储存编码数组
decode=[]

#初始化数组左右区间
def init():
    return 0,1

#初始化储存保存解码字符串的数组
def initdec():
    decode = []
    return decode

#初始化解码数组为"[0.001,0.1,0.5,0.7,1]
def initenca():
    for i in range(len(a)):
        enca.append(a[i])
    return enca


#编码函数,c:要编码的字符,begin end:当前概率区间
def encoding(c,begin,end):
    # 根据预先定义的字典序查找当前编码值
    pos=ord(c)-ord('A');
    interval=end-begin
    if(interval== 0):
        raise ValueError("string is too big")
        return
    #更新概率区间
    end = begin + interval * a[pos + 1]
    begin = begin+interval*a[pos]
    return begin,end


#解码函数 begin:编码
def decoding(begin):
    #根据解码数组的概率区间找到编码的当前字符
    for i in range(len(enca)):
        if(enca[i]>begin):
            pos=i-1
            break
    #将查找到的字符添加进储存数组
    decode.append(dict[pos])
    #更新概率区间
    newbegin=enca[pos]
    newend=enca[pos+1]
    #(如果新的区间和旧的区间相同,函数结束,返回结果
    if begin==newbegin:
        return
    interval = newend-newbegin
    for i in range(len(enca)):
        enca[i]=a[i]*interval+newbegin
    #查找下一个字符
    decoding(begin)
    return



if __name__=="__main__":

    op=input("请输入请求(0:退出 1:编码 2:解码):")
    while(1):
        if op=='0':
            exit(0)

        elif op=='1':
            begin, end = init()
            str=input("请输入要编码的字符串:")
            for i in str:
                begin,end=encoding(i,begin,end)
            print(str,":" ,begin)
            op = input("请输入请求(0:退出 1:编码 2:解码):")

        elif op=='2':
            begin, end = init()
            initenca()
            initdec()
            num = input("请输入要解码的编码值")
            decoding((float)(num))
            print(decode)
            op = input("请输入请求(0:退出 1:编码 2:解码):")

        else:
            raise ValueError("input error")
            exit(0)
