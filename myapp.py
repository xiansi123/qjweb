# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify,json
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from config import *
from Models import *
from exts import db
from decorators import longin_required
app = Flask(__name__)
#由于不知道的原因，从configure导入在运行manager.py db migrate时会出错
#app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql123456@127.0.0.1/qjweb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']=SECRETT_KEY
db.init_app(app)
@app.route('/')
@longin_required
def index():
    if request.method=='GET':
        re_json={}
        following_list=[]
        user_id = session.get('user_id')
        # follow_rela表示follow表中的元组
        follow_rela = Follow.query.filter(Follow.follower == user_id).all()
        if follow_rela:
            for i in follow_rela:
                #print i
                #假定找到的被关注者id都存在
                followed_user=User.query.filter(User.id==i.following).first()
                if followed_user:
                    following_list.append(followed_user.username)
        #print following_list
        re_json['following_list']=following_list
    #return jsonify(re_json)
    return render_template('index.html',re_json=re_json)

@app.route('/question/',methods=['GET','POST'])
@longin_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content=request.form.get('content')
        user_id = session.get('user_id')
        question=Question(title=title,content=content,author_id=user_id)
        #user=User.query.filter(User.id==user_id).first()
        try:
            db.session.add(question)
            db.session.commit()
            #print user.questions
        except Exception as e:
            print e
            db.session.rollback()
        return render_template('question.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:

        username=request.form.get('username')
        password = request.form.get('password')
        user=User.query.filter(User.username==username,User.password==password).first()
        if user:
            #login_user(user)
            session['user_id']=user.id
            session['user_state'] = user.state
            session['intention'] = user.intention
            #30天内不再需要登录
            session.pernanent=True
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误'
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        tele=request.form.get('tele')
        username=request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        #如果已经注册则不能再注册
        user=User.query.filter(User.telephone==tele).first()
        if user:
            flash(u'手机号已经被注册')
            return redirect(url_for('register'))

        else:
            if password!=password1:
                flash(u'密码不一致')
                return redirect(url_for('register'))
            else:
                try:
                    user=User(telephone=tele,username=username,password=password1)
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print e
                    flash(u'添加失败')
                    db.session.rollback()
                return redirect(url_for('login'))

@app.route('/setting/',methods=['GET','POST'])
def setting():
    if request.method=='GET':
        return render_template('setting.html')

@app.route('/logout/',methods=['GET','POST'])
def logout():
    session['user_id'] = None
    return render_template('logout.html')

@app.route('/personal/',methods=['GET','POST'])
@longin_required
def personal():
    if request.method=='GET':
        user_id = session.get('user_id')
        user_state=session['user_state']
        re_json = {}
        if user_state==1: #在校生
            info=Stu.query.filter(Stu.user_id==user_id).first()
            if info:
                re_json['number']=info.number
                re_json['name'] = info.name
                re_json['school'] = info.school
                re_json['sex'] = info.sex
                re_json['age'] = info.age
                re_json['major'] = info.major
                re_json['depart'] = info.depart
                re_json['term'] = info.term

        elif user_state==2:#研究生
            info=Post.query.filter(Post.user_id==user_id).first()
            if info:
                re_json['city']=info.city
                re_json['school'] = info.school
                re_json['major'] = info.major
                re_json['name'] = info.name
                re_json['sex'] = info.sex
                re_json['age'] = info.age
                re_json['major'] = info.major
                re_json['depart'] = info.depart
                re_json['grades'] = info.grades
                re_json['advice']=info.advice
                re_json['others'] = info.others
        elif user_state==3:#出国留学生
            info = Abroad.query.filter(Abroad.user_id == user_id).first()
            if info:
                re_json['country']= info.country
                re_json['city']   = info.city
                re_json['school'] = info.school
                re_json['name']   = info.name
                re_json['sex']    = info.sex
                re_json['age']    = info.age
                re_json['major']  = info.major
                re_json['TOELF']  = info.TOELF
                re_json['IELTS']  = info.IELTS
                re_json['others'] = info.others
                re_json['advice'] = info.advice
        elif user_state == 4:  # 工作
            info = Job.query.filter(Job.user_id == user_id).first()
            if info:
                re_json['city'] = info.city
                re_json['name'] = info.name
                re_json['content'] = info.content
                re_json['salary'] = info.salary
                re_json['company'] = info.company
                re_json['sex'] = info.sex
                re_json['age'] = info.age
                re_json['others'] = info.others
                re_json['advice'] = info.advice
        else:#老师
            info = Tea.query.filter(Tea.user_id == user_id).first()
            if info:

                re_json['school'] = info.school
                re_json['name'] = info.name
                re_json['sex'] = info.sex
                re_json['willings'] = info.willings
                re_json['major_in'] = info.major_in
                re_json['others'] = info.others
        #print jsonify(re_json)
    #return jsonify(re_json)
    return  render_template('personal.html',re_json=re_json)

@app.route('/suggestion/',methods=['GET','POST'])
@longin_required
def suggestion():
    if request.method=='GET':
        re_json={}
        suggest_list=[]
        user_id = session.get('user_id')
        intention=session.get('intention')
        if intention == 1:  # 找导师
            teas=Tea.query.all()
            if teas:
                for t in teas:
                    suggest_list.append(t.name)
        elif intention == 2:#考研
            posts = Post.query.all()
            if posts:
                for p in posts:
                    suggest_list.append(p.name)
        elif intention == 3:#出国
            abroads = Abroad.query.all()
            if abroads:
                for a in abroads:
                    suggest_list.append(a.name)
        else:#intention == 4 找工作
            jobs = Job.query.all()
            if jobs:
                for j in jobs:
                    suggest_list.append(j.name)
        re_json['suggest_list']=suggest_list
    return jsonify(re_json)
    #return render_template('suggestion.html',re_json=re_json)



@app.route('/test/')
def jsonrep():
    t = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    return jsonify(t)
#添加记录
def insert_info(user_state,user_id,res_json):
    if user_state == 1:  # 在校生
        new_info=Stu(user_id=session['user_id'],
        number=res_json['number'] ,
        name=res_json['name'] ,
        school=  res_json['school'],
        sex = res_json['sex'] ,
        age=res_json['age'] ,
        major=res_json['major'] ,
        depart=res_json['depart'] ,
        iterm=res_json['term'])
    elif user_state == 2:  # 研究生
        new_info= Post(user_id=session['user_id'],
                      city=res_json['city'],
                      school=res_json['school'],
                      major=res_json['major'],
                      name=res_json['name'],
                      sex=res_json['sex'],
                      age=res_json['age'],
                      grades=res_json['grades'],
                      advice=res_json['advice'],
                      others=res_json['others']
                      )
    elif user_state == 3:  # 出国留学生
        new_info = Abroad(user_id=session['user_id'],
                          city=res_json['city'],
                          school=res_json['school'],
                          major=res_json['major'],
                          name=res_json['name'],
                          sex=res_json['sex'],
                          age=res_json['age'],
                          TOELF=res_json['TOELF'],
                          country=res_json['country'],
                          IELTS=res_json['IELTS'],
                          advice=res_json['advice'],
                          others=res_json['others'],
                          )
    elif user_state == 4:  # 工作
        new_info = Job(user_id=session['user_id'],
                       city=res_json['city'],
                       content=res_json['content'],
                       name=res_json['name'],
                       company=res_json['company'],
                       sex=res_json['sex'],
                       age=res_json['age'],
                       salary=res_json['salary'],
                       advice=res_json['advice'],
                       others=res_json['others']
                       )
    else:  # 老师
        new_info = Tea(user_id=session['user_id'],
                       major_in=res_json['major_in'],
                       name=res_json['name'],
                       school=res_json['school'],
                       sex=res_json['sex'],
                       willings=res_json['willings'],
                       others=res_json['others']
                       )
    try:
        db.session.add(new_info)
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()

#修改
def modify(user_state,user_id,res_json):
        data = json.loads(res_json)
        if user_state == 1:  # 在校生
            info = Stu.query.filter(Stu.user_id == user_id).first()
            keys=data.keys()
            for i in keys:
                info.i=data[i]

if __name__ == '__main__':
    app.run(host='0.0.0.0')




