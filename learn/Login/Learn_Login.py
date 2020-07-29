import pymysql
db = pymysql.connect('localhost', 'root', '', 'bili_search')
cmd = db.cursor()
cmd.execute('delete from test')
db.commit()
db.close()