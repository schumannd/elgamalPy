#!/usr/bin/python
from Point import Point
import sys
import random

def decryptHomeWork(cypherfile):
	p = 211287523889848166456771978073530465593093161450010064509303400255860514422619
	a = 102112374625719848836417645466897582644268266380360636462856219195606277562091
	cypherArray = []
	cleartext = ""
	with open(cypherfile, "r") as textFile:
		for line in textFile:
			x = line.split(',')
			cypherArray.append(Point(int(x[0]),int(x[1])))
	for cypherPoint in cypherArray:
		cleartext += chr(decrypt(cypherPoint.x, cypherPoint.y, a, p))
	print cleartext

def decrypt(c1, c2, a, p):
	sharedSecret = pow(c1, a, p)
	return (c2 * modularInverse(sharedSecret, p)) % p

def special_pow( a, b, m):
	if b == 0:
		return 1
	elif not b & 1:
		y = special_pow( a, b/2, m)
		z = pow(y, 2, m)
		if z == 1 and y != 1 and y != m-1:
			return 0
		else:
			return z
	else:
		y = special_pow( a, b-1, m)
		z = pow( a*y, 1, m)
		return z

def is_prime( m, confidence):
	while confidence > 0:
		# miller's Test
		a = random.randrange( 1, m-1)
		if special_pow(a, m, m) != a:
			return False

		confidence -= 1
	return True

def random_prime( bitlength, confidence ):
	lower = pow(2, bitlength-1)
	upper = pow(2, bitlength) - 1

	p = random.randrange(lower, upper)
	while not is_prime(p, confidence):
		p = random.randrange(lower, upper)

	return p

def random_safe_prime( bitlength, confidence ):
	while True:
		q = random_prime( bitlength - 1, confidence)
		p = 2*q + 1
		if  is_prime(p, confidence):
			return p

def random_generator( p):
	q = (p - 1)/2

	while True:
		g = random.randrange(2, p-2 )
		if ( pow(q, 2, p) != 1 and pow(g, q, p) != 1):
			return g


def main():
	if len(sys.argv) == 2:
		# case specific decryption
		decryptHomeWork(sys.argv[1])
	if len(sys.argv) < 5:
		print "usage: <prime-bit-length> <confidence> <pub-key filename> <sec-key filename>"
		return

	bitlength = int(sys.argv[1])
	confidence = int(sys.argv[2])
	pubkeyfile = open(sys.argv[3])
	seckeyfile = open(sys.argv[4])

	p = random_safe_prime( bitlength, confidence)
	g = random_generator( p)
	#a = random.randrange( (p-1)/2, p - 2)
	a = random.randrange( 1, p - 2)
	b = pow(g, a, p)

	print "p = ", p
	print "g = ", g
	print "b = ", b
	print "a = ", a

	#TODO: write to files

	pubkeyfile.close()
	seckeyfile.close()

############# copy pasted from my other projects because lazyness
def pulverizer(a, b): # a > b
	x1, y1, x2, y2 = 1, 0, 0, 1
	while b != 0:
		q, r = a//b, a%b
		x, y = x1 - q*x2, y1 - q*y2
		a, b, x1, y1, x2, y2 = b, r, x2, y2, x, y
		# print str(q)+", "+str(r)+", "+str(a)+", "+str(b)+", "+str(x1)+", "+str(y1)+", "+str(x2)+", "+str(y2)
	return a, x1, y1

def modularInverse(e, phi):
	g, x, y = pulverizer(e, phi)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % phi

if __name__ == "__main__":
	main()
