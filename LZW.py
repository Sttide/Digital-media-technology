#LZW编码 15030140050 刘超
import math
import numpy as np
#字母集

def init():
    en_dict = {'A': 1, 'B': 2, 'C': 3, 'D':4}
    dict_num = 5
    return en_dict,dict_num

def encode(in_str,en_dict,dict_num):
    #传参：输入字符串，编码字典，字典中word的个数
    length = len(in_str)
    i = 0
    code = []
    while(i<length):
        isexise = in_str[i] in en_dict      #是否存在于字典中
        newin_str = in_str[i]
        tmp = i
        while(isexise and (tmp+1 < length)):
            newin_str = newin_str+in_str[tmp+1]
            tmp = tmp+1
            isexise = newin_str in en_dict  #判断是否结束

        #将其及下一位添加至词典中去
        if(not isexise):
            en_dict[newin_str] = dict_num
            dict_num = dict_num+1
            jnum = newin_str[0:-1]
            code.append(en_dict[jnum])
            #print(i, ":", newin_str[0:-1])
            i = tmp
        else:
            #print(i, ":",newin_str)
            jnum = newin_str
            code.append(en_dict[jnum])
            i = tmp + 1
    #print(en_dict)
    return code

def decode(code,en_dict,dict_num):
    #传参：编码，初始编码字典，字典中word的个数
    #方便操作做如下处理
    de_dict = dict(map(lambda t: (t[1], t[0]), en_dict.items()))
    length = len(code)
    #存储结果
    res = ""

    #将字典中第一个加入到解码字符串中去
    res = res + de_dict[code[0]]
    for step in range(length-1):
        #前缀和当前 要解码的码字
        pre = code[step]
        now = code[step+1]
        pre_str = de_dict[pre]

        if now in de_dict:
            #码字对应的字符串在译码词典中，直接解码
            now_str = de_dict[now]
            #print(now_str)
            res = res + now_str
            now_str = pre_str + de_dict[now][0]

            de_dict[dict_num] = now_str
            dict_num = dict_num + 1
        else:
            #码字对应的字符串不在译码字典中
            #将前缀和前缀的第一个字符作为当前串
            now_str = pre_str + pre_str[0]
            #print(now_str)
            res = res + now_str

            de_dict[dict_num] = now_str
            dict_num = dict_num + 1
    #print(de_dict)
    #print(res)
    return res


if __name__ == "__main__":
    en_dict = {'A': 1, 'B': 2, 'C': 3}
    dict_num = 4
    op = input("请输入请求(0:退出 1:编码 2:解码):")
    while (1):
        if op == '0':
            exit(0)
        elif op == '1':
            en_dict, dict_num = init()
            in_str = input("请输入要进行编码的字符串:")
            #in_str = "ABBABABACABA"
            res = encode(in_str,en_dict,dict_num)
            print("编码结果是:",res)
            op = input("请输入请求(0:退出 1:编码 2:解码):")

        elif op == '2':
            in_str = input("请输入要进行译码的字符串:")
            code = []
            for i in in_str:
                code.append(int(i))
            en_dict, dict_num = init()
            ans = decode(code,en_dict,dict_num)
            print("译码结果是:",ans)
            op = input("请输入请求(0:退出 1:编码 2:解码):")
        else:
            raise ValueError("input error")
            exit(0)
