import mysql.connector
import pandas as pd
sqlproxy = "select ip from proxy_ip1_text "
sqlgongkong = 'select ip from all_ics_data '
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
            # print first
            # first = row.replace(' ','')
            new.append(first)
    # print new
    return new


# print type(new[0])


def cos(vector1,vector2):
    dot_product = 0.0;
    normA = 0.0;
    normB = 0.0;
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)

def ver(s):
    dict1 = {}
    for i in range(1,126):
        dict1[i] = s.count(i)
    print ('ver done')
    return tuple(dict1.values())



def ipsplit3(ip):
    s1 =''
    ipdiv = ip.split('.')
    s1 = "".join(ipdiv[0] )+'.'+ "".join(ipdiv[1] )
    # print s1
    return s1

def getdict():
    # gkip = getip(sqlgongkong)
    proxyip = getip(sqlproxy)
    dict1 = {}
    for i in proxyip:
        s2 = ipsplit3(i)
        if int(s2.split('.')[0])<233:
            dict1[s2] = 0
    # print dict1
    return dict1

def compare(dict2):
    gkip = getip(sqlgongkong)
    # proxyip = getip(sqlproxy)
    for ip in gkip:
        s2 = ipsplit3(ip)
        # print s2
    # l1 = [u'1.179.156', u'1.179.174', u'1.174.182', u'1.1.182', u'1.119.193', u'1.0.186', u'1.0.184', u'1.175.134', u'1.179.146', u'1.0.180']
    # for s2 in l1:
        if s2 in dict2:
            temp =  int(dict2[s2] )
            temp += 1
            dict2[s2] = temp
    # print dict2
    # print sorted(dict2.keys())
    # l2 = (sorted(dict2.items(), key=lambda item: item[0]))

    # print l2
    # print  key, dict[key] for key in sorted(dict.keys())

    x = []
    y = []
    for key in dict2:
        x.append(key)
        y.append(dict2[key])
    print (x)
    print (y)
    return dict2

def writeRecord(record):
    fp  = open("txt1.txt", 'w+')
    fp.writelines(str(record))
    fp.close()
    print "updata record"

# totle = []
# cishu = 0
# for i in l2:
#
#     if 0<int(i[0].split('.')[0])<126:
#         cishu  += i[1]
#         totle.append(i[1])
# # print totle
# print len(totle)
# print cishu
# for i in range(1,11):
#     print i,totle.count(i)

l1 = compare(getdict())
# writeRecord(l1)
# for i in l1:
#     # if l1[i][1]>10:
#         print l1[i]
# dict2 = {u'1.179.174.2': '', u'1.0.180.122': '', u'1.179.156.233': '', u'1.0.184.23': '', u'1.119.193.36': '', u'1.179.146.153': '', u'1.174.182.63': '', u'1.175.134.99': '', u'1.0.186.14': '', u'1.1.182.3': ''}