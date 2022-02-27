"""Module for interacting with a Redis database"""
import redis

r = redis.Redis(host='redis', port=6379)

def add(hashname, field, value):
    """Adds a field:value pair to a hash"""
    r.hset(hashname, field, value)

def remove(hashname, field):
    """Removes field from a hash"""
    r.hdel(hashname, field)

def remove_field(hashname, field, value):
    """Removes a value from a field in a hash"""
    r.hdel(hashname, field, value)

def list_hash(hashname):
    """Lists al the fields/values in a hash"""
    return r.hgetall(hashname)

def list_field(hashname, field):
    """Lists the value of a field in a hash"""
    return r.hget(hashname, field)
