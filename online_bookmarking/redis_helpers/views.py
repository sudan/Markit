import redis
from online_bookmarking.settings import HOSTNAME,PORT_NUMBER,DATABASE

class Redis:
	""" A redis helper class """ 

	#Create a connection with redis server and return the object
	def __init__(self):
		self.redis_object = redis.StrictRedis(host=HOSTNAME,port=PORT_NUMBER,db=DATABASE)

	#Increment the global key and return it
	def next_unique_key(self,key):
		return self.redis_object.incr(key)

	#Get the value from a key
	def get_value(self,key):
		return self.redis_object.get(key)

	#Set the value for a key
	def set_value(self,key,value):
		self.redis_object.set(key,value)

	#Add an element to the set
	def add_to_set(self,key,value):
		self.redis_object.sadd(key,value)

	#Remove element from the set
	def remove_from_set(self,key,value):
		self.redis_object.srem(key,value)

	#Membership check in the set 
	def is_member_in_set(self,key,value):
		return self.redis_object.sismember(key,value)

	#Returns members of the set
	def members_in_set(self,key):
		return self.redis_object.smembers(key)

	#Add element to the stack
	def add_to_stack(self,key,value):
		self.redis_object.lpush(key,value)

	#Add element to the queue
	def add_to_queue(self,key,value):
		self.redis_object.rpush(key,value)

	#Get the length of the list  stack/queue
	def get_length(self,key):
		return self.redis_object.llen(key)

	#Get elements from the list given start and end indexes
	def get_elements_in_range(self,key,start=0,end=None):
		if end is None:
			return self.redis_object.lrange(key,start,self.get_length(key))
		else:
			return self.redis_object.lrange(key,start,end)



