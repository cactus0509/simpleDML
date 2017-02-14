# simpleDML

这是一个非常简单的DML工具，使用了web.py框架。
使用方法：

1. 安装 web.py 
   # pip install web.py
2. 安装python模块 ：  MySQLdb  DBUtils
    # pip2.7 install DBUtils
    # pip2.7 install MySQL-python

3. 修改数据库连接池，要维护的表。

   # vi admin.py
   
    
   
   3.1 数据库连接池部分 
   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
        if DBPool.__pool is None:  
            DBPool.__pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,  
                              host="192.168.4.202" , port=3306, user="no1" , passwd="password",  
                              db="no1",use_unicode=False,charset="utf8",cursorclass=DictCursor,setsession=['SET AUTOCOMMIT=1'])  
        connect = DBPool.__pool.connection()
        connect.autocommit = 1
        print connect
        return connect  
   
   
   3.2  表维护部分：
  
 
 5. 启动 功能页面
  # python admin.py 

6.打开浏览器访问:
   http://localhost:8080
   
    
 
 