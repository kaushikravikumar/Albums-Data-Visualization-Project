import json
import requests
import csv

GET_ALBUM_IDS = "https://api.spotify.com/v1/search"
GET_ALBUMS = "https://api.spotify.com/v1/albums"
GET_ARTIST = "https://api.spotify.com/v1/artists/"

# OAuth Token must be constantly refreshed!!
OAuth_Token = "BQAtdMHTKC5N6Kk7WqhJXHlDZPhOPe7P5yk-jnrVOw85nL-BntMU8ON5eyHq9nv6-Ho-xd_a0MwJBaJicm1U9N7bhfj7wpJ0ZFkFdwbePf1Vng4kjBFLAWa1YWFmLHSDyut9yR-1OEX5nQdjIg"
header = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': "Bearer " + OAuth_Token }

albumIds = []

albumData = []

def encodeSpaces(str):
    return str.replace(" ", "%20")

def fetch_json():
    with open('./data/filtered_pitchfork.json') as json_file:  
        data = json.load(json_file)
    data = data["objects"][0]["rows"]

    for i in range(len(data)):
        getAlbumIDRequest(data[i][1], data[i][2])

    global albumIds
    albumIds = [albumIds[20*i:20*(i+1)] for i in range(len(albumIds) / 20 + (len(albumIds) % 20 > 0))]
    albumIdsStr = map(lambda x : ','.join(x), albumIds)
    for ids in albumIdsStr:
        getAlbumDataRequest(ids)

def getAlbumIDRequest(title, artist):
    r = requests.get(GET_ALBUM_IDS + "?" + "q=" + encodeSpaces(title + " " + artist) +
    "&type=album&market=US&limit=1", headers= header)
    try:
        data = r.json()
    except ValueError:
        print(r)
        return

    if(('albums' in data) and len(data['albums']['items']) > 0):
        data = data['albums']['items'][0]['id']
        albumIds.append(data)
        print('found')
    else:
        print('couldntfind')

def getArtistGenre(id):
    r = requests.get(GET_ARTIST + id, headers=header)
    data = r.json()
    return data['genres']
    

def getAlbumDataRequest(ids):
    r = requests.get(GET_ALBUMS + "?" + "ids=" + ids + "&market=US", headers=header)
    try:
        data = r.json()
    except:
        print(r)

    for i in range(len(data['albums'])):
        albumName = data['albums'][i]['name']
        albumPop = data['albums'][i]['popularity']
        albumReleaseDate = data['albums'][i]['release_date']
        albumNumTracks = data['albums'][i]['total_tracks']
        albumLabel = data['albums'][i]['label']

        artistId = data['albums'][i]['artists'][0]['id']
        artistName = data['albums'][i]['artists'][0]['name']
        albumGenres = getArtistGenre(artistId)
        albumData.append({"title": albumName, "artist": artistName , "pop": albumPop, "genres": albumGenres,
        "release_date": albumReleaseDate, "label": albumLabel, "numTracks": albumNumTracks})
        print("added")

    print(albumData)

def filterPitchforkData():
    with open('./data/filtered_pitchfork_data.csv', 'rb') as inp, open('./data/more_filtered_pitchfork_data.csv', 'wb') as out:
        writer = csv.writer(out)
        with open('./data/popularity_data.json') as json_file2:
            spotify_data = json.load(json_file2)
            for row in csv.reader(inp):
                found = False
                for j in range(len(spotify_data)):
                    if row[1].lower() in spotify_data[j]['title'].lower() and row[2].lower() in spotify_data[j]['artist'].lower():
                        found = True
                    if row[1].lower() in spotify_data[j]['title'].lower() and spotify_data[j]['artist'].lower() in row[2].lower():
                        found = True
                    if spotify_data[j]['title'].lower() in row[1].lower() and spotify_data[j]['artist'].lower() in row[2].lower():
                        found = True
                    if spotify_data[j]['title'].lower() in row[1].lower() and row[2].lower() in spotify_data[j]['artist'].lower():
                        found = True
                    
                if found == True:
                    writer.writerow(row)
                else:
                    print(row)


if __name__ == '__main__':
    # USED TO FETCH THE POPULARITY_DATA JSON FILE
    
    # fetch_json()
    # with open('./data/popularity_data.json', 'w') as fout:
    #     json.dump(albumData, fout)

    # _______________________________________________________________________________________________

    # USED TO FILTER PITCHFORK DATA TO ONLY INCLUDE THOSE VALUES IN POPULARITY_DATA JSON FILE

    # filterPitchforkData()


            

