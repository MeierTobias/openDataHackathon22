import pandas as pd




def from_csv_with_coordinates(filename): #, **kwargs

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
		

def from_csv_glas(filename): #, **kwargs

	#with open(filename, 'r') as f:
	#	data = f.readlines()
		

	with open(filename, 'r') as f:
		data = pd.read_csv(f, sep=';')
		
	header = list(data) #data.pop(0)
	
	print(data)

	if 'geo_point_2d' in header:
		#i_loc = header.index('Location')
		
		#df['loc'] = data['Location']
		df = pd.DataFrame()
		df[['lon', 'lat']] = data['geo_point_2d'].str.split(',', 1, expand=True)
		df["braun"] = [1 if "Braun" in ele else 0 for ele in data["Tags"]]
		df["green"] = [1 if "GrÃ¼n" in ele else 0 for ele in data["Tags"]]
		df["white"] = [1 if "Weiss" in ele else 0 for ele in data["Tags"]]

		df['value'] = 1
		
	elif 'Geo Point' in header:
		df = pd.DataFrame()
		df[['lon', 'lat']] = data['Geo Point'].str.split(',', 1, expand=True)
		df['value'] = 1
		
	else:
		raise ValueError('no Location found in dataset')
		
	
	print(df)
	
	return df
		

	
	
	
	