#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import random
class RSA(object):
	"""docstring for RSA"""
	def __init__(self,nbit):
		super(RSA, self).__init__()
		#self.generate_key(nbit)
	#Miller_Rabin 素数检测
	def Miller_Rabin(self,p,trials=5):
		#ues to tell whether p is prime number
		assert p>=2
		if p==2:
			return 1
		if p%2 == 0:
			return 0
		s = 0
		d = 1
		a = random.randint(1,p-1)
		while p%2==0:
			s += 1
			p = p/2
			d = p
		while trials>1:
			for r in range(s):
				if a**d%p != 1 and a**(2**r*d)%p != -1:
					return 0
			trials -= 1
		return 1
	#随机数生成
	def generate_prime(self,n):
		while 1:
			p = self._generate_prime(n)
			if p!=0:
				return p
	def _generate_prime(self,n):
		# generate a random prime number
		p = random.randint(10**(n-1),10**n-2)
		# add 1 if it is odd
		if p%2==0:
			p+=1
		# produce the former 400 prime number
		k = reduce(lambda a, x: all(x % t for t in a) and a.append(x) or a, xrange(2, 10000), [])
		while p<10**n:
			flag = 1
			# calculate p/ki to simplify the generation
			for i in k:
				if p==i:
				 continue
				if p%i==0:
					flag = 0
					break
			if flag==1:
				if self.Miller_Rabin(p):
					return p
				else:
					p+=2
			else:
				p+=2
		return 0
	def generate_key(self,nwei):
		p1 = self.generate_prime(nwei)
		p2 = self.generate_prime(nwei)
		while p2==p1:
			p1 = self.generate_prime(nwei)
			p2 = self.generate_prime(nwei)
		n = p1*p2
		fi = (p1-1)*(p2-1)
		#choice e
		prime = reduce(lambda a, x: all(x % t for t in a) and a.append(x) or a, xrange(2, 10000), [])
		e = random.choice(prime)
		while fi%e==0:
			e = random.choice(prime)
		[d,k,q] = self.ext_euclid(e,fi)
		d = d%n;
		self.pub_key = [n,e]
		self.pri_key = [n,d]
	def ext_euclid (self,a , b):
		#扩展阿基里德算法计算模反元素
		if b == 0:
			return 1, 0, a
		else:
			x,y,q = self.ext_euclid(b,a%b)
			x,y = y,(x-(a//b)*y)
			return x, y, q
	def rsa_encode(self,fromstring):
		ustring = fromstring.decode('utf-8')
		n = self.pub_key[0]
		e = self.pub_key[1]
		tostring = u''
		for i in range(len(ustring)):
			m = ord(ustring[i])
			c= str(m**e%n)+','
			tostring = tostring + c
		return tostring.encode('utf-8')
	def rsa_decode(self,fromstring):
		marr = fromstring.split(',')
		[n,d] = self.pri_key
		tostring = u''
		for s in marr[:-1]:
			c = int(s,10)
			m = c**d%n
			tostring = tostring + unichr(m)
		return tostring.encode('utf-8')
	def rsa_encodewithkey(self,fromstring,key1,key2):
		self.pub_key = [key1,key2]
		ustring = fromstring
		n = int(self.pub_key[0],10)
		e = int(self.pub_key[1],10)
		tostring = u''
		for i in range(len(ustring)):
			m = ord(ustring[i])
			c= str(m**e%n)+','
			tostring = tostring + c
		print 1
		return tostring.encode('utf-8')
	def rsa_decodewithkey(self,fromstring,key1,key2):
		self.pri_key = [int(key1),int(key2)]
		marr = fromstring.split(',')
		[n,d] = self.pri_key
		tostring = u''
		for s in marr[:-1]:
			c = int(s,10)
			m = c**d%n
			tostring = tostring + unichr(m)
		return tostring.encode('utf-8')
	pub_key = [89773,7349]#public key 
	pri_key = [89773,4025]#private key