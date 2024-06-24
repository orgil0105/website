from flask import Flask, render_template, redirect,request, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    intro = db.Column(db.String(240), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img = db.Column(db.String)


    

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("resume.html")

@app.route('/tovari')
def tovari():
    vivodikrana = Article.query.order_by(Article.date.desc()).all()
    return render_template('tovari.html', articles=vivodikrana)

@app.route('/tovari/<int:id>')
def abtovar(id):
    vivodikran = Article.query.get(id)
    return render_template('abouttovar.html', article=vivodikran)

@app.route('/tovari/<int:id>/delete')
def tovari_delete(id):
    vivodikran = Article.query.get_or_404(id)

    try:
        db.session.delete(vivodikran)
        db.session.commit()
        return redirect('/tovari')
    except:
        return 'При удалении товара возникла ошибка'
    

@app.route('/tovari/<int:id>/update', methods=['POST','GET'])
def tovari_update(id):
    vivodikran = Article.query.get(id)
    if request.method == 'POST':
        vivodikran.title = request.form['title']
        vivodikran.intro = request.form['intro']
        vivodikran.text = request.form['text']
        

        try:
            db.session.commit()
            return redirect('/tovari')
        except:
            return 'При редактировании товара возникла ошибка'
    else:
        return render_template('update.html', article=vivodikran)


@app.route('/create-post', methods=['GET', 'POST'])
def post():
        if request.method == 'POST':
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']
            img = request.files["img"]
            imgname = img.filename
            if imgname:
                img.save(os.path.join(app.root_path, 'static', 'images', imgname))

            article = Article(title=title, intro=intro, text=text, img=imgname)

            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/tovari')
            except:
                return 'При добавлении товара возникла ошибка'
        else:
            return render_template("create-post.html")

if __name__=='__main__':
    app.run(debug=True, port=5001)
    
    

