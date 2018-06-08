#LZSS编码 15030140050 刘超

import numpy as np
#最小匹配长度
min_length = 2

#寻找最长匹配子串
def seek(str,goalstr):
    #在str中查找与goalstr相匹配的最长的字符串
    #dp数组储存长度
    length = len(str)
    dp = [0]*20
    lengoal = len(goalstr)
    for i in range(length):
        if goalstr[0] == str[i]:
            dp[i] = max(dp[i],1)
            j=i+1
            tmp=1
            if tmp >= lengoal or j >= length:
                break
            while(goalstr[tmp]==str[j]):
                dp[j]=max(dp[j],j-i+1)
                tmp=tmp+1
                j=j+1
                if tmp >= lengoal or j >= length:
                    break

    pos = np.argmax(dp,axis=0)
    #print(dp)
    #返回位置，长度，初始位置为dp[x]-pos
    return pos,dp[pos]



def encode(string):
    lengthe = len(string)
    strs = string

    pipeistr = ""
    final =[]
    i = 0
    while(i<lengthe):
        #print(pipeistr,"  ",strs)
        pos,leng = seek(pipeistr,strs)
        if leng>=min_length:
            pipeilen = len(pipeistr)

            final.append((str)(pipeilen-(pos+1-leng)))
            final.append((str)(leng))

            for j in range(leng):
                pipeistr = pipeistr + strs[j]

            #字符串从0开始，所以是leng：
            strs = strs[leng:]
            #i = i + leng
            lengthe = len(strs)
        else:
            final.append(strs[i])

            pipeistr = pipeistr+strs[i]
            strs = strs[i+1:]
            lengthe = len(strs)
    return final

def decoding(code):
    length = len(code)
    res = ""
    i = 0
    while i < length:
        if code[i]>"1" and code[i]<="9":
            origin = int(code[i])
            num = int(code[i+1])
            for j in range(num):
                res = res + res[i-origin+j]
            i = i+2
        else:
            res = res + code[i]
            i = i+1
    return  res


if __name__ == "__main__":
    #测试seek函数
    #x,length =seek("abcdefghaizjf","abc")
    #print(x,length)

    #实现编码
    op = input("请输入请求(0:退出 1:编码 2:解码):")
    while (1):
        if op == '0':
            exit(0)
        elif op == '1':
            string = input("请输入要进行编码的字符串:")
            #string = "AABBCBBAABC"
            res = encode(string)
            code = "".join(res)
            print("编码结果是:",code)
            op = input("请输入请求(0:退出 1:编码 2:解码):")

        elif op == '2':
            in_str = input("请输入要进行译码的字符串:")
            ans = decoding(in_str)
            print("译码结果是:",ans)
            op = input("请输入请求(0:退出 1:编码 2:解码):")

        else:
            raise ValueError("input error")
            exit(0)
