import redis

r = redis.Redis(host='redis', port=6379)

## Add hashset
def add(hashname, field, value):
    r.hset(hashname, field, value)

## Remove hashset field
def remove(hashname, field):
    r.hdel(hashname, field)

def remove_field(hashname, field, value):
    r.hdel(hashname, field, value)

## List channels
def list_hash(hashname):
    return r.hgetall(hashname)

def list_field(hashname, field):
    return r.hget(hashname, field)

