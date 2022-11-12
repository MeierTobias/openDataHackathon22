import pandas as pd




def from_csv_with_coordinates(filename):

	#with open(filename, 'r') as f:
	#	data = f.readlines()
		

	with open(filename, 'r') as f:
		data = pd.read_csv(f, sep=';')
		
	header = list(data) #data.pop(0)

	if 'Location' in header:
		#i_loc = header.index('Location')
		
		#df['loc'] = data['Location']
		df = pd.DataFrame()
		df[['lon', 'lat']] = data['Location'].str.split(',', 1, expand=True)
		df['value'] = 1
	elif 'Geo Point' in header:
		df = pd.DataFrame()
		df[['lon', 'lat']] = data['Geo Point'].str.split(',', 1, expand=True)
		df['value'] = 1
		
	else:
		raise ValueError('no Location found in dataset')
		
	
	print(df)
	
	return df
		

	
	
	