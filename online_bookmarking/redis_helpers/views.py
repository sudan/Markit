import redis
from online_bookmarking.settings import HOSTNAME,PORT_NUMBER,DATABASE

class Redis:
	""" A redis helper class """ 

	def __init__(self):
		''' Create a connection with redis server and return the object '''

		self.redis_object = redis.StrictRedis(host=HOSTNAME,port=PORT_NUMBER,db=DATABASE)
	
	def next_unique_key(self,key):
		''' Increment the global key and return it '''

		return self.redis_object.incr(key)
	
	def get_value(self,key):
		'''  Get the value from a key '''

		return self.redis_object.get(key)
	
	def set_value(self,key,value):
		''' Set the value for a key '''

		self.redis_object.set(key,value)
	
	def remove_key(self,key):
		''' remove the key '''

		self.redis_object.delete(key)
	
	def add_to_set(self,key,value):
		''' Add an element to the set '''

		self.redis_object.sadd(key,value)
	
	def remove_from_set(self,key,value):
		''' Remove element from the set '''

		self.redis_object.srem(key,value)
	
	def is_member_in_set(self,key,value):
		''' Membership check in the set '''

		return self.redis_object.sismember(key,value)
	
	def members_in_set(self,key):
		''' Returns members of the set '''

		return self.redis_object.smembers(key)
	
	def total_members(self,key):
		''' Get the count in a set '''

		return self.redis_object.scard(key)
	
	def add_to_stack(self,key,value):
		''' Add element to the stack '''

		self.redis_object.lpush(key,value)

	def remove_from_stack(self,key,value):
		''' Remove element from the stack '''

		self.redis_object.lrem(key,0,value)
	
	def add_to_queue(self,key,value):
		''' Add element to the queue '''

		self.redis_object.rpush(key,value)

	def remove_from_queue(self,key,value):
		''' Remove element from the queue '''

		self.redis_object.lrem(key,0,value)
	
	def get_length(self,key):
		''' Get the length of the list  stack/queue '''

		return self.redis_object.llen(key)
	
	def get_elements_in_range(self,key,start=0,end=None):
		''' Get elements from the list given start and end indexes '''

		if end is None:
			return self.redis_object.lrange(key,start,self.get_length(key))
		else:
			return self.redis_object.lrange(key,start,end)
	
	def check_existence(self,key):
		''' Check for the existence of a key '''
		
		return self.redis_object.exists(key)


