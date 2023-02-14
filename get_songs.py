from functions import artists_all,  genius_url2id, artist_songs, song_id2url
import time 
from tqdm import tqdm

start = time.time() ## точка отсчета времени

f = open('songs.tsv', mode='w', encoding='utf-8')
g = open('songs_log_file.tsv', mode='w')

artists = artists_all()

for a_url in tqdm(artists):
	try:
		a_id = genius_url2id(a_url)
		songs = artist_songs(a_id)
		for s in songs:
			song_url = song_id2url(s)
			f.write(a_url+'\t'+a_id+'\t'+s+'\t'+song_url+'\n')
	except:
		g.write(a_url+'\n')
		f.write(a_url+'\t'+a_id+'\t'+s+'\t'+song_url+'\n')
	time.sleep(1)

f.close()
g.close()


end = time.time() - start ## собственно время работы программы

print(end) ## вывод времени