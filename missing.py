import requests
import json
from time import sleep
url = 'https://graphql.anilist.co'

media_id = list()

query = '''
query ($id: String, $page: Int) { # Define which variables will be used in the query (id)
  Page (perPage: 50, page: $page) { 
    mediaList (userName: $id, status: COMPLETED, type: ANIME) {
      mediaId
    }
  }
}
'''

token = "INSERT TOKEN HERE"
head = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + token,
  }


for n in range(10):
    variables = {
        'id': "KROKIk",
        'page': n,
    }
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    json_obj = json.loads(response.text)["data"]["Page"]["mediaList"]
    if not json_obj:
        break
    for mediaid in json_obj:
        media_id.append(mediaid)

ids =  list(set([id["mediaId"] for id in media_id]))

relations = set()
for id in ids:
    query = '''
               query ($id: Int) {
                 Media (id: $id) { 
                   relations {
                       nodes {
                           id
                       }
                   }
                 }
               }
               '''

    variables = {
        'id': id
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=head)
    json_obj = json.loads(response.text)["data"]["Media"]["relations"]["nodes"]
    for id in json_obj:
        relations.add(id["id"])
    sleep(0.5)


data = relations


for id in data:
    query = '''
               query ($id: Int) {
                    Media (id: $id) {
                        type 
                        mediaListEntry {
                            status
                        }
                    }
                }
               '''

    variables = {
        'id': id
    }

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=head)
    try:
        json_obj = json.loads(response.text)["data"]["Media"]["mediaListEntry"]
        json_obj2 = json.loads(response.text)["data"]["Media"]["type"]
    except TypeError:
        print("ERROR: id")
        continue
    print(json_obj, json_obj2)

    if json_obj == None and json_obj2 == "ANIME":
        query = '''
                mutation ($mediaId: Int, $status: MediaListStatus) {
                    SaveMediaListEntry (mediaId: $mediaId, status: $status) {
                        id
                        status
                    }
                }
               '''
        variables = {'mediaId': id, "status": "PLANNING"}

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=head)
        
        print(id)
    sleep(1)
