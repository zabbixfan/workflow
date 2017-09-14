from app import db
from app.common.time_helper import timestamp_to_datetime
from uuid import uuid1 as uuid



class TicketLog(db.Model):
    __tablename__ = "workflow_operatelog"
    id = db.Column(db.Integer,primary_key=True)
    ticketId = db.Column(db.String(255),default="")
    user = db.Column(db.String(255),default="")
    time = db.Column(db.DATETIME)
    action = db.Column(db.String(255),default="")
    content = db.Column(db.String(1000),default="")

    def save(self,wait_commit=False):
        db.session.add(self)
        if wait_commit:
            db.session.flush()
        else:
            db.session.commit()
    @staticmethod
    def commit():
        db.session.commit()