import json
import redis
r = redis.Redis(host='localhost', port=6379)
a=[1,2,3]
a=a+[4,5,6]
r.set('a',json.dumps(a))
