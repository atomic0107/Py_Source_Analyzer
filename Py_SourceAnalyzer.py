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
depth_list = []
depth_line_list = []

def com_skip(line):
    global skip_flag
    e_num = 0
    c_num = 0
    if line.find("#") > -1:
        c_num = line.find("#")
        if line.rfind("'") > -1:
            e_num = line.rfind("'")
        if e_num < c_num:
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
    outfile.write("S(start)-->")

    #for i in range(len(funclist)):
    #print(funclist[i])
    file = open(path,"r",encoding = "utf-8")
    cnt = 0
    state = 0
    tabcnt = 0
    line_num = []
    pop_flag = False

    for line in file:
        cnt += 1
        #line = line[:line.find("/n")]
        line = line.replace('"',"'")
        line = com_skip(line)
        if state == 0:
            if(len(funclist) > 0):
                if line.find("def " + funclist[0]) > -1 :
                    funclist.pop(0)
                    state = 1
                    continue
        elif state == 1:
            if (line.find("def ") == 0):
                #state = 0
                continue
            elif(line.find("for") > -1):
                #state = 2
                continue
            elif(line.find("if") > -1) or (line.find("else") > -1):
                #temp_cnt = cnt
                tabcnt = tab_cnt(line)
                for i in range( len(depth_list) ):#> 0:
                    if (depth_list[0] > tab_cnt(line)):
                        depth_list.pop(0)
                        if len(depth_line_list) > 0:
                            line_num.append(depth_line_list[0])
                            depth_line_list.pop(0)
                            pop_flag = True


                depth_list.insert(0,tab_cnt(line)+1)#ネストの深さを記録
                depth_line_list.insert(0,cnt)#if処理の番号を記録

                #write process
                line = line[line.rfind("    ")+4:]
                line = line[:line.find("\n")]
                print(str(cnt)+" "+line)
                print("==> if tabs cnt = "+str(tabcnt+1))
                print("==>"+str(depth_list))
                print("==>"+str(depth_line_list))
                outfile.write(str(cnt)+'{"'+str(cnt)+" "+line+'"}'+"\n")
                if pop_flag == True:
                    for i in range(len(line_num)):
                        outfile.write(str(line_num[i])+"-->|NO|"+str(cnt)+"\n")
                    pop_flag = False
                    line_num.clear()
                outfile.write(str(cnt) + "-->|YES|")
                #state = 2
                continue
            else:
                #write process
                cline = line[line.rfind("    ")+4:]
                if(len(cline) < 2 ):#処理のない行はSkip(改行処理のみの場合等)
                    continue
                for j in range( len(depth_list)):# > 0:
                    if (depth_list[0] > tab_cnt(line)):
                        depth_list.pop(0)
                        if len(depth_line_list) > 0:
                            line_num.append(depth_line_list[0])
                            depth_line_list.pop(0)

                line = line[line.rfind("    ")+4:line.find("\n")]
                print(str(cnt)+" "+line)
                outfile.write(str(cnt)+'["'+str(cnt)+" "+line+'"]'+"\n")
                if pop_flag == True:
                    for i in range(len(line_num)):
                        outfile.write(str(line_num[i])+"-->|NO|"+str(cnt)+"\n")
                    pop_flag = False
                    line_num.clear()
                outfile.write(str(cnt)+"-->")#次の

        elif state == 2:
            if(line.find("def ")==0):
                state = 0
                break
    outfile.write("END[end]\n")
    outfile.write("```")
    outfile.close()

def tab_cnt(line):
    cnt = 0
    while(line.find("    ") == 0):
        if(line.find("    ") == 0):
            line = line[line.find("    ")+4:]
            cnt += 1
    return cnt

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

