import pymysql

def datab():
	# db=pymysql.connect(host="192.168.137.1",port=3306,user="niu",passwd="hanshu123??",db="carset",charset='utf8'  )
	db=pymysql.connect("127.0.0.1","root","Mysql_991121","carset",charset='utf8' )
	
	return db