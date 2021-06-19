import pymysql 
pymysql.install_as_MySQLdb() 
import MySQLdb 
  
# connect python with mysql with your hostname,  
# username, password and database 
db= MySQLdb.connect("localhost", "tanuja", "Tan@5588", "geeksforgeeks") 
  
# get cursor object 
cursor= db.cursor() 
  
# get number of rows in a table and give your table 
# name in the query 
cursor.execute("""select table_name as "Table",
                               round(((data_length + index_length)/1024/1024),2) 
                               as "Size(MB)" from information_schema.TABLES 
                               where table_schema="geeksforgeeks" and 
                               table_name="geekstudent" order by
                               (data_length+index_length)desc""") 
size_of_table= cursor.fetchall()

  
# print the number of rows 
for i in size_of_table:
	print(size_of_table)