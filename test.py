try:
	x = 1
	y = 0
	try: print(x/y)
	except Exception: print("first divide by zero")
	print(x/y)
except Exception: print("second divide by zero")
