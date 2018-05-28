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
        follower_list=[]
        user_id = session.get('user_id')

        # follow_rela表示follow表中的元组
        #查询关注者
        follow_rela = Follow.query.filter(Follow.follower == user_id).all()
        if follow_rela:
            for i in follow_rela:
                #print i
                #假定找到的被关注者id都存在
                following_user=User.query.filter(User.id==i.following).first()
                if following_user:
                    following_user_info = {}
                    following_user_info["name"] = following_user.username
                    following_user_info["following_id"] = following_user.id
                    following_list.append(following_user_info)

        #print following_list
        re_json['following_list']=following_list
        #查询粉丝
        follow_rela1 = Follow.query.filter(Follow.following == user_id).all()
        if follow_rela1:
            for i in follow_rela1:
                # print i
                # 假定找到的被关注者id都存在
                follower_user = User.query.filter(User.id == i.follower).first()
                if follower_user:
                    follower_user_info = {}
                    follower_user_info["name"] = follower_user.username
                    follower_user_info["follower_id"] = follower_user.id

                    follower_list.append(follower_user_info)

        re_json['follower_list'] = follower_list

    #return jsonify(re_json)
    return render_template('index.html',re_data=re_json)

@app.route('/dynamic')
@longin_required
def dynamic():
    #data = json.loads(request.get_data())
    # 或者data = json.loads(request.form.get('data'))
    #followings_id = data['following_list_id']
    followings_id={0:1}
    followings_info=[]
    #followings_id为{0:id,1:id,}
    for key,value in followings_id.items():
        dynamic_info={}
        dynamic = Dynamic.query.filter(Dynamic.user_id == value).first()
        dynamic_info["following_id"]=value
        dynamic_info["Dynamic_type"]=dynamic.Dynamic_type
        dynamic_info["Dynamic_name"] = dynamic.Dynamic_name
        dynamic_info["Dynamic_content"] = dynamic.Dynamic_content
        dynamic_info["Dynamic_time"] = dynamic.Dynamic_time
        followings_info.append(dynamic_info)
    return jsonify(followings_info)

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
        print username
        password = request.form.get('password')
        print password
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
            return u'用户名或密码错误login'
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
                re_json['no']=info.no
                re_json['name'] = info.name
                re_json['school'] = info.school
                re_json['sex'] = info.sex
                re_json['age'] = info.age
                re_json['major'] = info.major
                re_json['depart'] = info.depart
                re_json['term'] = info.term
                re_json['school_life'] = info.school_life
                re_json['hobby'] = info.hobby
                re_json['self_evaluation'] = info.self_evaluation
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
                re_json['school_life'] = info.school_life
                re_json['hobby'] = info.hobby
                re_json['self_evaluation'] = info.self_evaluation
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
                re_json['school_life'] = info.school_life
                re_json['hobby'] = info.hobby
                re_json['self_evaluation'] = info.self_evaluation
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
                re_json['school_life'] = info.school_life
                re_json['hobby'] = info.hobby
                re_json['self_evaluation'] = info.self_evaluation
        else:#老师
            info = Tea.query.filter(Tea.user_id == user_id).first()
            if info:

                re_json['school'] = info.school
                re_json['name'] = info.name
                re_json['sex'] = info.sex
                re_json['willings'] = info.willings
                re_json['major_in'] = info.major_in
                re_json['others'] = info.others
                re_json['school_life'] = info.school_life
                re_json['hobby'] = info.hobby
                re_json['self_evaluation'] = info.self_evaluation
        #print jsonify(re_json)
    #return jsonify(re_json)
    return  render_template('personal.html',re_data=re_json)

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
                    suggest = {}
                    suggest["name"]=t.name
                    #print suggest["name"]
                    suggest["suggest_id"] = t.user_id
                    suggest["school"] = t.school
                    suggest["sex"] = t.sex
                    suggest["major_in"] = t.major_in
                    suggest_list.append(suggest)
                print suggest_list
        elif intention == 2:#考研
            posts = Post.query.all()
            if posts:
                for p in posts:
                    suggest = {}
                    suggest["name"]=p.name
                    suggest["suggest_id"] = p.user_id
                    suggest["sex"] = p.sex
                    suggest["depart"] = p.depart
                    suggest["school"] = p.school

                    suggest_list.append(suggest)

        elif intention == 3:#出国
            abroads = Abroad.query.all()
            if abroads:
                for a in abroads:
                    suggest = {}
                    suggest["name"]=a.name
                    suggest["suggest_id"] = a.user_id
                    suggest["sex"] = a.sex
                    suggest["depart"] = a.depart
                    suggest["school"] = a.school
                    suggest_list.append(suggest)

        else:#intention == 4 找工作
            jobs = Job.query.all()
            if jobs:
                for j in jobs:
                    suggest = {}
                    suggest["name"]=j.name
                    suggest["suggest_id"] = j.user_id
                    suggest["sex"] = j.sex
                    suggest["depart"] = j.depart
                    suggest["school"] = j.school
                    suggest_list.append(suggest)

        re_json['suggest_list']=suggest_list
        #print re_json
    #return jsonify(re_json)
    return render_template('suggestion.html', re_data=re_json)

@app.route('/myGoal/',methods=['GET','POST'])
@longin_required
def myGoal():
    if request.method == 'GET':
        # user_id = session.get('user_id')
        # intention = session.get('intention')
        # if not intention:
        return render_template('myGoal.html')

@app.route('/selectMygoal/')
@longin_required
def selectMygoal():
    data = json.loads(request.get_data())
    #或者data = json.loads(request.form.get('data'))
    user_id = session.get('user_id')
    user=User.query.filter(User.id==user_id).first()
    user.intention=data['intention']
    return render_template('suggestion1.html')
    # request.method == 'GET':
    #     return "请选择"
    # else:
    #     return "xxx"

@app.route('/unfollow/')
@longin_required
def unfollow():
    if request.method == 'POST':
        data=json.loads(request.get_data())
        following_id=data['following_id']
        try:
            user = User.query.filter(User.id == following_id).first()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
            #return "delete ok"
        except Exception as e:
            print e
            flash(u'删除失败')
            db.session.rollback()
    else:
        return "请提交参数"

@app.route('/follow/')
@longin_required
def follow():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        following_id = data['follow_id']
        try:
            user = User.query.filter(User.id == following_id).first()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
            # return "delete ok"
        except Exception as e:
            print e
            flash(u'删除失败')
            db.session.rollback()
    else:
        return "请提交参数"

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




