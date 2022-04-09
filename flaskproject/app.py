from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
connection_obj = sql.connect('COVID.db') 

cursor_object = connection_obj.cursor() 

cursor_object.execute('DROP TABLE IF EXISTS COVID') 

table = '''CREATE TABLE COVID( 

    AADHARNUMBER VARCHAR(25) PRIMARY KEY NOT NULL, 

    NAME VARCHAR(25) NOT NULL, 

    AGE INT, 

    DOSES INT 

    );''' 

cursor_object.execute(table)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def COVID_details():
    return render_template('COVID.html')



@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
         name = request.form['name']
         aadhar_no = request.form['aadhar_no']
         age = request.form['age']
         doses = request.form['doses']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO covid (name,aadhar_no,age,doses) VALUES (?,?,?,?)",(name,aadhar_no,age,doses) )
            
            con.commit()
            msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            con.close()
            return render_template("result.html",msg = msg)
            
   
@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from COVID")
   
   rows = cur.fetchall()
   return render_template("list.html",rows = rows)

if __name__ =='__main__':
    app.run(debug=True)