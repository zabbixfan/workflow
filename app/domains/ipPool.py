from app.models.ipPool import ipPool
def getIpPool(keyword):
    res=[]
    q=ipPool.query
    if keyword:
        key = keyword.replace("%","").replace("_","").replace("*","")
        key = '%{}%'.format(key)
        q = q.filter(ipPool.ip.like(key))
    for item in q.all():
        res.append({
            'ip':item.ip,
            'status': item.status
        })
    return res