# coding=utf-8
import os
import sys
import subprocess
result2=[]
def write_File(filename,result,mode):
    with open(filename,mode) as f:
        f.writelines(result)
def ping_hosts(ipaddrs):
    result_list=[]
    if sys.platform.startswith('win'):
        for key,value in ipaddrs.items():
            allRe = subprocess.Popen("ping -n 2 %s" %str(key), shell=True, stdout=subprocess.PIPE)
            lines = allRe.stdout.read().decode('gbk')
            if  u'100% 丢失' in lines or u'无法访问目标主机' in lines:
                #print('%s is down' % ip)
                result_list.append('本机ping %s不通'%value)
            else:
                #print('%s is up' % ip)
                result_list.append('本机ping %s可通'%value)
    return result_list
def ping_host(ip):
    if sys.platform.startswith('win'):
        allRe = subprocess.Popen("ping -n 1 %s" %str(ip), shell=True, stdout=subprocess.PIPE)
        lines = allRe.stdout.read().decode('gbk')
        if  u'100% 丢失' in lines or u'无法访问目标主机' in lines:
            print('本机ping %s不通'%ip)
            stat = '本机ping %s不通'%ip
        else:
            print('本机ping %s可通'%ip)
            stat = '本机ping %s可通'%ip
    return stat

def ping_host(ip):
    if sys.platform.startswith('win'):
        allRe = subprocess.Popen("ping -n 1 %s" %str(ip), shell=True, stdout=subprocess.PIPE)
        lines = allRe.stdout.read().decode('gbk')
        if  u'100% 丢失' in lines or u'无法访问目标主机' in lines:
            print('本机ping %s不通'%ip)
            stat = '本机ping %s不通'%ip
        else:
            print('本机ping %s可通'%ip)
            stat = '本机ping %s可通'%ip
    return stat

def get_mac_address():
    '''
    @summary: return the MAC address of the computer
    '''
    result1 = []
    gateway=''
    flag=0
    try:
        if sys.platform.startswith('win'):
            allRe=subprocess.Popen("ipconfig /all", shell=True, stdout=subprocess.PIPE)
            lines=allRe.stdout.readlines()
            for line in lines:
                line=line.lstrip().decode('gbk')
                result2.append(line)
                if u'无线' in line or u'蓝牙'in line or '隧道' in line:
                    flag=0
                    continue
                elif u'以太网适配器 以太网' in line or u'以太网适配器 本地连接' in line:
                    result1.append(line)
                    print(line)
                    flag=1
                if flag==1 and line.lstrip().startswith('物理地址'):
                     mac = line.split(":")[1].strip()
                     print(u"物理地址（MAC）为:" + mac)
                     result1.append(u"物理地址（MAC）为:" + mac+"\n")
                if flag==1 and line.lstrip().startswith('IPv4 地址'):
                    ip = line.split(":")[1].strip()
                    print(u"IP为:" +ip)
                    result1.append(u"IP地址为:" +ip+"\n")
                if flag == 1 and line.lstrip().startswith('子网掩码'):
                    mask = line.split(":")[1].strip()
                    print(u"子网掩码为:" + mask)
                    result1.append(u"子网掩码为:" + mask+"\n")
                if flag == 1 and line.lstrip().startswith('默认网关'):
                    gateway = line.split(":")[1].strip()
                    print(u"默认网关为:" + gateway)
                    result1.append(u"默认网关为:" + gateway+"\n")
                    break
    except Exception as e:
        print(u"抱歉，程序出错")
        print(e)
        return None
    return result1,gateway


if __name__=='__main__':
    resulttxt,gateway=get_mac_address()
    if resulttxt==[]:
        print("您的以太网网卡可被禁用，为获取到以太网网卡信息")
    elif gateway=='':
        print("未获取到网关地址，请确认网关地址是否配置")
    else:
        print(resulttxt)
    write_File("result.txt", resulttxt,'w')
    #os.system(r'result.txt')
    if(gateway!=''):
        iplist={'127.0.0.1':'本机回环地址',gateway:'网关地址','10.217.2.200':'门户网站'}
        ping_result=ping_hosts(iplist)
    print(ping_result)

