from flask import Flask,render_template as rt,request as req,redirect,url_for
from flask_sqlalchemy import  SQLAlchemy
from wtforms import TextField,IntegerField,FloatField,SelectField,SelectMultipleField,RadioField
from flask_wtf import FlaskForm
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/pydbb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='pr@g@ti'
db=SQLAlchemy(app)

class Empform(FlaskForm):
 empid=IntegerField("EmpId:")
 empname=TextField("EmpName:")
 empage=IntegerField("EmpAge")
 emphobbies=SelectMultipleField("Emp Hobbies:",choices=(("1","Indoor"),("2","Outdoor"),("3","Coding")))

class Empmodel(db.Model):
    empid=db.Column("Emp_Id",db.Integer(),primary_key=True)
    empname=db.Column("Emp_Name",db.String(100))
    empage=db.Column("Emp_Age",db.Integer())
    emphobbies=db.Column("Emp_Hobbies",db.String(100))

@app.route("/emp/welcome/",methods=["GET"])
def Welcome_EmpPage():
    return rt('demo.html',eform=Empform())

@app.route("/emp/save/",methods=["POST","GET"])
def Save_Empinfo():
    msg=''
    dbmodel=Empmodel.query.filter_by(empid=req.form['empid']).first()
    if dbmodel:
        dbmodel.empname=req.form['empname']
        dbmodel.empage=req.form['empage']
        dbmodel.emphobbies=req.form['emphobbies']
        msg="Emp record updated...!!!"
    else:
        db.session.add(Empmodel(**req.form))
        msg="Emp record inserted"
    db.session.commit()
    return rt('demo.html',eform=Empform(formdata=None),msg=msg,emps=Empmodel.query.all())

@app.route("/emp/edit/<int:eid>")
def Edit_Emp(eid):
 dbmodel=Empmodel.query.filter_by(empid=eid).first()
 filledform=None
 if dbmodel:
     filledform=Empform(**dbmodel.__dict__)
 return rt('demo.html',eform=filledform,emps=Empmodel.query.all())

@app.route("/emp/delete/<int:eid>")
def Delete_Emp(eid):
    msg=''
    dbmodel=Empmodel.query.filter_by(empid=eid).first()
    if dbmodel:
        db.session.delete(dbmodel)
        db.session.commit()
        msg="Emp record deleted"
    return rt('demo.html',eform=Empform(formdata=None),emps=Empmodel.query.all(),msg=msg)

if __name__ == '__main__':
    #db.create_all()
 app.run(debug=True)