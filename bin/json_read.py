#converts a json result file to a list format that can be fed to Graphite
#follows the format 'environment.table_id.product_name.name value time\n'
from time_convert import to_unix


def to_graphite(jlines):

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
				#print jlines[i+step][19:38] #time
				
				if jlines[i+step+1].find('"t_added"') > 0:
					t_added = True
					#print jlines[i+step+2][21:-1] #value with "t_added"
					message.append(jlines[i+step+2][21:-1]) #add value to message
				else:
					t_added = False
					#print jlines[i+step+1][21:-1] #value
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
			#print jlines[i][17:-2]
			#print name_start, end
			for x in range(name_start, end):
				message[x] = jlines[i][17:-2] + ' ' + message[x] #add name to message
			name_start = end
		
		if jlines[i].find('"table_id"') > 0 and data:
			#print jlines[i][17:22]
			for x in range(table_start, end):
				message[x] = jlines[i][17:22] + '.' + message[x] #add table_id to message
			
		if jlines[i].find('"product_name"') > 0 and data:
			#print jlines[i][21:-2]
			for x in range(table_start, end):
				message[x] = message[x][:5] + '.' + jlines[i][21:-2] + message[x][5:] #add product_name to message
			table_start = end

	return message

def add_env(env, glines):
	for line in range(len(glines)):
		glines[line] = env + '.' + glines[line]
	return glines
			
def main():
	#test output
	jfile = 'result_2015-02-19.json'
	env = 'PR'
	
	with open(jfile, "r") as jin, open('test_format.txt', "w") as gout:
		gout.writelines(add_env(env, to_graphite(jin.readlines())))
	
	print 'successful'
	
if __name__ == "__main__":
	main()