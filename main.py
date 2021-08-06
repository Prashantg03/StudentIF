from flask import Flask,render_template,request
import pandas as pd
import csv
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/SIS_project'
db=SQLAlchemy(app)

class Registrationform(db.Model):
    stud_id=db.Column(db.Integer, primary_key=True)
    stud_name    = db.Column(db.String(50) , nullable=False)
    father_name   = db.Column(db.String(50) , nullable=False)
    sur_name   = db.Column(db.String(50) , nullable=False)
    mother_name   = db.Column(db.String(50) , nullable=False)
    gender = db.Column(db.String(7) , nullable=False)
    dob    = db.Column(db.String(30) , nullable=False)
    doj    = db.Column(db.String(30) , nullable=False)
    s_class   = db.Column(db.String(30) , nullable=False)
    course_name   = db.Column(db.String(100) , nullable=False)
    mobile_number	    = db.Column(db.Integer , nullable=False)
    city   = db.Column(db.String(50) , nullable=False)
    address   = db.Column(db.String(50) , nullable=False)
    email_id   = db.Column(db.String(50) , nullable=False)
    
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/registration",methods=['GET','POST'])
def registration():
    if (request.method=='POST'):
        """Add Entry to Database"""
        sname=request.form.get('sname')
        fname=request.form.get('fname')
        surname=request.form.get('surname')
        mname=request.form.get('mname')
        gender=request.form.get('gender')
        dob=request.form.get('dob')
        doj=request.form.get('doj')
        s_class=request.form.get('class')
        course=request.form.get('course')
        mobile=request.form.get('mobile')
        city=request.form.get('city')
        address=request.form.get('address')
        email=request.form.get('email')

        entry=Registrationform(stud_name=sname,father_name=fname,sur_name=surname,mother_name=mname,
                           gender=gender,dob=dob,doj=doj,s_class=s_class,course_name=course,mobile_number=mobile,city=city,address=address,email_id=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('registration.html')

@app.route("/studinfo")
def stud_info():
    info=Registrationform.query.all()
    return render_template('studinfo.html',info=info)

def write_to_csv(data):
    with open('database.csv',mode='a') as db2:
        name = data['name']
        email = data['email']
        message = data['message']
        csv_writer = csv.writer(db2,delimiter=',', quotechar='|',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,message])

@app.route('/send', methods=['POST','GET'])
def form_submit():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return render_template('ok.html')
        except:
            print('something went wrong... data did not save to the database\n Try again later')
    else:
        print('Something went wrong.Try again....')

def access():
    pd.read_csv('database.csv')
    print(pd)

access()


app.run(debug=True)

