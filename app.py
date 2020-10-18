from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import pandas as pd
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'
db = SQLAlchemy(app)

class Reactions(db.Model):
    __tablename__ = 'Reactions'
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))

    def __repr__(self):
        return f'<Reaction {self.id} : Reaction {self.reaction} : room {self.room_id}>'

class Rooms(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        reaction = request.form['content']
        room_id = request.form['room_id']
        new_reaction = Reactions(reaction=reaction, room_id=room_id)

        try:
            db.session.add(new_reaction)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        reactions = Reactions.query.order_by(Reactions.date_created).all()
        return render_template('index.html', tasks=reactions)

@app.route('/room/<int:id>', methods=['GET', 'POST'])
def room(id):
    if request.method == 'POST':
        reaction = int(request.form['react'])
        print("REACTION\n\n\n", reaction)
        new_reaction = Reactions(reaction=reaction, room_id=id)

        try:
            db.session.add(new_reaction)
            db.session.commit()
            return redirect(f'/room/{id}')
        except:
            return 'There was an issue adding your task'

    reactions = Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 1), Reactions.room_id == id).all()
    print(reactions)
    df = pd.read_sql(Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 5), Reactions.room_id == id).statement, db.session.bind)
    print(df)
    total = df["reaction"].sum() / len(df) if len(df) > 0 else 0
    print(total)
    return render_template('studentview.html', room_id=id, temp=f"{total * 100}%")

@app.route('/_stuff', methods=['GET'])
def stuff():
    return jsonify(result=random.randint(0, 10))


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Reactions.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Reactions.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)
