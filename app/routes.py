from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Task
from datetime import datetime

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
    new_task = Task(title=title, description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


