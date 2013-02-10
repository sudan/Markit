import redis
from online_bookmarking.settings import HOSTNAME,PORT_NUMBER,DATABASE


def create_connection():
	return redis.StrictRedis(host=HOSTNAME,port=PORT_NUMBER,db=DATABASE)

def get_value(redis_object,key):
	return redis_object.get(key)

def set_value(redis_object,key,value):
	redis_object.set(key,value)

#still more helper functions to come....
