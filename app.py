from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Task %r' %self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        #get task from the form
        content = request.form['content']
        #create task object
        task = Task(content=content)
        #Add task to db
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'could not add the task :('
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method=='POST':
        task.content = request.form['content']
        try:
            #No need to add because the task is already in the db. Just update the DB!!
            db.session.commit() 
            return redirect('/')
        except:
            return 'Could not update the Task :('
    else:
        return render_template('update.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error occurred. Could not delete the Task :('

@app.route('/delete/all')
def deleteAll():
    try:
        db.session.query(Task).delete()
        # db.session.delete(tasks)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error occured. Could not delete the tasks :('


if __name__ == '__main__':
    app.run(debug=True)
