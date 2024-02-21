'''
Before you can run this code, please do the following:
    Fill up the information in line 23 below "connStr = "host='cmpstudb-01.cmp.uea.ac.uk' dbname= '' user='' password = " + pw"
    using the Russell Smith's provided credentials', add your password in the pw.txt file.
    
    Get connected to VPN (https://my.uea.ac.uk/divisions/it-and-computing-services/service-catalogue/network-and-telephony-services/vpn) if you are running this code from an off-campus location.
    
    Get the server running in https://pgadmin.cmp.uea.ac.uk/ by log into the server. 
    
'''

import psycopg2
import pandas as pd

def getConn():
    #function to retrieve the password, construct
    #the connection string, make a connection and return it.
    #The pw.txt file will have the password to access the PGAdmin given to you by Russell Smith
    pwFile = open("pw.txt", "r")
    pw = pwFile.read();
    pwFile.close()
    # Fill up the following information from the Russell Smith's email.
    connStr = "host='cmpstudb-01.cmp.uea.ac.uk' \
               dbname= 'gev23vau' user='gev23vau' password = " + pw
    #connStr=("dbname='studentdb' user='dbuser' password= 'dbPassword' " )
    conn=psycopg2.connect(connStr)      
    return  conn

def clearOutput():
    with open("output.txt", "w") as clearfile:
        clearfile.write('')
        
def writeOutput(output):
    with open("output.txt", "a") as myfile:
        myfile.write(output)
         
try:
    conn=None   
    conn=getConn()
    # All the sql statement once run will be autocommited
    conn.autocommit=True
    cur = conn.cursor()
    
    f = open("input.txt", "r")
    clearOutput()
    for x in f:
        print(x)
        if(x[0] == 'A'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="INSERT INTO spectator (sno,sname,semail) VALUES ({},'{}','{}');".format(data[0],data[1],data[2]);
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

            
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * FROM spectator WHERE sno = {};".format(data[0])
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
        if(x[0] == 'B'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES ('{}','{}','{}','{}','{}',{});".format(data[0],data[1],data[2],data[3],data[4],data[5]);
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

            
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * FROM event WHERE ecode = '{}';".format(data[0])
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
                
        if(x[0] == 'C'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="DELETE from ticket where sno={};".format(data[0]);
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                sql="DELETE from spectator where sno={};".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

            
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * from ticket where sno={};".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                sql="SELECT * from spectator where sno={};".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
                
        if(x[0] == 'D'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="DELETE from ticket where ecode='{}';".format(data[0]);
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                sql="DELETE from event where ecode='{}';".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

            
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * from ticket where ecode='{}';".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                sql="SELECT * from event where ecode='{}';".format(data[0]);
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
                
        if(x[0] == 'E'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="INSERT INTO ticket (tno, ecode, sno) VALUES ((SELECT COALESCE(MAX(tno), 0) + 1 FROM ticket),'{}',{});".format(data[0],data[1]);
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

            
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * FROM ticket WHERE ecode = '{}';".format(data[0])
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
                
        if(x[0] == 'F'):
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="SELECT count(sno) as total_spectators,e.elocation,e.edate from event e join ticket t on e.ecode=t.ecode group by e.elocation,e.edate;"
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                
            except Exception as e:
                writeOutput(str(e)+"\n")

                print (e)
                
         
        if(x[0] == 'G'):
    # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
        # The SQL statement can be a INSERT statement
                sql="select count(tno) as total_tickets,e.edesc from event e join ticket t on e.ecode=t.ecode group by e.edesc Order by e.edesc;"
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
        # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
        
            except Exception as e:
                writeOutput(str(e)+"\n")

                print (e)
                
        
                
        if(x[0] == 'H'):
             raw = x.split("#",1)
             raw[1]=raw[1].strip()
             data = raw[1].split("#") 
             # Statement to insert data into the student table
             try:
                 cur.execute("Set SEARCH_PATH to 'tria', public;");
                 # The SQL statement can be a INSERT statement
                 sql="select count(tno) as total_tickets,e.edesc from event e join ticket t on e.ecode=t.ecode where e.ecode='{}'group by e.edesc;".format(data[0]);
                 writeOutput("TASK "+x[0]+"\n")         
                 cur.execute(sql)
                 writeOutput(cur.statusmessage+"\n")
                 table_df=pd.read_sql_query(sql, conn)
                 # Converting dataframe to string so that it can be written to text file.
                 table_str=table_df.to_string()
                 writeOutput(table_str+"\n")
                 
             except Exception as e:
                 writeOutput(str(e)+"\n")

                 print (e)
                
        if(x[0] == 'I'):
             raw = x.split("#",1)
             raw[1]=raw[1].strip()
             data = raw[1].split("#") 
             # Statement to insert data into the student table
             try:
                 cur.execute("Set SEARCH_PATH to 'tria', public;");
                 # The SQL statement can be a INSERT statement
                 sql="select s.sname,e.edate,e.elocation,e.etime,e.edesc from spectator s, ticket t, event e where e.ecode=t.ecode and s.sno=t.sno and s.sno={} group by e.edesc,s.sname,e.edate,e.elocation,e.etime;".format(data[0]);
                 writeOutput("TASK "+x[0]+"\n")         
                 cur.execute(sql)
                 writeOutput(cur.statusmessage+"\n")
                 table_df=pd.read_sql_query(sql, conn)
                 # Converting dataframe to string so that it can be written to text file.
                 table_str=table_df.to_string()
                 writeOutput(table_str+"\n")
                 
             except Exception as e:
                 writeOutput(str(e)+"\n")

                 print (e)
                 
        if(x[0] == 'J'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="select  sname,COALESCE(t.ecode, c.ecode) AS ecode, case when c.tno is not null then 'cancelled' else'valid' end as indication from spectator s full outer join ticket t on s.sno=t.sno full outer join  cancel c on t.tno=c.tno and t.ecode=c.ecode and t.sno=c.sno where t.tno={} or c.tno={};".format(data[0],data[0]); 
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")


                print (e)
                
        if(x[0] == 'K'):
            raw = x.split("#",1)
            raw[1]=raw[1].strip()
            data = raw[1].split("#")   
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;");
                # The SQL statement can be a INSERT statement
                sql="select * from Cancel where ecode='{}';".format(data[0]); 
                writeOutput("TASK "+x[0]+"\n")         
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")


                print (e)
        if(x[0] == 'L'):
            # Statement to insert data into the student table
            try:
                cur.execute("Set SEARCH_PATH to 'tria', public;")
                writeOutput("TASK "+x[0]+"\n") 
                sql="DELETE from spectator"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n") 
                sql="DELETE from event"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                sql="DELETE from ticket"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                sql="DELETE from cancel"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
            except Exception as e:
                writeOutput(str(e)+"\n")

                print (e)
            try:
                cur.execute("SET SEARCH_PATH to 'tria', public;");
                sql="SELECT * from spectator"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                sql="SELECT * from event"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                sql="SELECT * from ticket"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
                sql="SELECT * from cancel"
                cur.execute(sql)
                writeOutput(cur.statusmessage+"\n")
                # Sending the query and connection object to read_sql_query method of pandas pd. It reurns table as dataframe.
                table_df=pd.read_sql_query(sql, conn)
                # Converting dataframe to string so that it can be written to text file.
                table_str=table_df.to_string()
                writeOutput(table_str+"\n")
            except Exception as e:
                print (e)
        elif(x[0] == 'X'):
            print("Exit {}".format(x[0]))
            writeOutput("\n\nExit program!")
except Exception as e:
    print (e)               