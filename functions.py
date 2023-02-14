import requests
import time
import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from fake_useragent import UserAgent

def metadata(api_id,fields=None,show_url=False): ##проверить
	'''Gets the song's metadata or the artist's metadata, depending on the provided id. '''	
	url = 'https://genius.com/api'+api_id
	if show_url:
		print(url)
	r = requests.get(url)
	data = r.json()['response'][api_id.split('/')[1][:-1]]
	if fields is None:
		return data
	else:
		data = defaultdict(lambda:'NULL',data)
		data_out = {key:data[key] for key in fields}
		return data_out

def artist_songs(artist_id,show_url=False):
	'''Gets all the song ids, sorted by popularity'''
	song_ids = []
	next_page = 0
	base_url = 'https://genius.com/api'+artist_id+'/songs?sort=popularity&per_page=50'
	while next_page is not None:
		url = base_url+'&page='+str(next_page) if next_page!=0 else base_url
		if show_url:
			print(url)
		r = requests.get(url)
		song_ids += [song['api_path'] for song in r.json()['response']['songs']]
		next_page = r.json()['response']['next_page']
		time.sleep(2)
	return song_ids

def artists_all(show_url=False):
	'''Crawls the site for all the artists' urls'''
	artists_out = []
	letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0']
	for lett in letters:
		url = 'https://genius.com/artists-index/'+lett
		if show_url:
			print(url)
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		artists = soup.find_all(name='a',attrs={'class':"artists_index_list-artist_name"})+soup.find_all(name='ul',attrs={'class':"artists_index_list"})[1].find_all(name='a')
		artists_out += [link['href'] for link in artists]
		time.sleep(1)
	return artists_out

def available_artistsmetadata():
	'''Finds all the files of the form artists_metadata*.json 
	and reads all the artists_ids found in them'''
	artist = set([])
	available_files = [fname for fname in os.listdir('.') if (fname[:16]=='artists_metadata')&(fname.split('.')[-1]=='json')]
	for fname in available_files:
		with open(fname) as f:
			for line in f:
				try:
					data = json.loads(line)
					artist.add(data['api_path'])
				except:
					pass
	return artist,len(available_files)


def genius_url2id(url):
	'''Given the url, returns the ID (works for songs and artists'''
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	artist_id = soup.find_all(name='meta',attrs={'name':'newrelic-resource-path'})[0]['content']
	print(artist_id)
	return artist_id

def song_id2url(song_id):
	'''Given the song ID, returns the song url'''
	song_url = 'https://genius.com/api'+song_id
	#print(song_url)
	r = requests.get(song_url)
	page_url = "http://genius.com" + r.json()["response"]["song"]["path"]
	#print(page_url)
	return page_url


def song_lyrics(song_url):
	'''Given the song url, returns the lyrics.'''
	page = requests.get(song_url, headers={'User-Agent': UserAgent().chrome}).text
	html = BeautifulSoup(page, "html.parser")
	print(html[:10])
	#lyrics = html.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6.YYrds").text()
	#print(type(lyrics))
	lyrics  = html.find_all(name='div',attrs={'class':'lyrics'}).text.strip()
	print(type(lyrics))
	#lyrics-root > div.
	return lyrics

# if __name__ == '__main__':
# 	page_url = 'https://genius.com/Billy-joel-we-didnt-start-the-fire-lyrics'
# 	print(page_url)
# 	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
# 	for i,a in annotations:
# 		print(i)
# 		print(a)
# 		print('--------')

# 	song_id = '/songs/347866'
# 	page_url = song_id2url(song_id)
# 	print(page_url)
# 	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
# 	for i,a in annotations:
# 		print(i)
# 		print(a)
# 		print('--------')