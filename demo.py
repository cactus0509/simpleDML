#!/usr/bin/env python 
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web
import MySQLdb  
from MySQLdb.cursors import DictCursor  
from DBUtils.PooledDB import PooledDB  

render = web.template.render('templates') 
"""
create table fly ( id int not null primary key AUTO_INCREMENT, fly_from varchar(32),fly_to varchar(32),price int, flight_no varchar(32) , time varchar(32) ); 

"""
init_tables=[
 {
    "table_name": "fly",
    "table_name_cn": "航班信息",
    "dml":{
            "insert":True,
            "delete":True,
            "update":True,
            "query":True
    },
    "primary_key": "id",
    "sort":" order by id desc ",
    "structure": [
                     { "column":"id", "type":"int","column_cn":"ID" , "size":10, "show": True ,"search":True  },
                     { "column":"fly_from", "type":"varchar","column_cn":"出发地","show": True,"insert":True },
                     { "column":"fly_to", "type":"varchar", "column_cn":"目的地","show": True ,"search":True,"insert":True},                      
                     { "column":"price", "type":"int","column_cn":"价格","show": True ,"insert":True, },
                     { "column":"flight_no", "type":"varchar","rows":"20", "cols":"120","show": True , "column_cn":"航班号","show": True ,"insert":True, },
                     { "column":"time", "type":"varchar", "column_cn":"离港时间","show": True ,"insert":True, },
                ]
 },         
]
 
urls = (        
  '/', 'index',
  '/table','TABLE',
  '/search','SEARCH',
  '/insert','INSERT',
  '/edit','EDIT',
  '/delete','DELETE',
  '/getone','GETONE'
)

class DBPool(object):   
    #连接池对象  
    __pool = None   
    @staticmethod  
    def getConn():  
        """ 
        @summary: 静态方法，从连接池中取出连接 
        @return MySQLdb.connection 
        """  
        
        if DBPool.__pool is None:  
            DBPool.__pool = PooledDB(creator=MySQLdb, mincached=1 , maxcached=20 ,  
                              host="192.168.4.202" , port=3306, user="fly" , passwd="fly",  
                              db="fly",use_unicode=False,charset="utf8",cursorclass=DictCursor,setsession=['SET AUTOCOMMIT=1'])  
        connect = DBPool.__pool.connection()
        connect.autocommit = 1
        print connect   
        return connect
     
    @staticmethod  
    def getCursor():
        return DBPool.getConn().cursor()
    
    
class DBMgr():
    page_count=100
    def getData(self,table_name,columns,page,sort=None,search_column=None):
        try:
            cursor = DBPool.getCursor()
            sql_columns=""
            
            for col in columns:
                sql_columns = sql_columns + col["column"]  + ","
            sql_columns = sql_columns + "1 "
            
            limit_from = page * self.page_count
            limit_to = self.page_count
            where = ""
            orderby=""
            if sort:
                orderby=sort
            
            if search_column:
                for line in search_column:
                    if line["value"]:
                        if line["type"] == "int":
                            where = where + " and " + line["column"] + " = " + line["value"]
                        if line["type"] in [ "textarea", "varchar" ]:
                            where = where + " and " + line["column"] + " like '%" + line["value"] + "%'"
                         
            
            sql =   " select " + sql_columns + " from "+ table_name   + " where 1 =1  " + where +  orderby + "  limit " + str(limit_from) + "," + str(limit_to)
            print sql
            cursor.execute(sql)
            rows=[]
            data= cursor.fetchall()
            
            for line in data:
                cells={}
                for column in columns:
                    cells[column["column"]] =  line[ column["column"] ]  
                rows.append(  cells  )  
             
            return rows
        
        except Exception,e:
            print e
            return None
        
    def getone(self,th_data,search_column):
        try:
            cursor = DBPool.getCursor()
            sql_columns=""
            print 3
            print  search_column
            for col in th_data:
                sql_columns = sql_columns + col["column"]  + "," 
            sql_columns = sql_columns + " 1 "
             
            primary_key = search_column["primary_key"]
            primary_key_value = search_column["primary_key_value"]
            where = " where " +  primary_key + " = '" + primary_key_value  + "'"
            table_name=search_column["table_name"] 
            sql =   " select " + sql_columns + " from "+ table_name   +  where + " limit 1 "
            print sql
            cursor.execute(sql)
            data = cursor.fetchone()
            
            for line in th_data:
                line["value"] =  data[ line["column"]  ]
                
            return th_data
        
        except Exception,e:
            print e
            return None
        
    def delete(self,table_name,delete_key,value):
        try:
            cursor = DBPool.getCursor() 
            sql =   " delete from " + table_name  + " where " + delete_key + " = '" + value + "'" 
            print sql
            cursor.execute(sql) 
        
        except Exception,e:
            print e
            return None
        
        
    def insert(self,table_name,editColumn):
        try:
            cursor = DBPool.getCursor()
            columns=[]
            values=[] 
            if editColumn:
                for line in editColumn: 
                    columns.append( line["column"]  )
                    values.append( "'" +  line["value"]  + "'") 
            
            print columns
            print values 
            sql =   """ insert into {0} ( {1} )  values  ( {2} )  """.format( table_name, ",".join(columns),",".join(values)  )
            print sql
            cursor.execute(sql) 
        
        except Exception,e:
            print e
            return None

    def update(self,table_name,editColumn,primary_column):
        try: 
            cursor = DBPool.getCursor()
            
            columns=[] 
            where= primary_column["primary_key"] + " = '" +   primary_column["primary_key_value"]  + "'"
            if editColumn:
                for line in editColumn: 
                    columns.append( line["column"]   + " ='" + line["value"]  + "'" )
            sql =   """ update  {0}  set  {1}  where {2} """.format( table_name, ",".join(columns),  where )
            print sql
            cursor.execute(sql) 
        
        except Exception,e:
            print e
            return None
        
        
dbMgr=DBMgr()
     
class index:
    def GET(self): 
        data=[]  
        for table in init_tables:
            data.append( table) 
        return render.main( data,None,None,None)

class TABLE:
    def GET(self): 
        input=web.input() 
        table_name_req=input.table_name
        data=[]
        th_data=[] 
        search_column={ "table_name": table_name_req, "data": [] } 
        sort=None
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["primary_key"] = table["primary_key"]
                search_column["dml"] = table["dml"]
                sort=table["sort"]
                structure = table["structure"]
                for row in structure:
                    if row["show"]:
                        th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                    if "search"in row and row["search"]:
                        search_column["data"].append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  ) 
                     
            data.append( table )
        
        #td
        page=0
        
        td_data = dbMgr.getData(table_name_req,th_data,page,sort)
        return render.main( data,th_data,td_data,search_column)


class DELETE:
    def GET(self): 
        input=web.input() 
        table_name_req=input.table_name
        data=[]
        th_data=[] 
        search_column={ "table_name": table_name_req, "data": [] } 
        sort=None
        delete_key=None
        delete_value=None
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["primary_key"] = table["primary_key"]
                search_column["dml"] = table["dml"]
                sort=table["sort"]
                structure = table["structure"]
                delete_key=table["primary_key"]
                delete_value=dict(input)[ delete_key  ]
                for row in structure:
                    if row["show"]:
                        th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                    if "search"in row and row["search"]:
                        search_column["data"].append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  ) 
                     
            data.append( table )
        
        #td
        page=0
        
        #delete 
        dbMgr.delete(table_name_req,delete_key,delete_value)
        
        td_data = dbMgr.getData(table_name_req,th_data,page,sort)
        raise web.seeother('/table?table_name=' + table_name_req )
    
    
class SEARCH:
    def POST(self): 
        input=dict(web.input())  
        table_name_req=input["table_name"] 
        print table_name_req
        
        data=[]
        th_data=[]
        td_data=[]
        whereColumn=[]
        sort=None
        
        search_column={ "table_name": table_name_req, "data": [  ] }
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["primary_key"] = table["primary_key"]
                search_column["dml"] = table["dml"]
                search_column["primary_key"] = table["primary_key"]
                sort  = table["sort"]
                structure = table["structure"]
                for row in structure:
                    if row["show"]:
                        th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                    if "search"in row and row["search"]:
                        search_column["data"].append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                        whereColumn.append(  { "column": row["column"] , "type":row["type"], "value":None   }   )
            
            data.append( table )
         
        for line in  whereColumn:
            value=input[ line["column"] ]
            if value:
                line["value"] = value
        
        print whereColumn
        #td
        page=0
         
        td_data = dbMgr.getData(table_name_req,th_data,page,sort,whereColumn)
        return render.main( data,th_data,td_data,search_column)
    
class INSERT:
    def GET(self): 
        input=web.input() 
        table_name_req=input.table_name
        action=input.action
        data=[]
        th_data=[]
        td_data=[]
        search_column={ "table_name": table_name_req, "data": [] } 
        
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["dml"] = table["dml"]
                search_column["primary_key"] = table["primary_key"]
                search_column["action"] = action
                
                structure = table["structure"]
                for row in structure: 
                    size=32
                    type="varchar"
                    rows="3"
                    cols="20"
                    if "size" in  row:
                        size=row["size"]
                        
                    if "type" in  row:
                        type=row["type"]
                    if "rows" in  row:
                        rows=row["rows"]
                    if "cols" in  row:
                        cols=row["cols"]
                    
                    th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"] ,"value":""  , "size": size, "type":type,"cols":cols,"rows":rows   }  )  
        
        #td 
        return render.table(th_data,search_column)
    

class GETONE:
    def GET(self): 
        input=web.input() 
        table_name_req=input.table_name
        action=input.action 
        th_data=[] 
        search_column={ "table_name": table_name_req, "data": [] }  
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["dml"] = table["dml"]
                search_column["primary_key"] = table["primary_key"]
                search_column["action"] = action
                search_column["primary_key_value"] = dict(input)[  table["primary_key"]   ] 
                 
                structure = table["structure"]
                for row in structure: 
                    size=32
                    type="varchar"
                    rows="3"
                    cols="20"
                    if "size" in  row:
                        size=row["size"]
                        
                    if "type" in  row:
                        type=row["type"]
                    if "rows" in  row:
                        rows=row["rows"]
                    if "cols" in  row:
                        cols=row["cols"]
                    
                    th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"] ,"value":""  , "size": size, "type":type,"cols":cols,"rows":rows   }  )  
        
        #td  
        th_data=dbMgr.getone(th_data,search_column)
 
        return render.table(th_data,search_column)


class EDIT:
    def POST(self): 
        input=dict(web.input())  
        table_name_req=input["table_name"]
        action=input["action"]
        data=[]
        th_data=[] 
        editColumn=[]

        primary_key=None
        primary_key_value=None
        
        search_column={ "table_name": table_name_req, "data": [  ] }
        primary_column={}
        
        #th
        for table in init_tables:
            if not th_data and table["table_name"] == table_name_req:
                search_column["table_name_cn"] = table["table_name_cn"]
                search_column["primary_key"] = table["primary_key"]
                search_column["dml"] = table["dml"]
                structure = table["structure"]
                primary_key=table["primary_key"]
                primary_key_value=dict(input)[ primary_key  ] 
                primary_column={"primary_key":primary_key,"primary_key_value":primary_key_value}               
                for row in structure:
                    if row["show"]:
                        th_data.append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                    if "search" in row and row["search"]:
                        search_column["data"].append( { "column" :   row["column"] , "column_cn" :   row["column_cn"]  }  )
                    if "insert" in row and row["insert"]:
                        html=False
                        if "html" in row:
                            html = row["html"] 
                        editColumn.append(  { "column": row["column"] , "type":row["type"], "value":None,"html":html  }   )
                            
            data.append( table )
         
        for line in  editColumn: 
            value=input[ line["column"] ] 
            _type= line["type"] 
            html= line["html"]
            if value and _type=="textarea":
                if html:
                    html_head="""
                    <?xml version="1.0" encoding="utf-8" ?> 
                    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN"> 
                    <head>  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8"/>  
                    <style> p{ text-indent:2em; text-align:justify; font-size:12.0pt; line-height:150%; font-family:宋体;  } </style>  
                    </head> 
                    <body>
                    """ 
                    if value.find("html") < 0 and  value.find("head") < 0 :
                        value = html_head + value + "</body><html>" 
                    if value.find("</body><html>") < 0 :
                        value =  value + "</body><html>" 
                    line["value"] = value
            else:
                line["value"] = value
        #td                
        if action=="insert": 
            dbMgr.insert(table_name_req,editColumn) 
        elif action=="update":
            dbMgr.update(table_name_req,editColumn,primary_column) 
        raise web.seeother('/table?table_name=' + table_name_req )
        
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run() 
    
         