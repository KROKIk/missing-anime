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

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjI3ZDhjZWRjZmQ3MGYyZDdjNTMzNmEzNjcxYzk5Yzk5NGU5MjM0OWQ4NmVlOGQ4MjQzNzE0MGViYjNiN2YyNjVkYzkyZjdhZmY5YjFiMDA5In0.eyJhdWQiOiIzMDY3IiwianRpIjoiMjdkOGNlZGNmZDcwZjJkN2M1MzM2YTM2NzFjOTljOTk0ZTkyMzQ5ZDg2ZWU4ZDgyNDM3MTQwZWJiM2I3ZjI2NWRjOTJmN2FmZjliMWIwMDkiLCJpYXQiOjE2NDc4MDQ1MTcsIm5iZiI6MTY0NzgwNDUxNywiZXhwIjoxNjc5MzQwNTE3LCJzdWIiOiIzODY4MjYiLCJzY29wZXMiOltdfQ.fclDoDFQg7eax-xi4kIKs84B-4Z9-nv0OYDJnnFp4FHcJgu1Txg1ALkrSLKviKeiEQg0Zu9S8_zVslcgGa7DsdoqSK6ar4XHkIGRwWR2d_kEdj96rTu6kM7sgmiTWnwV0dn4IRVsNfTAYW5cQ5Mfwdi4WNC8bWSCeRzqOdnNPhy54XnHvwCDVP6v_Ui82-ZDS2QnZWGn33Z0Ku8x0N9DWd0dkbPQ2MxdJLU2to8DAGHPtnu4etnXvERXHVh1zOFA-TTgD0Qr7HZh8joWZO3s7F6mBKGgMtDuy0iXXMRXuRjJnOuR3D6iyX4tM023QzXO-1Wm5X-pTxC7ZWF6F53X7GtcPkFxMDtusSzly4M16tMkEBAEpwHLESFW5Bex1ONyzEPwlPZC3jZcdqBMR5kFIDEHk4OcJRfuhzJePmsiJtq-EiZzOdw41oo1QrUYrCx1idbXw2oFF7lQ7htFJumF_ZNinJJlRmb3wVMUxia1GciBiHCETIk8RzKzYMTVMJWMHg5Dhd3gWA0rygtj6wiLWyNXorIzDAn_ywk2Z20q7I3Aa0D39XtYqnGXaWPzvZsQxLH2s9z1awDG3BfBFgeMC5MZgPBewNgUfFy-eJzTwxRRpPijFHpRpdypn_-p0-FNbn36jLyDHCtdfAAwjA316WNvAdGL0YbimwFyibEfFfo"
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
