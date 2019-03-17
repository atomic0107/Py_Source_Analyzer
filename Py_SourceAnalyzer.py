'''
Created on 2019/03/16
@author: tom_uda
'''
# -*- coding: utf-8 -*-
import os,sys
import re
funclist = []
skip_flag = 0
def com_skip(line):
    global skip_flag
    line = line[:line.find("#")]
    if(skip_flag == 0):
        if(line.find("''") > -1):
            skip_flag = 1
    else:
        if(line.find("''") > -1):
            skip_flag = 2
    return line

def fnc_analyze(path):
    print("――――――――function――――――――")
    cnt = 0
    file = open(path,"r",encoding="utf-8")
    for line in file:
        cnt += 1
        line = line[:line.find('/n')]
        line = com_skip(line)
        if skip_flag == True:
            continue
        #print(line)
        #print(line + "\t" + str(cnt))
        #if (line.find('"') > -1):
        #    print(line[line.find('"'):] +"\t"+ str(cnt))
        
        if(line.find("def ") == 0):
            line = line[4:line.find("(")]
            print(str(cnt) + "\t" + line)
            funclist
    file.close()

def analyze(path):
    fnc_analyze(path)

def main():
    print(os.getcwd())
    print("↓ please input path of folder including analyze source ")
    path = os.getcwd()
    #path = input()
    file_list = os.listdir(path)
    cnt = len(file_list)
    for i in range (cnt):
        line = file_list[i]
        path = os.getcwd()
        if( line.find('.py') > -1 ):
            line = line[line.find('.py'):]
            if len(line) != 3:#ファイル名の拡張子が".py"でなければskip
                continue
            print("file_cnt =" + str(i))
            #print(str(file_list[i]))
            path = path + "//"  + file_list[i]
            analyze(path)

if __name__ == '__main__':
    main()

