from datetime import datetime
import pymysql as pymysql
from flask import app, request, render_template, current_app, g, Flask, jsonify

# 创建数据库
DBHOST = '127.0.0.1'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'todolist127135'
DBTYPE = 'utf8'

try:
    todolist001 = pymysql.connect(
        host='127.0.0.1',
        user="root",
        password="123456"
    )
    # 创建表格
    mycursor = todolist001.cursor()
    # mycursor.execute('DROP DATABASE IF EXISTS todolist127135')
    mycursor.execute("CREATE DATABASE IF NOT EXISTS todolist127135")

    db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME, charset=DBTYPE)
    print('数据库todolist127135连接成功')
    cur = db.cursor()
    # cur.execute('DROP TABLE IF EXISTS TODOLIST')
    sql = '''
    CREATE TABLE IF NOT EXISTS TODOLIST(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1000),
    content VARCHAR(1000),
    completionstatus VARCHAR(1000),
    addingtime TIMESTAMP,
    deadline INT)'''

    cur.execute(sql)
    print('TODOLIST表格创建成功')
    cur.close()
except pymysql.Error as e:
    print('TODOLIST表格创建失败：' + str(e))
# 初始化
app = Flask(__name__)
app.secret_key = "123456"

db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME, charset=DBTYPE)


# 设置向表格插入数据的函数
def insert_db(title, content, completionstatus, addingtime, deadline):
    cursor = db.cursor()
    todolist_sql = "INSERT INTO `TODOLIST` (`title`, `content`, `completionstatus`, `addingtime`, `deadline`) VALUES(" \
                   "%s, %s, %s, %s, %s); "
    cursor.execute(todolist_sql, (title, content, completionstatus, addingtime, deadline))
    db.commit()


# 增：新增待办事项，输入格式如下：
# "标题":"666",
# "内容":"我",
# "截止时间":20231223，
# 其中用户输入的截止时间为八位整数即可，如20230112，后台会自动转化为相应的日期
@app.route('/add', methods=['POST'])  # 这里要get方法吗
def add():
    try:
        task_json = request.get_json()  # 获取json数据
        print(task_json)
        get_title = task_json.get("标题")
        get_content = task_json.get("内容")
        get_completionstatus = "未完成"
        get_addingtime = datetime.now()  # 这里的时间戳的格式要注意一下 好像有问题
        get_deadline = task_json.get("截止时间")
        if not all([get_title, get_content, get_completionstatus, get_addingtime, get_deadline]):
            return jsonify(msg="您的信息录入不完全，请检查")
        insert_db(get_title, get_content, get_completionstatus, get_addingtime, get_deadline)
        data1 = {"title": get_title, "content": get_content, "completionstatus": get_completionstatus,
                 "addingtime": get_addingtime, "deadline": get_deadline}
        return jsonify(code=200, msg="success", data=data1)
    except Exception as e:
        print(e)
        # return jsonify(msg="出错了！请查看是否正确访问！")
        return jsonify(code=404, msg="该活动不存在")


# 删除所有事项
@app.route('/delete/alltask', methods=['DELETE'])
def delete_all():
    cursor = db.cursor()
    sql_delete_all = "DELETE FROM TODOLIST"
    cursor.execute(sql_delete_all)
    db.commit()
    # return jsonify(msg="已删除所有待办事项")
    return jsonify(code=200, msg="success")


# 删除某条指定id的任务
@app.route('/delete/<number>', methods=['DELETE'])  # 我有点疑惑这里的方法
def delete_onepiece(number):
    cursor = db.cursor()
    sql_delete_onepiece = "DELETE FROM TODOLIST where id = %r"  # 我不知道为啥%d不行，%s也不行，但是%r就可以跑了...
    id1 = int(number)
    cursor.execute(sql_delete_onepiece, id1)
    db.commit()
    # return jsonify(msg=f"id为{number}的任务已经删除")
    return jsonify(code=200, msg="success")


# 删除所有未完成任务
@app.route('/delete/allundone', methods=['DELETE'])  # 我有点疑惑这里的方法
def delete_allundone():
    cursor = db.cursor()
    sql_delete_allundone = "DELETE FROM TODOLIST WHERE  completionstatus = %s"
    status = "未完成"
    cursor.execute(sql_delete_allundone, status)
    db.commit()
    # return jsonify(msg="所有未完成事项已删除")
    return jsonify(code=200, msg="success")


# 删除所有已完成任务
@app.route('/delete/alldone', methods=['DELETE'])  # 我有点疑惑这里的方法
def delete_alldone():
    cursor = db.cursor()
    sql_delete_alldone = "DELETE FROM TODOLIST WHERE  completionstatus = %s"
    status = "已完成"
    cursor.execute(sql_delete_alldone, status)
    db.commit()
    # return jsonify(msg="所有已完成事项已删除")
    return jsonify(code=200, msg="success")


# 查看所有事项
@app.route('/search/alltask', methods=['GET'])
def search_all_task():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM  TODOLIST")
    all_result = cursor.fetchall()
    return jsonify(ode=200, msg="success", data=all_result)
    # for x in all_result:
    # print(x)


# 查看指定id的事项
@app.route('/search/<number>', methods=['GET'])  # 我有点疑惑这里的方法
def search_id(number):
    cursor = db.cursor()
    sql_search_onepiece = "SELECT * FROM TODOLIST where id = %r"  # 我不知道为啥%d不行，%s也不行，但是%r就可以跑了...
    id1 = int(number)
    cursor.execute(sql_search_onepiece, id1)
    myresult = cursor.fetchall()
    return jsonify(code=200, msg="success", data=myresult)


# 查看所有未完成任务
@app.route('/search/allundone', methods=['GET'])  # 我有点疑惑这里的方法
def search_allundone():
    cursor = db.cursor()
    sql_search_allundone = "SELECT * FROM TODOLIST WHERE  completionstatus = %s"
    status = "未完成"
    cursor.execute(sql_search_allundone, status)
    myresult = cursor.fetchall()
    return jsonify(ode=200, msg="success", data=myresult)


# 查看所有已完成任务
@app.route('/search/alldone', methods=['GET'])  # 我有点疑惑这里的方法
def search_alldone():
    cursor = db.cursor()
    sql_search_alldone = "SELECT * FROM TODOLIST WHERE  completionstatus = %s"
    status = "已完成"
    cursor.execute(sql_search_alldone, status)
    myresult = cursor.fetchall()
    return jsonify(ode=200, msg="success", data=myresult)


# 输入关键字查询事项(一直出错）
@app.route('/search/onepiece', methods=['GET'])  # 我有点疑惑这里的方法
def search_onepiece():
    try:
        task_json = request.get_json()
        get_keywords = task_json.get("关键词")
        # keywords = f"{get_keywords}"
        cursor = db.cursor()
        sql_search_onepiece1 = "SELECT * FROM TODOLIST WHERE title LIKE '%%%s%%'" % get_keywords
        cursor.execute(sql_search_onepiece1)
        myresult1 = cursor.fetchall()
        sql_search_onepiece2 = "SELECT * FROM TODOLIST WHERE content LIKE '%%%s%%'" % get_keywords
        cursor.execute(sql_search_onepiece2)
        myresult2 = cursor.fetchall()
        return jsonify(ode=200, msg="success", data=(myresult1, myresult2))


    except Exception as e:
        print(e)
        # return jsonify(msg="出错了！请查看是否正确访问！")
        return jsonify(code=404, msg="该活动不存在")


# 将指定id的未完成任务更改为已完成任务
@app.route('/update/done/<number>', methods=['PUT'])  # 我有点疑惑这里的方法
def update_onedone(number):
    try:
        cursor = db.cursor()
        sql_update_done = "UPDATE TODOLIST SET completionstatus = '已完成' where id = %s"
        id1 = int(number)
        cursor.execute(sql_update_done, id1)
        myresult = cursor.fetchall()
        db.commit()
        # return jsonify(msg="修改成功")
        return jsonify(ode=200, msg="success")
    except Exception as e:
        print(e)
        # return jsonify(msg="请检查是否正确操作")
        return jsonify(code=404, msg="该活动不存在")


# 将指定id的已完成任务更改为未完成任务
@app.route('/update/undone/<number>', methods=['PUT'])  # 我有点疑惑这里的方法
def update_oneundone(number):
    try:
        cursor = db.cursor()
        sql_update_undone = "UPDATE TODOLIST SET completionstatus = '未完成' where id = %s"
        id1 = int(number)
        cursor.execute(sql_update_undone, id1)
        myresult = cursor.fetchall()
        db.commit()
        # return jsonify(msg="修改成功")
        return jsonify(ode=200, msg="success")
    except Exception as e:
        print(e)
        # return jsonify(msg="请检查是否正确操作")
        return jsonify(code=404, msg="该活动不存在")


# 将所有的未完成任务更改为已完成任务
@app.route('/update/alldone', methods=['PUT'])  # 我有点疑惑这里的方法
def update_alldone():
    try:
        cursor = db.cursor()
        sql_update_alldone = "UPDATE TODOLIST SET completionstatus = REPLACE(completionstatus,'未完成','已完成') where " \
                             "completionstatus = '未完成' "
        cursor.execute(sql_update_alldone)
        myresult = cursor.fetchall()
        db.commit()
        # return jsonify(msg="修改成功")
        return jsonify(ode=200, msg="success")
    except Exception as e:
        print(e)
        # return jsonify(msg="请检查是否正确操作")
        return jsonify(code=404, msg="该活动不存在")


# 将所有的已完成任务更改为未完成任务
@app.route('/update/allundone', methods=['PUT'])  # 我有点疑惑这里的方法
def update_allundone():
    try:
        cursor = db.cursor()
        sql_update_allundone = "UPDATE TODOLIST SET completionstatus = REPLACE(completionstatus,'已完成','未完成') where " \
                               "completionstatus = '已完成' "
        cursor.execute(sql_update_allundone)
        myresult = cursor.fetchall()
        db.commit()
        # return jsonify(msg="修改成功")
        return jsonify(ode=200, msg="success")
    except Exception as e:
        print(e)
        # return jsonify(msg="请检查是否正确操作")
        return jsonify(code=404, msg="该活动不存在")


app.run()
