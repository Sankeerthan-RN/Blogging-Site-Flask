from flask import Flask,render_template,url_for,flash,session,redirect,logging,request
# from flask_mysqldb import MySQL
from registrationform import RegisterForm
from articleform import ArticleForm
from wtforms import *
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL


app=Flask(__name__)
app.secret_key='nasjdsbdjkasduig123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sankeerthan'
app.config['MYSQL_DB'] = 'blogapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
        return render_template('about.html',title='About')
@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()   
    # result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()
    
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    cur.close() 


@app.route('/edit_article<string:id>/',methods=['GET','POST'])   

def edit_article(id):
    form=ArticleForm(request.form)
    cur=mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()    
    form.title.data = article['title']
    form.body.data = article['body']
    cur.close()
    if(request.method== 'POST' and form.validate()):
        title=request.form.get('title')
        body=request.form.get('body')
        cur=mysql.connection.cursor()
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        
        mysql.connection.commit()
        cur.close()
        flash('ARTICLE EDITED','success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('edit_article.html',form=form)    


@app.route('/delete_article/<string:id>',methods=['GET','POST'])    

def delete_article(id):
    cur = mysql.connection.cursor()

    
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    
    
    mysql.connection.commit()

    
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))
    
@app.route('/article/<string:id>/')       
def article(id):
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    # result = cur.execute("SELECT * FROM articles)

    article = cur.fetchone()

    return render_template('article.html', article=article)


    


@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()   
    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cur.fetchall()
    cur.close()
    print(result)
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

    

class ArticleForm(Form):
    title = StringField(u'title', validators=[validators.input_required(),validators.length(min=1,max=100)])
    body = TextAreaField(u'body', validators=[validators.input_required(),validators.length(min=10)])

@app.route('/create_article',methods=['GET','POST'])
def create_article():
    form=ArticleForm(request.form)
    if(request.method== 'POST' and form.validate()):
        title=form.title.data
        body=form.body.data
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('ARTICLE created','success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('add_article.html',form=form)       

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        fname=form.first_name.data
        lname=form.last_name.data
        email=form.email.data
        uname=form.username.data
        password=sha256_crypt.encrypt(str(form.password.data))
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users(firstname,lastname,email,username,password) VALUES(%s,%s,%s,%s,%s)",(fname,lname,email,uname,password))

        mysql.connection.commit()
        cur.close()

        flash('You are successfully registered','success')
        return redirect(url_for('index'))
        
    return render_template ('register.html',form=form)   

@app.route('/login',methods=['POST','GET'])    
def login():
    if request.method=='POST':
        cur_user=request.form.get('username')
        password_user=request.form.get('password')
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * FROM users WHERE username = %s", [cur_user])
        if result > 0:
            
            data = cur.fetchone()
            password = data["password"]

           
            if sha256_crypt.verify(password_user, password):
               
                session['logged'] = True
                session['username'] = cur_user

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Password'
                return render_template('login.html', error=error)
            
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)   

    else:
        return render_template('login.html')   

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))
if __name__=='__main__':
    
    app.run(debug=True)