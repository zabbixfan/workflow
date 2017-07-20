from app import db
from app.common.time_helper import timestamp_to_datetime
from uuid import uuid1 as uuid

statusMapper={
    'Apply':2,
    'Approve':3,
    'Refuse': 1,
    'Complete':4,
    'Delete': 0
}


class Tickets(db.Model):
    __tablename__= "workflow_list"
    id = db.Column(db.String(255),primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255),default="")
    status = db.Column(db.String(255),default="")
    requestMan = db.Column(db.String(255),default="")
    auditor = db.Column(db.String(255),default="")
    executor = db.Column(db.String(255),default="")
    email = db.Column(db.String(255),default="")
    data = db.Column(db.String(65535), default="")
    createTime = db.Column(db.DATETIME)
    requestManEng = db.Column(db.String(255),default="")

    def save(self,wait_commit=False):
        # if not self.id:
        #     self.id=uuid().get_hex()
        db.session.add(self)
        if wait_commit:
            db.session.flush()
        else:
            db.session.commit()
    @staticmethod
    def commit():
        db.session.commit()
    @staticmethod
    def get_by_ticketid(id):
        return Tickets.query.filter(Tickets.id==id).first()

class Project(db.Model):
    __tablename__ = "workflow_projectdetail"
    id = db.Column(db.String(255),primary_key=True)
    ticketId = db.Column(db.String(255))
    projectName = db.Column(db.String(255),default="")
    projectDescpriton = db.Column(db.String(255),default="")
    projectGroupName = db.Column(db.String(255),default="")
    projectType = db.Column(db.String(255),default="")
    owner = db.Column(db.String(255),default="")
    gitUrl = db.Column(db.String(255),default="")
    domainName = db.Column(db.String(255),default="")
    def save(self,wait_commit=False):
        if not self.id:
            self.id=uuid().get_hex()
            db.session.add(self)
            if wait_commit:
                db.session.flush()
        else:
            if wait_commit:
                db.session.flush()
            db.session.commit()
    @staticmethod
    def commit():
        db.session.commit()
    @staticmethod
    def get_by_pid(id):
        return Project.query.filter(Project.id==id).first()

