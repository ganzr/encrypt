#!/usr/bin/env python
# -*- coding: utf-8 -*-     
class DES(object):
	"""docstring for DES"""
	def __init__(self):
		super(DES, self).__init__()
	
	def des_encode(self,from_string,key):
		#if the length of the from_string is not the times of 16, add 0
		bin_string = self.stringToBin(from_string)
		str_len = len(bin_string)
		while str_len%64 != 0:
			bin_string = bin_string + '00000000'
			str_len += 8
		print bin_string
		self.run_keyi = []
		key = self.stringToBin(key)
		key_len = len(key)
		while(key_len%64 != 0):
			key = key + '10011001'
			key_len +=8
		if key_len>64:
			kk = self.stringToBin('ganz')
			for k in range(64,key_len,32):
				kk =self._or_permutation(key[k:k+32],kk,32)
			key = self._or_permutation(key[0:64],kk+kk,64)
		#use the former 56bit as key
		self._key_generate(key)
		output = ''
		for i in range(0,str_len,64):
			from_code = bin_string[i:i+64]
			#IP置换
			from_code = self._ip(from_code)
			L = from_code[0:32]
			R = from_code[32:64]
			#16 round encode
			for j in range(16):
				e_R = self._extend_permutation(R)
				or_R = self._or_permutation(e_R,self.run_keyi[j],48)
				s_R = self._s_box_permutation(or_R)
				p_R = self._p_permutation(s_R)
				temp_R = self._or_permutation(p_R,L,32)
				L = R
				R = temp_R
			to_code = R + L
			to_code = self._ip1(to_code)
			output = output + to_code
		return output
	def des_decode(self,from_string,key):
		str_len = len(from_string)
		output = ''
		if(str_len%64!=0):
			return false
		self.run_keyi = []
		key = self.stringToBin(key)
		key_len = len(key)
		while(key_len%64 != 0):
			key = key + '10011001'
			key_len +=8
		if key_len>64:
			kk = self.stringToBin('ganz')
			for k in range(64,key_len,32):
				kk =self._or_permutation(key[k:k+32],kk,32)
			key = self._or_permutation(key[0:64],kk+kk,64)
		#use the former 56bit as key
		self._key_generate(key)
		for i in range(str_len/64):
			from_code = from_string[64*i:64*i+64]
			from_code = self._ip(from_code)
			L = from_code[32:64]
			R = from_code[0:32]
			for j in range(16):
				e_L = self._extend_permutation(L)
				or_L = self._or_permutation(e_L,self.run_keyi[15-j],48)
				s_L = self._s_box_permutation(or_L)
				p_L = self._p_permutation(s_L)
				temp_L = self._or_permutation(p_L,R,32)
				R = L
				L = temp_L
			to_code = L + R
			to_code = self._ip1(to_code)
			output = output + to_code
		print output
		output = self.binToString(output)
	 	return output

	def _key_rotate(self,input,bit):
		output = input[1:] + input[0]
		if(bit==2):
			output = output + input[1]
		return output
	def _key_generate(self,input):
		p_key = ''
		for i in range(56):
			p_key = p_key + input[self.pc1[i]-1]
		for i in range(16):
			l_key = self._key_rotate(p_key[0:28],self.loop_table[i]) + self._key_rotate(p_key[28:56],self.loop_table[i])
			p_key = l_key
			p2_key = ''
			for j in range(48):
				p2_key = p2_key + l_key[self.pc2[j]-1]
			self.run_keyi.append(p2_key)
		return 0
	def _ip(self,input):
		output = ''
		for i in range(64):
			output = output + input[self.ip[i]-1]
		return output
	def  _ip1(self,input):
		output = ''
		for i in range(64):
			output = output + input[self.ip_1[i]-1]
		return output
	def _extend_permutation(self,input):
		output = ''
		for i in range(48):
			output = output + input[self.e_table[i]-1]
		return output
	def _s_box_permutation(self,input):
		#s盒压缩置换，48bit到32bit
		output = ''
		for i in range(8):
			instring = input[6*i:6*i+6]
			row = instring[0] + instring[5]
			row = int(row,2)
			col = int(instring[1:5],2)
			val = self.s_box[i][row][col]
			bin_str = str(bin(val))[2:]
			while len(bin_str)<4:
				bin_str = '0'+bin_str
			output = output + bin_str
		return output
	def _p_permutation(self,input):
		output = ''
		for i in range(32):
			output = output + input[self.p_table[i]-1]
		return output

	def _or_permutation(self,str1,str2,length):
		out = ''
		for i in range(length):
			out = out + str(int(str1[i])^int(str2[i]))
		return out
	def stringToBin(self,string):
		return_string = ''
		for s in string:
			hex_string = '%02x'%ord(s)
			binString = bin(int(hex_string,16))
			binString = binString[2:]
			while len(binString) != 8:
				binString = '0' + binString
			return_string = return_string + binString
		return return_string
	def binToString(self,binString):
		return_string = ''
		length = len(binString)
		for i in range(0,length,8):	
			val = int(binString[i:i+8],2)
			return_string = return_string + chr(val)
		return unicode(return_string,'utf-8')
	run_keyi = []
	ip = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9 , 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]
	ip_1 = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41,  9, 49, 17, 57, 25]
	e_table = [32, 1,  2,  3,  4,  5,  4,  5, 
       6, 7,  8,  9,  8,  9, 10, 11, 
      12,13, 12, 13, 14, 15, 16, 17,
      16,17, 18, 19, 20, 21, 20, 21,
      22, 23, 24, 25,24, 25, 26, 27,
      28, 29,28, 29, 30, 31, 32,  1]
	p_table = [16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10, 
     2,  8, 24, 14, 32, 27,  3,  9,
     19, 13, 30, 6, 22, 11,  4,  25]
	pc1 = [57, 49, 41, 33, 25, 17,  9,
       1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27,
      19, 11,  3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29,
      21, 13,  5, 28, 20, 12, 4]
	pc2 = [14, 17, 11, 24,  1,  5,  3, 28,
      15,  6, 21, 10, 23, 19, 12,  4, 
      26,  8, 16,  7, 27, 20, 13,  2, 
      41, 52, 31, 37, 47, 55, 30, 40, 
      51, 45, 33, 48, 44, 49, 39, 56, 
      34, 53, 46, 42, 50, 36, 29, 32]
	loop_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
	s_box=[ [[14, 4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
     [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
     [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],    
     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],

     [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],     
     [3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],     
     [0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],     
     [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],

     [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],     
     [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],   
     [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],     
     [1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],

    [[7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11,  12,  4, 15],     
     [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,9],     
     [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],     
     [3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],


    [[2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],     
     [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],     
     [4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],     
     [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],

    [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
     [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],     
     [9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],     
     [4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],

    [[4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],     
     [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],     
     [1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],     
     [6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],

   [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],     
     [1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],     
     [7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],     
     [2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]]
#convert string to binary bit stream
