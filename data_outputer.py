# coding:utf8
import MySQLdb


class HtmlOutputer(object):

    # 初始化数据列表
    def __init__(self):
        self.datas = []

    # 收集获得的数据到数据列表
    # @param data 收集到的数据元
    # @return

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # 以网页形式输出数据

    def output_html(self):
        fout = open('output.html', 'w')

        fout.write("<html><meta charset=\"utf-8\" />")
        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data[''])
            fout.write("<td>%s</td>" % data[''].encode('utf-8'))
            fout.write("<td>%s</td>" % data[''].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()

    # 链接数据库

    def database_connect(self):
        try:
            # 获得连接对象
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test',charset="utf8")
            # 得到连接的游标对象
            self.cur = self.conn.cursor()
            print "Mysql connect success!"
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])

    # 数据库查询操作

    def database_set_charset(self,db_name):
        try:
            self.conn.select_db(db_name)
            # count = self.cur.execute('select * from `oecss_student`')
            # print 'there has %s rows record' % count
            print "DB change success!"
            self.cur.execute("SET NAMES utf8")
            self.cur.execute("SET CHARACTER_SET_CLIENT=utf8")
            self.cur.execute("SET CHARACTER_SET_RESULTS=utf8")
            self.conn.commit()
            print "CHARSET FIXED"
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 数据库表创建操作

    def database_create(self):
        try:
            self.conn.select_db('python')
            sql = "CREATE TABLE IF NOT EXISTS `` "
            self.cur.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS ``"
            print "TABLE READY"
            self.cur.execute(sql)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 数据库写操作

    def database_insert(self,sql):
        try:
            self.cur.execute(sql)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 数据库读（全部）操作
    def database_read(self,table="`python_school`"):
        try:
            sql = "SELECT * FROM " + table
            res = self.cur.execute(sql)
            return self.cur.fetchall()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # sql提交

    def sql_commit(self):
        try:
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

