import math
import numpy as np
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
        
        emotions_all = Emotions.query.all()
        active = active_emotion(1, 5)
        temperature = emotion_to_sentiment(3, 5)
        return render_template('emotionsdb.html', emotions=emotions_all, active=active, temperature=temperature)
    else:
        print("hello")
        data = {}
        for k, v in request.form.items():
            if k in emotions:
                data[k] = float(v)
            else:
                data[k] = int(v)
        print(data)
        emotions_recording = Emotions(**data)
        db.session.add(emotions_recording)
        db.session.commit()
        return str(emotions_recording)

def emotion_to_sentiment(mins, id, sqrt=True, weight=1):
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
    neg_multiplier = 1
    temp = mean + weight * (avg_emotion_vec["happy"] * happy + avg_emotion_vec["surprise"] 
        * surprise + neg_multiplier * (avg_emotion_vec["sad"] * sad + avg_emotion_vec["angry"] * angry))

    if temp > 1:
        temp = 1
    elif np.isnan(temp):
        return mean
    return temp

def active_emotion(mins, id, exclude_neutral=True):
    avg_emotion_vec = recent_emotion_average(mins, id)
    if exclude_neutral:
        del avg_emotion_vec["neutral"]
    return avg_emotion_vec.idxmax(axis=1)

def recent_emotion_average(mins, id):
    print("querying database with the following params")
    print(mins, id)
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
    # if request.method == 'POST':
    #     reaction = int(request.form['react'])
    #     print("REACTION\n\n\n", reaction)
    #     new_reaction = Reactions(reaction=reaction, room_id=id)

    #     try:
    #         db.session.add(new_reaction)
    #         db.session.commit()
    #         return redirect(f'/room/{id}')
    #     except:
    #         return 'There was an issue adding your task'

    reactions = Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 1), Reactions.room_id == id).all()
    print(reactions)
    df = pd.read_sql(Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 5), Reactions.room_id == id).statement, db.session.bind)
    print(df)
    total = df["reaction"].sum() / len(df) if len(df) > 0 else 0
    print(total)

    return render_template('studentview.html', room_id=id, temp=f"{total * 100}%")

@app.route('room/<int: id>/react', methods=["GET"])
def get_pace(id):
    df = pd.read_sql(Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 5), Reactions.room_id == id).statement, db.session.bind)
    result = int(df["reaction"].sum() / 3)
    if result > 5:
        result = 5
    elif result < -5:
        result = -5
    return result

@app.route('/room/<int:id>/active', methods=['GET'])
def yeet(id):
    active = active_emotion(1, id)
    print("EWHLKJSD F" + str(active))
    if not isinstance(active, str):
        print("YEEE")
        return jsonify(result="happy")
    return jsonify(result=active)

# Returns the temperature
@app.route('/room/<int:id>/data', methods=['GET'])
def stuff(id):
    # # return jsonify(result=random.randint(0, 1) * 100)
    # reactions = Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 1), Reactions.room_id == id).all()
    # print(reactions)
    # df = pd.read_sql(Reactions.query.filter(Reactions.date_created > datetime.utcnow() - timedelta(minutes = 5), Reactions.room_id == id).statement, db.session.bind)
    # print(df)
    # total = df["reaction"].sum() / len(df) * 100 if len(df) > 0 else 0
    # return jsonify(result=total)
    result = emotion_to_sentiment(3, id) * 100
    print(f"looking for stuff in {id}")
    print (result)
    return jsonify(result=result)

@app.route('/room/<int:id>/push', methods=['POST'])
def stuff2(id):
    reaction = int(request.form['react'])
    print("REACTION\n\n\n", reaction)
    new_reaction = Reactions(reaction=reaction, room_id=id)

    try:
        db.session.add(new_reaction)
        db.session.commit()
        return redirect(f'/room/{id}/data')
    except:
        print("\n\nn\ yi8kes")
        return 'There was an issue adding your task'
    print("\n\nPOSTED+!!!!!\n\n")
    return jsonify()


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
