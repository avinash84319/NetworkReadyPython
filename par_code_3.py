import json
import redis
r = redis.Redis(host='localhost', port=6379)
a=json.loads(r.get('a$3'))
a=a+[5,4,3]
print(a)
