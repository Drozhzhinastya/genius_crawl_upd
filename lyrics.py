# import pandas as pd
# from functions import *
# data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned.csv',encoding='utf-8')
# print(len(data))
# g = open('lyrics_log_file.tsv',mode='w')
# for i in data['Song ID'].values:
# 	try:
# 		f = open('lyrics/'+str(int(i))+'.txt',mode='w')
# 		song_id = '/songs/'+str(int(i))
# 		song_url = song_id2url(song_id)
# 		f.write(song_lyrics(song_url).encode('utf-8'))
# 		f.close()
# 	except:
# 		g.write(str(int(i))+'\n')
# g.close()

import pandas as pd
import time
from functions import *
song_ids = pd.read_csv('songs.tsv',delimiter='\t',header=None)[2]
print(len(song_ids))

g = open('lyrics_log_file.tsv',mode='w')

for i in song_ids[:1]:
	song_id = i
	#print(song_id)
	song_url = song_id2url(song_id)
	print(song_url)
	try:
		filename = 'lyrics/'+i.strip('/songs/')+'.txt'
		#print(filename)
		f = open(filename,mode='w') #файлы называются по айдишнику песен
		f.write(song_lyrics(song_url).encode('utf-8'))
		f.close()
	except:
		g.write(i.strip('/songs/')+'\n')
		# f = open(filename,mode='w') #файлы называются по айдишнику песен
		# f.write(song_lyrics(song_url).encode('utf-8'))
		# f.close()
	time.sleep(1)

g.close()