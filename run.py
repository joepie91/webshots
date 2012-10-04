#!/usr/bin/python
import webshotslib, time

to_parse = []
to_parse_count = 0
users = []
users_count = 0
users_last_save = 0

print "Starting...",

for category in webshotslib.get_category_listings("http://community.webshots.com/"):
	to_parse.append(category)
	to_parse_count += 1
	print "\rTotal pages to be parsed: %d" % to_parse_count,
	
	for listing_page in webshotslib.get_user_listings(category):
		to_parse.append(listing_page)
		to_parse_count += 1
		print "\rTotal pages to be parsed: %d" % to_parse_count,
		
	time.sleep(0.5)

print ""

for listing_page in to_parse:
	for user in webshotslib.get_users(listing_page):
		if user not in users:
			users.append(user)
			users_count += 1
			print "\rUsers found: %d" % users_count,
			
			if users_count % 1000 < 100 and users_last_save != users_count:
				userfile = open("users.txt", "w")
				userfile.write("\n".join(users))
				userfile.close()
				users_last_save = users_count
	time.sleep(0.5)
