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
def ServicesList(keyword,envs,offset,limit):
    c = consul.Consul()
    _,services = c.kv.get('services/',recurse=True)
    results = []
    for service in services:
        key = service['Key']
        project = key.split('/')[1]
        env = key.split('/')[2]
        if key.endswith('status'):
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
        elif key.count('/') == 2:
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
    TotalCount = len(results)
    if limit==-1 or limit==0:
        results = results[offset:]
    else:
        results = results[offset:offset+limit]
    return {'Datalist':results,'TotalCount':TotalCount,"offset":offset,"limit":limit}
    import json
    print json.dumps({'data':results},indent=4)
    print len(results)
    return {'data':results}