import argparse

from driver import Driver

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Snipe some classes.')

	parser.add_argument('username', type=str, help='an integer for the accumulator')	
	parser.add_argument('password', type=str, help='an integer for the accumulator')

	args = parser.parse_args()

	d = Driver(args.username, args.password)
	d.start()


