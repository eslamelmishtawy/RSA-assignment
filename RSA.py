import random
import time
from tkinter import *

def gcd(a,b):
	while b != 0:
		a,b = b, a%b
	return a
	
def generateLargePrime(keysize=512):
    # Return a random prime number of keysize bits in size.
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num

def inverse(a,b):

	x = 0
	y = 1
	lx = 1
	ly = 0
	oa = a
	ob = b
	while b != 0:
		q = a // b
		(a, b) = (b, a % b)
		(x, lx) = ((lx - (q * x)), x)
		(y, ly) = ((ly - (q * y)), y)
	if lx < 0:
		lx += ob
	if ly < 0:
		ly += oa
	return lx

def rabinMiller(num):
	# Returns True if num is a prime number.
	print("fails")
	s = num - 1
	t = 0
	while s % 2 == 0:
		# keep halving s while it is even (and use t
		# to count how many times we halve s)
		s = s // 2
		t += 1

	for trials in range(5): # try to falsify num's primality 5 times
		a = random.randrange(2, num - 1)
		v = pow(a, s, num)
		if v != 1: # this test does not apply if v is 1.
			i = 0
			while v != (num - 1):
				if i == t - 1:
					return False
				else:
					i = i + 1
					v = (v ** 2) % num
	return True	
	
def generateKeys(p,q):
	n = p*q
	phi = (p-1)*(q-1)
	e = random.randrange(1, phi)
	
	g = gcd(e,phi)
	while g != 1:
		e = random.randrange(1, phi)
		g = gcd(e,phi)
	d = inverse(e,phi)
	return((e,n),(d,n))
		
def isPrime(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabinMiller().

	if (num < 2):
		return False # 0, 1, and negative numbers are not prime

    # About 1/3 of the time we can quickly determine if num is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabinMiller(), but unlike rabinMiller() is not guaranteed to
    # prove that a number is prime.
	lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
	103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
	229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
	367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
	503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
	653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
	821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971,
	977, 983, 991, 997]

	if num in lowPrimes:
		return True

    # See if any of the low prime numbers can divide num
	for prime in lowPrimes:
		if (num % prime == 0):
			return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
	
	return rabinMiller(num)
		
def squareAndMultiply( a, k, n):
	r = 1
	bits = list(bin(k)[2:])
	for bit in bits:
		r = (r * r) % n
		if int(bit) == 1:
			r = (r * a) % n
	return r
		
def encrypt(kpub, plaintext):
	key, n = kpub
	key = int(key)
	n = int(n)
	ciphertext = [squareAndMultiply(ord(char),key,n) for char in plaintext]
	return ciphertext

def decrypt(kpr, ciphertext):
	key, n = kpr
	key = int(key)
	n = int(n)
	plaintext = [chr((squareAndMultiply(char, key,n)))for char in ciphertext]
	return "".join(plaintext)
	
def generateCommand():
	p = generateLargePrime()
	q = generateLargePrime()
	public, private = generateKeys(p, q)
	t1.delete(1.0, END)
	t2.delete(1.0, END)
	t1.insert(INSERT,public)
	t2.insert(INSERT,private)

	
def encryptedMsgGetter():
	public = tuple(t1.get(1.0,END).split(' '))
	encrypted_msg = encrypt(public, e1_value.get())
	return encrypted_msg
def encryptCommand():
	t3.delete(1.0, END)
	t3.insert(INSERT,encryptedMsgGetter())

def decryptCommand():
	private = tuple(t2.get(1.0,END).split(' '))
	decryptedMessage = decrypt(private, encryptedMsgGetter())
	t4.delete(1.0, END)
	t4.insert(INSERT,decryptedMessage)	
	
window = Tk()

b1 = Button(window, text = "Generate", command=generateCommand)
b1.grid(row=6,column=0)
b2 = Button(window, text = "Encrypt", command=encryptCommand)
b2.grid(row=6,column=1)
b3 = Button(window, text = "Decrypt", command=decryptCommand)
b3.grid(row=6,column=2)


l1 = Label(window, text = "Enter a Message you want to send and press generate")
l1.grid(row=0,column=0)

l1 = Label(window, text = "Message before Encryption")
l1.grid(row=1,column=0)

e1_value = StringVar()
e1 = Entry(window, textvariable=e1_value)
e1.grid(row=1, column=1)

l2 = Label(window, text = "'p'")
l2.grid(row=2,column=0)

t1 = Text(window,height = 4, width = 40)
t1.grid(row=2,column=1)

l3 = Label(window, text = "'q'")
l3.grid(row=3,column=0)

t2 = Text(window,height = 4, width = 40)
t2.grid(row=3,column=1)

l4 = Label(window, text = "Encrypted Message")
l4.grid(row=4,column=0)

t3 = Text(window,height = 4, width = 40)
t3.grid(row=4,column=1)

l5 = Label(window, text = "'Message after decryption'")
l5.grid(row=5,column=0)

t4 = Text(window,height = 1, width = 40)
t4.grid(row=5,column=1)

window.mainloop()
	
