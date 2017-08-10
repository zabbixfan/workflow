#!coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from config import Config
from sqlalchemy import create_engine
from sqlalchemy import Column,String,DATETIME,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.time_helper import timestamp_to_datetime
from uuid import uuid1 as uuid

eng = create_engine(Config.CMDB_DATABASE_URI)
Model = declarative_base()
Session  = sessionmaker(bind=eng)
cmdbSession = Session()

class IdcCode(object):
    aliyun = "aliyun"
    internal = "datacenter"


class ServerStatus(object):
    Running = "running"
    Stopped = "stopped"
    Deleted = "deleted"


class Server(Model):
    __tablename__ = "cmdb_server"

    server_id = Column(String(32), primary_key=True)
    host_name = Column(String(255), default="")
    internal_ip = Column(String(50), default="")
    external_ip = Column(String(50), default="")
    cpu = Column(Integer, default=0)
    memory = Column(Integer, default=0)
    gpu = Column(Integer, default=0)
    disk = Column(Integer, default=0)
    idc = Column(String(255), default="")
    idc_server_id = Column(String(50), default="")
    idc_zone = Column(String(255), default="")
    os_platform = Column(String(255), default="")
    os_name = Column(String(255), default="")
    status = Column(String(50), default="")
    creation_time = Column(DATETIME, default=timestamp_to_datetime(0))
    expired_time = Column(DATETIME, default=timestamp_to_datetime(0))
    remark = Column(String(500), default="")
    manager = Column(String(32), default="")


    def save(self, wait_commit=False):
        if not self.server_id:
            self.server_id = uuid().get_hex()
        cmdbSession.add(self)
        if wait_commit:
            cmdbSession.flush()
        else:
            cmdbSession.commit()


    @staticmethod
    def commit():
        cmdbSession.commit()
