'''
This script imports and refactors the data
'''
import pandas as pd


def from_csv_with_coordinates(filename):

    with open(filename, 'r') as f:
        data = pd.read_csv(f, sep=';')

    header = list(data)

    if 'Location' in header:
        df = pd.DataFrame()
        df[['lat', 'lon']] = data['Location'].str.split(',', 1, expand=True)
        df['value'] = 1
    elif 'Geo Point' in header:
        df = pd.DataFrame()
        df[['lat', 'lon']] = data['Geo Point'].str.split(',', 1, expand=True)
        df['value'] = 1
    else:
        raise ValueError('no Location found in dataset')

    print(df)

    return df


def from_csv_glas(filename):  # , **kwargs

    with open(filename, 'r') as f:
        data = pd.read_csv(f, sep=';')

    header = list(data)

    if 'geo_point_2d' in header:
        df = pd.DataFrame()
        df[['lat', 'lon']] = data['geo_point_2d'].str.split(
            ',', 1, expand=True)
        df['sensorname'] = data['Sensorname']
        df["braun"] = [1 if "Braun" in ele else 0 for ele in data["Tags"]]
        df["green"] = [1 if "GrÃ¼n" in ele else 0 for ele in data["Tags"]]
        df["white"] = [1 if "Weiss" in ele else 0 for ele in data["Tags"]]

        df = df.drop_duplicates('name')

        gk = data.groupby('Sensorname')
        stationen = gk.groups.keys()
        print(len(stationen), ' stationen')
        mengen = {}
        for group_name, gk_group in gk:
            d = pd.DataFrame()
            device_id = group_name
            # , format='%d%b%Y:%H:%M:%S.%f')
            d['time'] = pd.to_datetime(gk_group['Gemessen am'])
            d['f'] = gk_group['FÃ¼llstandsdistanz']
            d.sort_values(by='time', inplace=True)

            d['d'] = d['f'].diff(periods=1)
            d.dropna()
            d.reset_index(drop=True)

            menge = -sum([a for a in d['d'].to_list() if a < 0])
            mengen.update({group_name: menge})
            print(group_name, menge)
    else:
        raise ValueError('no Location found in dataset')

    df['menge'] = df['name'].map(mengen)
    df.to_csv('glassammelstellen.tsv', sep=';', index=False)

    print(df)

    return df
