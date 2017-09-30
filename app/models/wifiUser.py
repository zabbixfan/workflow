from app import db

class radCheck(db.Model):
    __tablename__= "radcheck"
    __bind_key__ = 'radius'
    id=db.Column((db.INTEGER),primary_key=True)
    username=db.Column(db.String(64),default="")
    attribute=db.Column(db.String(64),default="Cleartext-Password")
    op=db.Column(db.String(64),default=":=")
    value=db.Column(db.String(64),default="")
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
    def delete(object):
        db.session.delete(object)
        db.session.commit()