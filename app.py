from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'
db = SQLAlchemy(app)

class Reactions(db.Model):
    __tablename__ = 'Reactions'
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))

    def __repr__(self):
        return f'<Reaction {id} : Reaction {reaction} : room {room_id}>'

class Rooms(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        reaction = request.form['content']
        room_id = 3 # TODO
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

@app.route('/room/<int:id>', methods=['GET'])
def room(id):
    reactions = Reactions.query.order_by(Reactions.date_created).all()
    return render_template('room.html', temp=5, room_id=id)


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
