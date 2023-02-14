import json,pandas as pd
from functions import metadata,available_artistsmetadata
import time

artist_ids = pd.read_csv('songs.tsv',delimiter='\t',header=None)
artist_ids = set(artist_ids[artist_ids.columns[1]])

fields = ['followers_count','alternate_names','name','url','api_path','twitter_name']

artists,nfiles = available_artistsmetadata()
artist_ids = artist_ids.difference(artists)

outfile = open('artists_metadata.json',mode='wb') if nfiles==0 else open('artists_metadata'+str(nfiles+1)+'.json',mode='wb')
g = open('artists_metadata_log_file.tsv',mode='w') if nfiles==0 else open('artists_metadata_log_file'+str(nfiles+1)+'.tsv',mode='w')

for artist_id in artist_ids:
	try:
		data_out = metadata(artist_id,fields)
		outfile.write((json.dumps(data_out)+'\n').encode('utf-8'))
	except:
		g.write(artist_id+'\n')
	time.sleep(1)
	
outfile.close()
g.close()