# simpleDML

这是一个非常简单的DML工具，使用了web.py框架。
使用方法：

1. 安装 web.py 
   # pip install web.py
2. 安装python模块 ：  MySQLdb  DBUtils
    >  # pip2.7 install DBUtils  <br>
    >  # pip2.7 install MySQL-python <br>

3. 修改数据库连接池，要维护的表。

   # vi admin.py
   
    
   
   3.1 数据库连接池部分 
   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
        if DBPool.__pool is None:  <br>
            DBPool.__pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,  <br>
                              host="192.168.4.202" , port=3306, user="no1" , passwd="password",  <br>
                              db="no1",use_unicode=False,charset="utf8",cursorclass=DictCursor,setsession=['SET AUTOCOMMIT=1']) <br> 
        connect = DBPool.__pool.connection()<br>
        connect.autocommit = 1<br>
        print connect<br>
        return connect  <br>
   
   
   3.2  表维护部分：
init_tables=[<br>
 {<br>
    "table_name": "t_yhk_words",  #表名<br>
    "table_name_cn": "每日习语",  #表的中文名称<br>
    "dml":{<br>
            "insert":True,   #是否启用增加表数据功能。<br>
            "delete":True,    #是否有删除数据功能。<br>
            "update":True,   #是否有修改数据功能。<br>
            "query":True     #是否有查询数据功能。<br>
    },
    "primary_key": "id",     # 表的主键，  这个一定要有。 而且只能是一个主键。<br>
    "sort":" order by id desc ",  # 查询列表的排序规则。 使用标准SQL语法<br>
    "structure": [   #表结构描述， 只需要列出必要的insert,update甬到的字段。<br>
                     { "column":"id", "type":"int","column_cn":"ID" , "size":10, "show": True ,"search":True  },   # show 表示数据在table显示时，是否显示该列。比如content字段太长，没有必要显示，就可以设置为show:False,<br>
                     { "column":"post_date", "type":"date","size":20, "column_cn":"日期","show": True,"insert":True },    # insert, 表示在插入数据功能页上该字段是否出现在form表单里。<br>
                     { "column":"title", "type":"varchar","size":80, "column_cn":"标题","show": True ,"search":True,"insert":True},  <br>                    
                     { "column":"content", "type":"textarea","rows":"20", "cols":"120", "column_cn":"内容","show": False ,"insert":True}<br><br>
                ]<br>
 }, <br>
 {}, --- 其他表<br>
 ]<br>
 
 
 5. 启动 功能页面
  # python admin.py 

6.打开浏览器访问:
   http://localhost:8080
   
    
 
 
