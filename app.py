import math
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'
db = SQLAlchemy(app)

emotions = ["angry", "happy", "sad", "surprise", "neutral"]

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

class Emotions(db.Model):
    __tablename__ = "Emotions"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    angry = db.Column(db.Float, default=0.0)
    disgust = db.Column(db.Float, default=0.0)
    fear = db.Column(db.Float, default=0.0)
    happy = db.Column(db.Float, default=0.0)
    sad = db.Column(db.Float, default=0.0)
    surprise = db.Column(db.Float, default=0.0)
    neutral = db.Column(db.Float, default=0.0)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))

    def __repr__(self):
        return f'<Angry {self.angry}; Disgust {self.disgust}; Fear {self.fear}; Happy {self.happy}; Sad {self.sad}; Surprise {self.surprise}; Neutral {self.neutral}>'

@app.route('/emotions', methods=["POST", "GET"])
def record_emotion():
    if request.method == "GET":
        emotions = Emotions.query.all()
        active = active_emotion(3, 1)
        temperature = emotion_to_sentiment(3, 1)
        print(active, temperature)
        return render_template('emotionsdb.html', emotions=emotions, active=active, temperature=temperature)
    else:
        print(request.form)
        emotions_recording = Emotions(**request.form)
        db.session.add(emotions_recording)
        db.session.commit()
        return str(emotions_recording)

def emotion_to_sentiment(mins, id, sqrt=True, weight=1.5):
    avg_emotion_vec = recent_emotion_average(mins, id)
    if sqrt:
        avg_emotion_vec = avg_emotion_vec.apply(math.sqrt)

    # sentiment weights
    happy = 1
    surprise = 1 / math.sqrt(2)
    sad = -1
    angry = -1 / math.sqrt(2)

    # mean temperature
    mean = 0.7

    # let neutral = 1.0 to be the mean temperature
    # multiply each emotion by the weight to determine the amount of change
    neg_multiplier = 1.5
    temp = mean + weight * (avg_emotion_vec["happy"] * happy + avg_emotion_vec["surprise"] 
        * surprise + neg_multiplier * (avg_emotion_vec["sad"] * sad + avg_emotion_vec["angry"] * angry))

    # if temp > 1:
    #     temp = 1
    return temp

def active_emotion(mins, id, exclude_neutral=True):
    avg_emotion_vec = recent_emotion_average(mins, id)
    if exclude_neutral:
        return avg_emotion_vec.drop(columns=["neutral"]).idxmax(axis=1)
    return avg_emotion_vec.idxmax(axis=1)

def recent_emotion_average(mins, id):
    df = pd.read_sql(Emotions.query.filter(Emotions.date_created > datetime.utcnow() - timedelta(minutes = mins), Emotions.room_id == id).statement, db.session.bind)
    print(df)
    return df[emotions].mean()


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

@app.route('/room/<int:id>', methods=['GET'])
def room(id):
    reactions = Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 1), Reactions.room_id == id).all()
    print(reactions)
    df = pd.read_sql(Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 5), Reactions.room_id == id).statement, db.session.bind)
    print(df)
    total = df["reaction"].sum() / len(df)
    print(total)
    return render_template('room.html', temp=total, room_id=id)


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
