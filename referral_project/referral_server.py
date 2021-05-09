from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 
import math, random

app = Flask(__name__,template_folder='template')
app.secret_key = 'your secret key'
@app.route('/')
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        con=sqlite3.connect('referaldb.db')
        name = request.form['username']
        mail_id = request.form['email']
        password=request.form['password']
        ref_code=request.form['ref_code']
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        OTP = ""
        length = len(string)
        for i in range(6):
            OTP += string[math.floor(random.random() * length)]
        referrals=con.execute("SELECT * from reftable")
        ref_list=[]
        ref_mails=[]
        for r in referrals.fetchall():
            ref_list.append(r[3])
            ref_mails.append(r[1])
        if mail_id in ref_mails:
            return render_template("register.html",msg="account already exist")
        elif ref_code in ref_list:
            referer=con.execute("SELECT * from reftable WHERE refcode=?",(ref_code,))
            r_l=referer.fetchall()
            referer_point=r_l[0][4]
            referer_mailid=r_l[0][1]
            con.execute("UPDATE reftable set pin=? WHERE email=?",(referer_point+10,referer_mailid))
            con.commit()
            try:
                con.execute("INSERT into reftable (name,email,pass,refcode,pin) values (?,?,?,?,?)",(name,mail_id,password,OTP,5))
                con.commit()
            except:
                con.rollback()
            finally:
                return render_template("result.html",name=name,point=5,ref_code=OTP)
                #return point
                con.close()
        else:
            try:
                con.execute("INSERT into reftable (name,email,pass,refcode,pin) values (?,?,?,?,?)",(name,mail_id,password,OTP,0))
                con.commit()
            except:
                con.rollback()
            finally:
                return render_template("result.html",name=name,point=0,ref_code=OTP)
                #return point
                con.close()
    return render_template("register.html")
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('password', None)
    session.pop('username', None)
    session.pop('username', None)
    return redirect(url_for('register'))


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        con=sqlite3.connect('referaldb.db')
        emails=con.execute("SELECT email,pass from reftable")
        ids=[]
        for i in emails.fetchall():
            ids.append(i[0])
        mail_id = request.form['email']
        pas_word=request.form['password']
        if mail_id in ids:
            password=con.execute("SELECT * from reftable WHERE email=?",(mail_id,))
            c_l=password.fetchall()
            if pas_word==c_l[0][2]:
                return render_template("login_result.html",name=c_l[0][0],point=c_l[0][4],ref_code=c_l[0][3])
            else:
                return render_template("login.html",msg="Invalid id or PASSWORD")
    return render_template("login.html")
@app.route('/loginlogout')
def loginlogout():
    session.pop('email', None)
    session.pop('password', None)
    #session.pop('username', None)
    #session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
   app.run(debug = True)
    
                

            
