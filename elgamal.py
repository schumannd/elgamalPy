
import sys
import random

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
	if len(sys.argv) < 4:
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

if __name__ == "__main__":
	main()
