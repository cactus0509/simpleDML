# simpleDML
# 什么时候使用该工具
当你需要制作一个表数据维护功能页面时，
1）你不想重复劳动时(例如java,你可能想从以前的项目中copy一份对表的增、删、改功能页面)，
2）你又不想提供给业务人员（不能让他使用navicat）工具时。
3）你自己有个项目，比如里面有多个系统配置表时。
4）界面需要有简单的增\删\改\查询 功能，可以使用这个工具。

这个工具，只需要配置一下数据库连接信息，表名，表字段，就可以拥有简单的增删改功能了。
开发。运维，dba应该都碰到过这些不痛不痒的问题。



使用方法：

## 1. 安装 web.py 
    >  # pip install web.py
## 2. 安装python模块 ：  MySQLdb  DBUtils
    >  # pip2.7 install DBUtils  <br>
    >  # pip2.7 install MySQL-python <br>

##  3. 修改数据库连接池，要维护的表。
### 3.1 准备数据。
```
MySQL [demo]> create database fly;

MySQL [demo]> create table fly ( id int not null primary key AUTO_INCREMENT, fly_from varchar(32),fly_to varchar(32),price int, flight_no varchar(32) , time varchar(32) ); 

insert into fly (fly_from,fly_to，flight_no,price,time ) values ('金昌','北京','KN5656',1338,'2017-02-14');
insert into fly (fly_from,fly_to,flight_no,price,time ) values ('呼和浩特','北京','KN2262',1198,'2017-02-14');
insert into fly (fly_from,fly_to,flight_no,price,time ) values ('长治','北京','KN2928',1658,'2017-02-14');
insert into fly (fly_from,fly_to,flight_no,price,time ) values ('安顺','北京','KN5226',1388,'2017-02-14');
insert into fly (fly_from,fly_to,flight_no,price,time) values ('襄阳','北京','KN5812',898,'2017-02-14');
```
   
### 3.2 编辑 demo.py ， 数据库连接池部分 
   ```
     if DBPool.__pool is None:  
         DBPool.__pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 , 
                           host="192.168.4.202" , port=3306, user="no1" , passwd="password", 
                                db="no1",use_unicode=False,charset="utf8",cursorclass=DictCursor,setsession=['SET AUTOCOMMIT=1']) 
         connect = DBPool.__pool.connection()
         connect.autocommit = 1
         print connect
         return connect 

  ```
   
### 3.3 编辑 admin.py ， 表维护部分：
 ```
init_tables=[
 {
    "table_name": "fly",  #表名
    "table_name_cn": "每日习语",  #表的中文名称
    "dml":{
            "insert":True,   #是否启用增加表数据功能。
            "delete":True,    #是否有删除数据功能。
            "update":True,   #是否有修改数据功能。
            "query":True     #是否有查询数据功能。
    },
    "primary_key": "id",     # 表的主键，  这个一定要有。 而且只能是一个主键。
    "sort":" order by id desc ",  # 查询列表的排序规则。 使用标准SQL语法
    "structure": [   #表结构描述， 只需要列出必要的insert,update用到的字段。
                     { "column":"id", "type":"int","column_cn":"ID" , "size":10, "show": True ,"search":True  },   # show 表示数据在table显示时，是否显示该列。比如content字段太长，没有必要显示，就可以设置为show:False,
                     { "column":"fly_from", "type":"varchar","column_cn":"出发地","show": True,"insert":True },    # insert, 表示在插入数据功能页上该字段是否出现在form表单里。
                     { "column":"fly_to", "type":"varchar", "column_cn":"目的地","show": True ,"search":True,"insert":True},                      
                     { "column":"price", "type":"int","column_cn":"价格","show": True ,"insert":True, },
                     { "column":"flight_no", "type":"varchar","rows":"20", "cols":"120","show": True , "column_cn":"航班号","show": True ,"insert":True, },
                     { "column":"time", "type":"varchar", "column_cn":"离港时间","show": True ,"insert":True, }
                ]
 }, 
 {}, --- 其他表
 ]
 ```
 
 
 
## 4. 启动 功能页面
  > python demo.py 

## 5.打开浏览器访问:
   http://localhost:8080
   
   <img src="http://myblog.mysqloracle.com/index.png">
   <img src="http://myblog.mysqloracle.com/update.png">
   
    
 
 

