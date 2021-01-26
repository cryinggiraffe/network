# coding=utf-8
import os
import sys
import subprocess
from multiprocessing.dummy import Pool as ThreadPool
def write_File(filename,result,mode):
    with open(filename,mode) as f:
        f.writelines(result)
def ping_hosts(ipaddrs):
    result_list=[]
    if sys.platform.startswith('win'):
        for key,value in ipaddrs.items():
            allRe = subprocess.Popen("ping -n 2 %s" %str(key), shell=True, stdout=subprocess.PIPE)
            lines = allRe.stdout.read().decode('gbk')
            if u'100% 丢失' in lines or u'无法访问目标主机' in lines:
                print('本机ping %s:网络不通' % value)
                result_list.append('本机ping %s:网络不通' % value)
            elif u'0% 丢失' in lines:
                print('本机ping %s:网络正常' % value)
                result_list.append('本机ping %s:网络正常' % value)
            else:
                print('本机ping %s:网络可能有丢包' % value)
                result_list.append('本机ping %s:网络有丢包' % value)

    return result_list
#返回一个dict
def ping_hostlist(ipaddrsdic):
    result_list = ipaddrsdic
    if sys.platform.startswith('win'):
        for key, value in ipaddrsdic.items():
            allRe = subprocess.Popen("ping -n 2 %s" % str(value), shell=True, stdout=subprocess.PIPE)
            lines = allRe.stdout.read().decode('gbk')
            if u'100% 丢失' in lines or u'无法访问目标主机' in lines:
                result_list[key]=False
            else:
                result_list[key]=True
    return result_list
def ping_host(item):
    if sys.platform.startswith('win'):
        allRe = subprocess.Popen("ping -n 1 %s" %str(item), shell=True, stdout=subprocess.PIPE)
        lines = allRe.stdout.read().decode('gbk')
        if  u'100% 丢失' in lines or u'无法访问目标主机' in lines:
            #print('本机ping %s不通'%ip)
            stat = '本机ping %s:网络不通'%item
        elif u'0% 丢失' in lines:
            #print('本机ping %s可通'%ip)
            stat = '本机ping %s:网络正常'%item
        else:
            stat = '本机ping %s:网络有丢包' % item
    return stat
def get_cmd_result():
    try:
        if sys.platform.startswith('win'):
            allRe = subprocess.Popen("ipconfig /all", shell=True, stdout=subprocess.PIPE).stdout
            resulttxt = allRe.read().decode('gbk')
            pattern=r'^以太网适配器 以太网|'
    except Exception as e:
        print(u"抱歉，程序出错")
        print(e)
    return resulttxt

def get_network_config():
    '''
    @summary: return the network config of the computer
    '''
    result1 = []
    gateway=''
    ip=''
    flag=0
    networkline =True
    try:
        if sys.platform.startswith('win'):
            allRe=subprocess.Popen("ipconfig /all", shell=True, stdout=subprocess.PIPE).stdout
            lines=allRe.readlines()
            for line in lines:
                line=line.decode('gbk')

                if u'无线' in line or u'蓝牙'in line or '隧道' in line or 'VMnet' in line:
                    flag=0
                    continue
                if (u'以太网适配器 以太网' in line or u'以太网适配器 本地连接' in line) or u'Ethernet adapter 本地连接' in line:
                    #result1.append(line)
                    #print(line)
                    flag=1
                    continue
                if flag==1:
                    if u'媒体已断开连接' in line:
                        #print("媒体已断开连接,您的网线可能未插好")
                        #result1.append(u"媒体已断开连接,您的网线可能未插好")
                        networkline=False
                    if line.lstrip().startswith('物理地址') or line.lstrip().startswith('Physical Address'):
                        mac = line.split(":")[1].strip()
                        #print(u"MAC（麦克）地址为:" + mac)
                        result1.append(u"MAC（麦克）地址:" + mac)
                        continue
                    if line.lstrip().startswith('IPv4') or line.lstrip().startswith('IP Address'):
                        ip = line.split(":")[1].strip()
                        #print(u"IP为:" +ip)
                        result1.append(u"IP地址为:" +ip)
                        continue
                    if line.lstrip().startswith('子网掩码') or line.lstrip().startswith('Subnet Mask'):
                        mask = line.split(":")[1].strip()
                        #print(u"子网掩码为:" + mask)
                        result1.append(u"子网掩码:" + mask)
                        continue
                    if line.lstrip().startswith('默认网关')  or line.lstrip().startswith('Default Gateway'):
                        gateway = line.split(":")[1].strip()
                        #print(u"默认网关为:" + gateway)
                        if(gateway==''):
                            result1.append(u"默认网关地址为:未配置网关地址")
                        else:
                            result1.append(u"默认网关为:" + gateway)
                        break
    except Exception as e:
        print(u"抱歉，程序出错")
        print(e)
    return result1,networkline,ip,gateway
#返回pingipdic为一个dict,key为ip，value为描述，对应的批量ping函数为ping_hosts
def genepingaskey(resulttxt,ip,gateway,networkline):
    pingipdic = {'127.0.0.1': '本机回环地址127.0.0.1'}
    hintlist =[]
    if resulttxt == []:
        #print("您的以太网网卡可能被禁用，未获取到以太网网卡信息")
        hintlist.append("您的网卡可能被禁用，不能网络配置信息")
    else:
        if networkline:
            if ip == '':
                #print("未获取到以太网IP地址，请确认IP地址是否配置")
                hintlist.append("IP地址未配置")
            # else:
            #     pingipdic[ip] = '本机IP地址%s' % ip
            if gateway == '':
                #print("未获取到以太网网关地址，请确认网关地址是否配置")
                hintlist.append("不能获取网关地址，网关地址未配置")
            else:
                pingipdic[gateway] = '网关地址%s' % gateway
                pingipdic['10.217.2.200'] = '门户网站地址10.217.2.200'
        else:
            hintlist.append('网络连接已断开,您的网线可能未插好')
    return hintlist,pingipdic
#返回pingipdic为一个dict,key为标识，value为ip,对应批量ping的函数为ping_hostlist
def genepingasvalue(resulttxt,ip,gateway,networkline):
    pingipdic = {'localhost': '127.0.0.1'}
    hintlist =[]
    if resulttxt == []:
        #print("您的以太网网卡可能被禁用，未获取到以太网网卡信息")
        hintlist.append("您的网卡可能被禁用，不能网络配置信息")
    else:
        if networkline:
            if ip == '':
                #print("未获取到以太网IP地址，请确认IP地址是否配置")
                hintlist.append("IP地址未配置")
            # else:
            #     pingipdic[ip] = '本机IP地址%s' % ip
            if gateway == '':
                #print("未获取到以太网网关地址，请确认网关地址是否配置")
                hintlist.append("不能获取网关地址，网关地址未配置")
            else:
                pingipdic['gateway'] = gateway
                pingipdic['MH'] = '10.217.2.200'
        else:
            hintlist.append('网络连接已断开,您的网线可能未插好')
    return hintlist,pingipdic
def printlist(list):
    for i in list:
        print(i)

def getdlpage():
    with open('xtlm2.html','r', encoding='utf-8') as f:
        html=u''+f.read()
    return html

if __name__=='__main__':
    resulttxt,networkline,ip,gateway,=get_network_config()
    if(len(resulttxt)!=0):
        print("本机网络配置：")
        printlist(resulttxt)
    ip = ip.replace('(首选)', '')
    hintlist,pingiplist=genepingaskey(resulttxt,ip,gateway,networkline)
    if len(hintlist)>0:
        print("\n异常提示信息：")
        printlist(hintlist)
    else:
        print("\n进行网络连通性测试：")
        #pool=ThreadPool(processes=12)
        #ping_result=pool.map(ping_host,pingiplist)
        ping_result=ping_hosts(pingiplist)
        print(ping_result)
    # testip=input("\n输入您想要ping测试的IP地址:")
    # print(ping_host(testip))



