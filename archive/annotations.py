import pandas as pd
from functions import song_id2url, song_annotations
song_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[2])

outfile = open('songs_annotations.tsv',mode='w', encoding='utf-8')
g = open('songs_annotations_log_file.tsv',mode='w',  encoding='utf-8')

for song_id in list(song_ids)[:10]:
    try:
        song_url = song_id2url(song_id)
        print(song_url)
        #print(song_id)
        annotation_ids = song_annotations(song_url)
        #print(len(annotation_ids))
        for annotation_id in annotation_ids:
            print(annotation_id)
            #outfile.write(song_url+'\t'+song_id+'\t'+annotation_id+'\n')
            
    except:
        g.write(song_id+'\n')
        

g.close()
outfile.close()