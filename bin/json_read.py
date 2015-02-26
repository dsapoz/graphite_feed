#conversion for json to graphite
from time_convert import to_unix, trend_time


def result_to_graphite(jlines):
	#converts a json result file to a list format that can be fed to Graphite
	#follows the format 'table_id.product_name.name value time\n'

	message = list()
	t_added = '' #indicates presence of "t_added"
	name_start = 0
	table_start = 0
	end = 0
	data = '' #indicates if table has data

	for i in range(len(jlines)):
		if table_start == end: #data set to False if table has just ended
			data = False

		if jlines[i].find('"data"') > 0:	
			data = True
			step = 1
			
			while jlines[i+step].find(']') < 0:
				step += 2	
				
				if jlines[i+step+1].find('"t_added"') > 0:
					t_added = True
					message.append(jlines[i+step+2][21:-1]) #add value to message
				else:
					t_added = False
					message.append(jlines[i+step+1][21:-1]) #add  value to message
					
				if jlines[i+step].find('"_t"') > 0:
					message[end] += ' ' + str(to_unix(jlines[i+step][19:38])) + '\n' #add time to message
				
				if t_added:
					step += 4
				else:
					step += 3
				
				end += 1
		
		if jlines[i].find('"name"') > 0 and data:
			jlines[i] = jlines[i].replace(".", "_") #replaces decimals (from 0.7, 0.75, etc) to match graphite format
			for x in range(name_start, end):
				message[x] = jlines[i][17:-2] + ' ' + message[x] #add name to message
			name_start = end
		
		if jlines[i].find('"table_id"') > 0 and data:
			for x in range(table_start, end):
				message[x] = jlines[i][17:22] + '.' + message[x] #add table_id to message
			
		if jlines[i].find('"product_name"') > 0 and data:
			for x in range(table_start, end):
				message[x] = message[x][:5] + '.' + jlines[i][21:-2] + message[x][5:] #add product_name to message
			table_start = end

	return message

def trend_to_graphite(jlines):
	#converts a json trend file to a list format that can be fed to Graphite
	#follows the format 'table_id.trend.product_name.name.day value time\n'
	#where all times are for the day 1/1/2015
	
	message = list()
	name_start = 0
	table_start = 0
	table_id = ''
	end = 0
	data = '' #indicates if table has data

	for i in range(len(jlines)):
		if table_start == end: #data set to False if table has just ended
			data = False
			
		if jlines[i].find('"table_id"') > 0:
			table_id = jlines[i][17:22]

		if jlines[i].find('"data"') > 0:	
			data = True
			step = 1
			
			while jlines[i+step].find(']') < 0:
				step += 2
				
				message.append(jlines[i+step+4][20:-2]) #add day to message
				message[end] += ' ' + jlines[i+step+1][21:-2] #add value to message	
				message[end] += ' ' + str(trend_time(jlines[i+step][19:-3])) + '\n' #add time to message
				
				step += 6
				end += 1
		
		if jlines[i].find('"name"') > 0 and data:
			jlines[i] = jlines[i].replace(".", "_") #replaces decimals (from 0.7, 0.75, etc) to match graphite format
			for x in range(name_start, end):
				message[x] = jlines[i][17:-2] + '.' + message[x] #add name to message
			name_start = end
			
		if jlines[i].find('"product_name"') > 0 and data:
			for x in range(table_start, end):
				message[x] = table_id + '.trend.' + jlines[i][21:-2] + '.' + message[x] #add table_id, trend and product_name to message
			table_start = end

	return message

def add_env(env, glines):
	for line in range(len(glines)):
		glines[line] = env + '.' + glines[line]
	return glines
			
def main():
	#test output
	jfile = 'A0101_PR_trend.json'
	env = 'PR'
	
	with open(jfile, "r") as jin, open('test_format.txt', "w") as gout:
		gout.writelines(add_env(env, trend_to_graphite(jin.readlines())))
	
	print 'successful'
	
if __name__ == "__main__":
	main()