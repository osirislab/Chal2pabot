#!/bin/python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import json


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db/chalbot'
db = SQLAlchemy(app)

class Challenge(db.Model):
    __tablename__ = "Challenge"

    name = db.Column(db.String(128), nullable=False, primary_key=True)
    url = db.Column(db.String(128), nullable=False)

    reports = db.relationship(
        'StateReport',
        backref=db.backref('chal', lazy=True),
        cascade="all, delete-orphan",
    )


class StateReport(db.Model):
    __tablename__ = "StateReport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), db.ForeignKey('Challenge.name'))
    state = db.Column(db.Boolean)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'timestamp': str(self.timestamp),
        }


db.create_all()


@app.route('/chal/new', methods=['POST'])
def chal_new():
    """
    {
      'url': 'http://web.chal.csaw.io:1000/'
      'name': 'dope ass challenge name'
    }
    """
    data = request.get_json(True)
    if 'url' in data and 'name' in data:
        c=Challenge.query.filter_by(
            name=data['name']
        ).first()
        if c is not None:
            return {
                'success': False,
                'reason': 'challenge exists'
            }, 400
        c=Challenge(
            url=data['url'],
            name=data['name'],
        )
        db.session.add(c)
        db.session.commit()

        return {
            'success': True,
            'data': data.copy()
        }
    return {
        'success': False
    }, 400


@app.route('/chal/del', methods=['POST'])
def chal_del():
    data = request.get_json(True)
    if 'name' in data:
        c=Challenge.query.filter_by(
            name=data['name']
        ).first()
        if c is not None:
            db.session.delete(c)
            db.session.commit()

            return {
                'success': True,
                'data': data.copy()
            }
    return {
        'success': False
    }


@app.route('/chal/report', methods=['POST'])
def chal_report():
    data = request.get_json(True)
    reptime=datetime.now()
    for chalname in data['CHALLENGE_MAP']:
        r=StateReport(
            name=chalname,
            state=chalname not in data['OFFLINE_CHALLENGES'],
            timestamp=reptime
        )
        db.session.add(r)
    db.session.commit()

    return {
        'success': True
    }


@app.route('/chal/list', methods=['GET'])
def chal_list():
    chals = Challenge.query.all()
    offline_chals = []
    for i in chals:
        report = StateReport.query.order_by(
            desc(StateReport.timestamp)
        ).limit(1).first()
        if report is not None and not report.state:
            offline_chals.append(
                report.name
            )

    return {
        'CHALLENGE_MAP': {
            chal.name: chal.url
            for chal in chals
        },
        'OFFLINE_CHALLENGES': offline_chals
    }


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
