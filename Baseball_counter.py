import re
import sys, os
import operator

if len(sys.argv) < 2:
	sys.exit("Usage: &s filename" % sys.argv[0])

filename = sys.argv[1]

if not os.path.exists(filename):
	sys.exit("Errot: File '%s not found" % sys.argv[1])

group_regex = re.compile(r"(\w+ \w+) batted (\d) times with (\d) hits and \d runs")
def get_stats(str):
	match = group_regex.match(str)
	if match is not None:
		return (match.group(1), match.group(2), match.group(3))
	else:
		return False

player_stats = {}

f = open(filename)
for line in f:
	rline = line.rstrip()
	if get_stats(rline):
		name, bat, hit = get_stats(rline)	
		if name in player_stats:
			tup = player_stats[name]
			bat_num = int(tup[0]) + int(bat)
			hit_num = int(tup[1]) + int(hit)
			tup_update = (bat_num, hit_num)
			player_stats[name] = tup_update
		else:
			player_stats[name] = (int(bat), int(hit))
f.close()

# print player_stats
hit_rates = {}
for name in player_stats:
	tup = player_stats[name]
	bat_num = int(tup[0])
	hit_num = int(tup[1])
	avg = round(float(hit_num)/float(bat_num), 3)
	hit_rates[name] = avg
sorted_rates = sorted(hit_rates.items(), key=operator.itemgetter(1), reverse = True)
for name,avg in sorted_rates:
	print name, ": ", '{0:.3f}'.format(avg)
