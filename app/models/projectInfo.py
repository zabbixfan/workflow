from app import db
from app.common.time_helper import timestamp_to_datetime
from uuid import uuid1 as uuid

class ProjectInfo(db.Model):
    __tablename__ = "workflow_projectInfo"
    pid = db.Column(db.String(255),primary_key=True)
    project = db.Column(db.String(255), default="")
    env = db.Column(db.String(32),primary_key=True)
    ip = db.Column(db.String(255),primary_key=True)
    port = db.Column(db.String(32),default="")
    def save(self,wait_commit=False):
            db.session.add(self)
            if wait_commit:
                db.session.flush()
            db.session.commit()
    @staticmethod
    def commit():
        db.session.commit()