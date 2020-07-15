from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from rivescript import RiveScript
import datetime
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
ENV = 'dep'
if ENV == 'DEV':
    # Development Database
    app.debug = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{passowrd}@localhost/{databasename}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/postgres'
else:
    # Deployment Database
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://unrsddyiapxizg:09a5b1765cd21fcf70b6f208ce10da94dccafa0acec4741b' \
                                            '5fca6a14540d77f8@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d2a43o4hjpbf76'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.create_all() >> Only first time to create database table

class Feedback(db.Model):
    __tablename__ = 'attendanceTable'
    name = db.Column(db.String(50))
    id = db.Column(db.String(7), primary_key=True)
    ip = db.Column(db.String(), unique=True)
    timestamp = db.Column(db.String())

    def __init__(self, name, id,ip,timestamp):
        self.name = name
        self.id = id
        self.ip = ip
        self.timestamp = timestamp

@app.route('/')
def index():
    session['name'] = ''
    session['id'] = ''
    return render_template('index.html')

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

@app.route('/submit', methods=['POST'])
def submit():
    # if request.method == 'POST':
    #     name = request.form['name']
    #     id = request.form['id']
    #     ip = request.remote_addr
    #     # print(name,id)
    #     if name=='' or id == '':
    #         return render_template('index.html', message='Please Enter Required Fields')
    #     if db.session.query(Feedback).filter(Feedback.ip == ip).count() != 0:
    #         return render_template('index.html', message='You Have Already Registered (Similar IP Address Detected)')
    #     if db.session.query(Feedback).filter(Feedback.name == name).count() == 0: #to check if student does not exist
    #         data = Feedback(name,id,ip)
    #         db.session.add(data)
    #         db.session.commit()
    #         return render_template('success.html')
    #     return render_template('index.html', message='You have already submitted your attendance')
    if request.method == 'POST':
        # global name, id
        try:
            if request.form['name'] != '': session['name'] = request.form['name']
            if request.form['id'] != '':  session['id']= request.form['id']
        except:
            pass
        # print(f"name: {session['name']} id: {session['id']} ")
        if session['name'] == '':
            print("The name is blank")
            return render_template('index.html', message='Please Enter Required Field')
        else:
            if session['id'] == '':
                print("Name is in ready to enter id")
                return render_template('index.html', reply1= bot.reply("localuser", session['name']))
        if session['name'] != '' and session['id'] != '':
            ip = request.remote_addr
            if db.session.query(Feedback).filter(Feedback.ip == ip).count() != 0:
                print("Name,ID reset1")
                session['name'], session['id'] = '', ''
                # session.pop('name', None)
                # session.pop('id', None)
                return render_template('index.html', message='You Have Already Registered (Similar IP Address Detected)')
            if db.session.query(Feedback).filter(Feedback.id == session['id']).count() == 0: #to check if student does not exist
                data = Feedback(session['name'],session['id'],ip, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                db.session.add(data)
                db.session.commit()
                print("Name,ID reset2")
                # name,id='',''
                session['name'], session['id'] = '', ''
                # session.pop('name', None)
                # session.pop('id', None)
                return render_template('success.html')
            print("Name,ID reset3")
            # name,id='',''
            session['name'],session['id']= '',''
            # session.pop('id', None)
            return render_template('index.html', message='You have already submitted your attendance before')

# def run():
#     bot = RiveScript()
#     bot.load_directory("./brain")
#     bot.sort_replies()
#     while True:
#         msg = input('You> ')
#         if msg == 'q':
#             break
#         reply = bot.reply("localuser", msg)
#         print('Bot>', reply)
#     bot.deparse()
#     name= bot.get_uservars().get('localuser').get('name')
#     id = bot.get_uservars().get('localuser').get('id')

def clearModel():
    db.session.query(Feedback).delete()
    db.session.commit()
    db.create_all()

if __name__ == '__main__':
    app.run()