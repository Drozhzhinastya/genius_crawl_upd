# genius_crawl

Crawler for genius

## Description of files:

get_songs.py

```
Retrieves a list of all the songs from genius and saves it to songs.tsv as:
artist_url	artist_id	song_id
```

songs_metadata.py

```
Retrieves the metadata for all the songs in songs.tsv and saves it to songs_metadata.json.
If a songs_metadata.json file already exists, it will ommit the songs in it and save the new songs to songs_metadata1.json.
```

artists_metadata.py

```
Retrieves the metadata for all the artists in songs.tsv and saves it to artists_metadata.json.
If a artists_metadata.json file already exists, it will ommit the artists in it and save the new artists to artists_metadata1.json.
```

annotations.py
```
Retrieves all the annotation ids for all the songs in songs.tsv and saves it to songs_annotations.tsv as:
song_url	song_id	annotation_id
```

annotations_content.py

```
Retrieves the content for all the annotations in songs_annotations.tsv and saves it as independent .tsv files (one for each song, with the song_id as the file name) in the folder annotations. (The character "\n" is replaced by "|" in the field annotation_content)
Each file has the format:
annotation_id	annotation_content
```

languages.py
```
Open the file 'processed_data/data_song_annotation_merged_20170815.csv' and adds two new columns: lang and is_null.
lang: Language detected using langdetect package
is_null: Boolean, if True the annotations are broken
```

lyrics.py
```
Opens the file 'processed_data/data_song_annotation_merged_20170815_cleaned.csv' and gets the lyrics for the songs in the column Song ID. 
It saves them as independent .txt files inside the 'lyrics' folder, with the name of the file being the Song ID.
```

classifier.py
```
Uses the training data in 'processed_data/songs_training.csv' to train an SVM classifier to clean the data. I then classifies all the songs available in 'processed_data/data_song_annotation_merged_20170815_cleaned.csv' adding a new column with the probability of the entry being a valid song. It finally saves the results into 'processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv'.
```

bow.py
```
Gets all the annotations for songs (prob>.5) from 'processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv' and splits them into individual annotations. It then turns every annotation into a bag of words using nltk (see cleanfunctions.py for functions). Finally, it saves the bag of words representation for each annotation into a picle file 'processed_data/texts.p' and into .txt file 'processed_data/texts.txt'. The pickle file is a list of lists and the .txt file has words separated by ' ' in each line.
```

topic_model.py
```
Reads the pickle object from 'processed_data/texts.p' and uses it to train two topic models, one using NMF and the other using LDA. To run it:
>>> python topic_model.py no_topics no_features

To load the models run:
>>> no_topics = 20
>>> no_features = 1000
>>> [tf,tf_vectorizer,lda] = pickle.load(open("processed_data/lda_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
>>> tf_feature_names = tf_vectorizer.get_feature_names()
>>> [tfidf,tfidf_vectorizer,nmf] = pickle.load(open("processed_data/nmf_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
>>> tfidf_feature_names = tfidf_vectorizer.get_feature_names()
```

explore_topics.py
```
This script is not meant to be run, but rather to be copied and pasted in a notebook.

Loads the topic model, and draws the word distribution for each one of them.
```

song2topics.py
```
This script is not meant to be run, but rather to be copied and pasted in a notebook.

Loads the topic model and the annotations, then it gets the lyrics for a given song and decomposes both the lyrics and the annotations into topics.
```

search_artist.py
```
Takes the list of all the artists in 'processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv' (with prob>=0.5) and tries to link them to their Wikipedia page using johnny5.

The results are written in 'processed_data/artist2wiki.tsv' with the following format:
	Primary Artist\tPrimary Artist ID\tWiki Title\twdid\tL\tinstance_of
```

artist_origin.py
```
Takes the list of all the artists' Wikipedia pages from 'processed_data/artist2wiki.tsv' and gets their place of origin using four possible different fields:
formation: Wikidata property P740
work_location: Wikidata property P937
birth_place: Wikidata property P19
residence: Wikipedia infobox type 'person' field
origin: Wikipedia infobox type 'musician' or 'musical artist' field

The results are written in 'processed_data/artist_origin.tsv' with the following format:
	'Primary Artist\tPrimary Artist ID\tWiki Title\ttag\tPlace Wiki Title\tlat\tlon'
where 'tag' corresponds to which type of field it corresponds to.
```

artist_msa.py
```
Takes the origins of all the artists from 'processed_data/artist_origin.tsv' and maps them to a US Metropolitan Statistical Area.

The results are written in 'processed_data/artist_origin_msa.csv' with the following format:
	'Primary Artist,Primary Artist ID,Wiki Title,tag,Place Wiki Title,ccode2,msa_name,msa_id,dusa_id'
where 'msa_id' corresponds to the MSA id, and 'dusa_id' corresponds to the MSA id used in DataUSA.
```

msa2topics.py
```
Takes the results of the topic model and breaks every song into topics. It then aggregates by MSA to assign topics to cities.

The results are written in:
	'processed_data/topic2words_modeltype_no_topics_no_features.csv': Table that maps topics to songs (topic,word,prob)
	'processed_data/songs2topics_modeltype_no_topics_no_features.csv': Table that maps Song ID to topic (Song ID,topic,pa)
	'processed_data/msa2topics_modeltype_no_topics_no_features.csv': Table that maps MSA to topic (NAME,topic,pa)
```