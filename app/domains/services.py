#!coding:utf-8
import consul


def append(res,service):
    key = service['Key']
    if key.count('/') == 2:
        res.append({
            "project": key.split('/')[1],
            "env": key.split('/')[2],
            "ip": '',
            "status": ''
        })
    else:
        res.append({
            "project": key.split('/')[1],
            "env": key.split('/')[2],
            "ip": key.split('/')[3],
            "status": service['Value']
        })
def ServicesList(keyword,envs,offset,limit,status):
    c = consul.Consul()
    _,services = c.kv.get('services/',recurse=True)
    results = []
    for service in services:
        key = service['Key']
        project = key.split('/')[1]
        env = key.split('/')[2]
        if key.endswith('status') or (key.count("/") == 2 and not key.endswith('port')):
            if keyword and envs:
                if project in keyword and env in envs:
                    append(results,service)
            elif keyword and not envs:
                if project in keyword:
                    append(results, service)
            elif not keyword and envs:
                if env in envs:
                    append(results,service)
            elif not keyword and not envs:
                append(results,service)
        if status:
            if status in ['failure','ok']:
                results = [item for item in results if item['status']==status]
            else:
                results = [item for item in results if item['status']]
        if status is False:
            results = [item for item in results if item['status'] == 'failure']
    TotalCount = len(results)
    if limit==-1 or limit==0:
        results = results[offset:]
    else:
        results = results[offset:offset+limit]
    return {'Datalist':results,'TotalCount':TotalCount,"offset":offset,"limit":limit}

def getServiceInfo(key):
    c = consul.Consul()
    _,services = c.kv.get('services/',index=1,recurse=True)
    services = set([serv["Key"].split("/")[1]for serv in services])
    if key:
        res = [ser for ser in services if ser.startswith(key) ]
    else:
        res = list(services)
    return {"data":res}