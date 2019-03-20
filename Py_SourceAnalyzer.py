'''
Created on 2019/03/16
@author: tom_uda
'''
# -*- coding: utf-8 -*-
import os,sys
import re
funclist = []
skip_flag = 0
path_w ="PySourceAnalyxer_result.txt"
flow_path_w = "py_flow.md"

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
        line = line[:line.find('(')]
        line = com_skip(line)
        line = line.expandtabs()
        if skip_flag == True:
            continue
        if line.find("def ") == 0:
            line = line[4:line.find("(")]
            print(str(cnt) + "\t" + line)
            funclist.append(line)
    file.close()
    if len(funclist):
        print(funclist)
    else:
        print("funclist is nothing")

def flowdown(path):
    #init
    global flow_path_w
    cnt = 0
    det_flag = False
    call_funclist = []
    state = 0 
    print("--------------flowdown-----------------")
    #file = open(path,"r",encoding = "utf-8")
    outfile = open(flow_path_w,"w",encoding = "utf-8")
    outfile.write("```mermaid\n")
    outfile.write("graph TD\n\n")
    outfile.write("S(start)")

    for i in range(len(funclist)):
        print(funclist[i])
        file = open(path,"r",encoding = "utf-8")
        cnt = 0
        state = 0
        for line in file:
            cnt += 1
            #line = line[:line.find("/n")]
            line = com_skip(line)
            line = line.replace('"',"'")
            if state == 0:
                if line.find("def " + funclist[i]) > -1 :
                    state = 1
            elif state == 1:
                if (line.find("def ") == 0):
                    continue
                elif(line.find("for") > -1):
                    state = 2
                    continue
                elif(line.find("if") > -1):
                    state = 2
                    continue
                else:

                    line = line[line.rfind("    ")+4:]
                    if(len(line) < 2 ):
                        continue
                    print(str(cnt)+" "+line)
                    outfile.write("-->"+str(cnt)+'["'+str(cnt)+" "+line+'"]'+"\n") 
                    outfile.write(str(cnt))
            elif state == 2:
                if(line.find("def ")==0):
                    state = 3
                    break
    outfile.write("-->END[end]\n")
    outfile.write("```")
    outfile.close()

def analyze(path):
    fnc_analyze(path)
    flowdown(path)

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

