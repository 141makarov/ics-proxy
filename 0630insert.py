# coding=utf-8
# 提取代理IP分成网段，拆成只有前三个字节，插入数据库
import mysql.connector
import threading
import time
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mydata',
          'charset': 'utf8'}

sql_insertq = "insert into proxy_ics_realation(proxy_ip,three_char,network_segment)values( %(ip)s,%(three_char)s,%(net_segment)s)"
sql_updataics_ip = "update proxy_ics_realation set ics_ip = %s ,ics_ip_count = %s where three_char = %s"
sqlproxy = "select ip from proxy_ip1_text "
sqlgongkong = 'select ip from all_ics_data '
sqlthreechar = 'select three_char from proxy_ics_realation where step50 is null '
sql_updata_step = "update proxy_ics_realation set step50 = %s where three_char = %s"
def insertMysql(sql,list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql, list)
    cur.close()
    conn.commit()
    conn.close()

def getip(s):
    config={'host':'127.0.0.1',
            'user':'root',
            'password':'123456',
            'port':3306 ,
            'database':'mydata',
            'charset':'utf8'}
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(s)
    results = cur.fetchall()
    new = []
    for row in results:
            row = "".join(row)
            first = row.replace(' ','')
            new.append(first)
    # print new
    return new

def ipsplit3(ip):
    s1 =''
    ipdiv = ip.split('.')
    s1 = "".join(ipdiv[0] )+'.'+  "".join(ipdiv[1] )+'.'+"".join(ipdiv[2])
    # print s1
    return s1

def net_seg(ip):
    s1 = ''
    ipdiv = ip.split('.')
    if int(ipdiv[0])<128:
        return 'A'
    if 128<int(ipdiv[0]) < 192:
        return 'B'
    if 192<int(ipdiv[0]) < 224:
        return 'C'
    else:
        print 'worng ip:',ip

def dealproxyip():
    ip_list = getip(sqlproxy)
    for ip in ip_list:

        dict1 = {'ip':'','net_segment':'','three_char':''}
        threec_char = ipsplit3(ip)
        net_segment = net_seg(ip)
        dict1['ip'] = str(ip)
        dict1['three_char'] = str(threec_char)
        dict1['net_segment'] = str(net_segment)
        print dict1
        insertMysql(sql_insertq,dict1)

def getthreechardict():
    dictthreechar = {}
    threecharlist = getip(sqlthreechar)
    for tc in threecharlist:
        dictthreechar[tc] = ''
    return dictthreechar

def dealicsip():# 将代理IP，网段，前三位插入数据库
    ip_list = getip(sqlproxy)
    dictthreechar = getthreechardict()
    for ip in ip_list:
        ip3 = ipsplit3(ip)
        if dictthreechar.has_key(ip3):
            temp = dictthreechar[ip3]
            temp += str(ip)
            dictthreechar[ip3] = temp
        else:
            dictthreechar[ip3] = ip
    insertMysql(dictthreechar)

def getkeydict():
    threelist = getip(sqlthreechar)
    dict1 = {}
    for three in threelist:
        dict1[three] = ''
    # print dict1
    print 'keydict done'
    return dict1

def getcountdict():
    threelist = getip(sqlthreechar)
    dict1 = {}
    for three in threelist:
        dict1[three] = 0
    print 'countdict done'
    return dict1

def camparedict(keydict ,list1,countdict):
    for ip in list1:
        threeip  = ipsplit3(ip)
        if keydict.has_key(threeip):
            temp = keydict[threeip]
            temp += '/'+ip
            keydict[threeip] = temp
            count = countdict[threeip]
            count +=1
            countdict[threeip] = count
    # print keydict
    # print countdict
    for key in keydict:
        threechar = tuple({str(key)})
        ics =tuple({ keydict[key]})
        count =tuple({countdict[key]})
    # print (threechar)
        s = ics +count +threechar
        print s
        insertMysql(sql_updataics_ip,s)

# porxyip = '192.168.3'
# gkip ='192.168.1'
global different
different = 50
def granularity(porxyip,gkip):
    global different
    # print porxyip
    # print gkip
    proxy = int(porxyip.split('.')[-1])
    gk = int(gkip.split('.')[-1])
    if int(porxyip.split('.')[0]) == int(gkip.split('.')[0]) and int(porxyip.split('.')[1]) == int(gkip.split('.')[1]):
        # print proxy - different
        if proxy - different <= gk <= proxy + different:
        # if proxy - different == gk or proxy + different == gk:
        #     print 1
            return True

# granularity(porxyip,gkip)

# keydict = getkeydict()
# countdict = getcountdict()
# gkip = getip(sqlgongkong)
# camparedict(keydict,gkip,countdict)

def thread(list1):
    threads = []
    for i in range(0, 20):
        threads.append(threading.Thread(target=judge_granularity, args=(list1[i * len(list1) / 20:(i + 1) * len(list1) / 20])))
    for i in threads:
        i.start()
        time.sleep(2)
    for i in threads:
        i.join()
        time.sleep(2)

def judge_granularity():
    # three_char = list(t)
    three_char = list(set(getip(sqlthreechar)))
    gkiplist = getip(sqlgongkong)
    while three_char:
        ip = three_char.pop()
        print len(three_char)
    # for ip in three_char:
        str1 = ''
        for gkip in gkiplist:
            three_gkip = ipsplit3(gkip)
            if granularity(ip,three_gkip):
                str1 += '/'+ str(gkip)
            else:continue
        ip =tuple({ip})
        str1 = tuple({str1})
        print ip
        print str1
        insertMysql(sql_updata_step, str1+ip)

# three_char = getip(sqlthreechar)
# thread(three_char)
judge_granularity()


