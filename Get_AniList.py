import requests
import json


def getTitles(request):
    titles = []
    titles.append(request.get('title_english'))
    titles.append(request.get('title_romaji'))
    return titles


# Here we define our query as a multi-line string
query = '''
query ($search: String) {
  Media (search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
  }
}
'''

api_url = 'https://graphql.anilist.co'
url = 'https://anilist.co/anime/'


def search(search):
    variables = {
        'search': search
    }
    response = requests.post(api_url, json={'query': query,
                                            'variables': variables})
    json_dict = json.loads(response.text)
    id = json_dict["data"]["Media"]["id"]
    link = url + str(id)
    return link
