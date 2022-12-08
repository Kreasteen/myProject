from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('todo_list.html', articles=articles)

@app.route('/todo/<int:id>')
def todo_detail(id):
    article = Article.query.get(id)
    return render_template('todo_detail.html', article=article)


@app.route('/todo/<int:id>/del')
def todo_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/todo')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template('/create.html')



if __name__ == '__main__':
    app.run()

