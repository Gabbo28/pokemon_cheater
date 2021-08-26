
#https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_I)#bank1_main_rival

import sys
import os


dictionary = {'A': 0x80, 'B': 0x81, 'C' : 0x82 , 'D': 0x83, 'E': 0x84, 'F': 0x85, 'G':0x86, 'H':0x87, 
			  'I':0x88, 'J':0x89, 'K':0x8a, 'L':0x8b, 'M':0x8c, 'N':0x8d, 'O':0x8e, 'P':0x8f, 
			  'Q':0x90, 'R':0x91, 'S':0x92, 'T':0x93, 'U':0x94, 'V':0x95, 'W':0x96, 'X':0x97,
			  'Y':0x98, 'Z':0x99, '(':0x9a, ')':0x9b, ':':0x9c, ';':0x9d, '[':0x9e, ']':0x9f,
			  'a':0xa0, 'b':0xa1, 'c':0xa2, 'd':0xa3, 'e':0xa4, 'f':0xa5, 'g':0xa6, 'h':0xa7,
			  'i':0xa8, 'j':0xa9, 'k':0xaa, 'l':0xab, 'm':0xac, 'n':0xad, 'o':0xae, 'p':0xaf,
			  'q':0xb0, 'r':0xb1, 's':0xb2, 't':0xb3, 'u':0xb4, 'v':0xb5, 'w':0xb6, 'x':0xb7, 
			  'y':0xb8, 'z':0xb9 }

def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

#def parse_lendian(array):



def fix_ceck():
	
	checksum = 0xff

	for c in ram[0x2598:0x3523] :
		checksum -= c

	ram[0x3523]=checksum&0xff # modulo 256!

	file.seek(0,0)
	file.write(ram)
	file.close()

	checksum=hex(checksum&0xff)
	print(f"Written checksum: {checksum}\n")

def money():

	#offset= 0x25f3 size 0x3

	pos=sys.argv.index("--money")

	if len(sys.argv) > pos+1 and is_int(sys.argv[pos+1]) :


		cash=sys.argv[pos+1].zfill(6) #padding cash with zeroes, 6 char total, as string
		
		
		#money = ram[0x25f3:0x25f6]
		
		sum = [int("0x"+cash[i:i+2], base=16) for i in range(0,6,2)] # alternativa bruta a BCD decoding
		
		#print(list(sum))
		#print(list(ram[0x25f3:0x25f6]))  ---debug stuff
		
		ram[0x25f3:0x25f6] = sum
		
		#print(list(ram[0x25f3:0x25f6]))


		print(f"You selected the wallet-fixing option :)\nNow the player has {cash}$, enjoy!\n")


		

	else :
		print("Input an amount between 0 and 999999 !\n")
		exit()


def myname(s):

	#player offset= 0x2598 size 0xb, always ends with 0x50
	#enemy  offset= 0x25f6 size 0xb, always ends with 0x50

	if s == "player":
		offset = 0x2598
		opt = "--myname"
	elif s == "rival":
		offset = 0x25f6
		opt = "--riv-name"
	elif s == "pokemon":
		offset = 0x307e
		opt = "--poke-name"


	pos=sys.argv.index(opt)
	
	if len(sys.argv) > pos+1:	
	
		#print(f"Changing name to {sys.argv[pos+1]}.\n")

		name=sys.argv[pos+1]

		if len(name)>7:
			print("The name's max length is 7 characters!")
			exit()

		chars=[ dictionary[c] for c in name]+[0 for j in range(0,7-len(name))]+[0x50] #padding chars with zeroes, 7 char total, as array
		
		#print(list(ram[0x2598:0x259f]))
		
		ram[offset:offset+0x8]=chars
		#print(list(ram[0x2598:0x259f]))
		print(f"You selected the change-your-name option :)\nNow the {s} is called {name}, enjoy!\n")

	else :
		print("Input a name!")
		exit()

def exp():

	# first party pokemon structure offset: 0x2f2c

	offset = 0x2f42
	opt = "--exp"

	pos=sys.argv.index(opt)

	if is_int(sys.argv[pos+1]) == False or int(sys.argv[pos+1])>16777215:
		print(f"You must enter a number between 1 and 0xffffff=16777215...but be reasonable plz")
		exit()


	exp = format(int(sys.argv[pos+1]), 'x').zfill(6)

	arr = [int("0x"+exp[i:i+2], base=16) for i in range(0,6,2)]

	#print(f"changing exp of first pokemon to {list(arr)}")

	ram[offset:offset+0x3]= arr

	print(f"You selected the change-exp option :)\n"
		f"This changes the experience points of the first pokemon of you list to {sys.argv[pos+1]}, enjoy!\n")

def main():

	file = open(sys.argv[1], 'rb+')
	
	ram = bytearray(file.read())


	print(f"\nWelcome {os.getlogin().title()}, this is the patching tool for Gen-1 GBC Pokemon games!\n")
	
	if "--money" in sys.argv:
		
		money()


	if "--myname" in sys.argv:
		
		myname("player")
		

	if "--riv-name" in sys.argv:
		
		myname("rival")

	if "--exp" in sys.argv:
		
		exp()
		
	fix_ceck()

def usage():

    print("Usage : python3 pokepatch.py  [file.sav] [options]\n"
    	"Options : --myname [name]    : change player name\n"
    	      "\t  --riv-name [name]  : change rival name\n"    			   
    	      "\t  --money [0-999999] : change money quantity\n"
    		  "\t  --exp [1-16777215] : change experience points of first pokemon\n")

def init_arg():

    if len(sys.argv) < 2: 

        usage()

        exit() 




#---main---



init_arg()

main()




