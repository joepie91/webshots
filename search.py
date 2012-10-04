#!/usr/bin/python

import webshotslib, argparse

parser = argparse.ArgumentParser(description='Finds usernames for Webshots')

parser.add_argument('--resume', dest='resume', action='store', default='%',
                   help='position to resume from')

args = parser.parse_args()
options = vars(args)

users = []

alphabet = "-0123456789abcdefghijklmnopqrstuvwxyz!"
alphabet_length = len(alphabet)

current_index = 0
current_character_index = []

current_character_index.insert(0, 0)

done = False
users_count = 0
users_last_save = 0
thousands_last_save = 0
request_count = 0

if options['resume'] != "%":
	# Resuming is requested, let's load the old user list first.
	user_list = open("users4.txt", "r")
	users = user_list.readlines()
	user_list.close()
	
	users_count = len(users)
	users_last_save = users_count
	thousands_last_save = users_count / 1000
	
	# Set the current state to the requested resume point
	if options['resume'].endswith("%"):
		options['resume'] = options['resume'][:-1]
	
	current_index = len(options['resume']) - 1
	
	current_character_index = []
	
	for character in options['resume']:
		current_character_index.append(alphabet.index(character))
	
	print "Resuming from %s%% - loaded %d users ..." % ("".join([alphabet[value] for value in current_character_index]), users_count)
else:
	# Do an initial query for all the special character stuff
	results, count = webshotslib.search_query("%")
		
	# Append all users to the user list
	for user in results:
		if user not in users:
			users.append(user)
			users_count += 1

while done == False:
	query = "".join([alphabet[value] for value in current_character_index])
	request_count += 1
	results, count = webshotslib.search_query(query)
	
	# Append all new users to the user list
	for user in results:
		if user not in users:
			users.append(user)
			users_count += 1
	
	# Save the users to a file if we've had another 1000 (approximately)
	if users_count % 1000 < 100 and users_last_save != users_count and thousands_last_save != users_count / 1000:
		print "\nSaving %d users to file..." % users_count
		userfile = open("users4.txt", "w")
		userfile.write("\n".join(users))
		userfile.close()
		users_last_save = users_count
		thousands_last_save = users_count / 1000
	elif request_count % 100 == 0:
		print "Users found so far: %s" % users_count

	# Decide what to do now
	if count < 100:
		# End of this query reached
		while True:
			if current_index >= 0:
				if current_character_index[current_index] < alphabet_length - 1:
					# More characters available, move on to the next character
					current_character_index[current_index] += 1
					print "\rMoving to next character, searching at %s%% ..." % "".join([alphabet[value] for value in current_character_index]),
					break
				else:
					# Ran out of characters, move up a level
					current_character_index.pop()
					current_index -= 1
					print "\nMoved up a level, searching at %s%% ..." % "".join([alphabet[value] for value in current_character_index])
			else:
				done = True
				print "\nDone!"
				exit(0)
			
	elif results[-1].lower().startswith(query):
		# Not specific enough, we need to go a level deeper
		current_index += 1
		current_character_index.insert(current_index, 0)
		print "\nIncreasing depth, searching at %s%% ..." % "".join([alphabet[value] for value in current_character_index])
	else:
		# Re-search with the current depth, with the start of the last result
		next_character = results[-1][current_index:current_index + 1].lower()
		
		try:
			current_character_index[current_index] = alphabet.index(next_character)
		except ValueError, e:
			# The next character is not in our list of characters, so we will append it to the alphabet.
			alphabet.append(next_character)
			alphabet_length = len(alphabet)
			print "\nAdded character %s to alphabet ..." % next_character
			
		print "\rContinuing search at %s%% ..." % "".join([alphabet[value] for value in current_character_index]),

# Final save
print "\nFinal save to file: %d users" % users_count
userfile = open("users4.txt", "w")
userfile.write("\n".join(users))
userfile.close()
