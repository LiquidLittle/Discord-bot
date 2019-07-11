import requests
import json
from fuzzywuzzy import fuzz


def getTitles(request):
    titles = []
    titles.append(request.get('title_english'))
    titles.append(request.get('title_romaji'))
    return titles


# Here we define our query as a multi-line string
query = '''
query ($search: String) {
    Page {
        media(search: $search, type: ANIME) {
            id
            title {
                romaji
                english
            }
        }
    }
}
'''

api_url = 'https://graphql.anilist.co'
url = 'https://anilist.co/anime/'


def data_to_dict(json_result):
    ''' Returns a dictionary of the json query with id as the key and the
        title as the value
    '''
    id_title_dict = {}
    media = json_result["data"]["Page"]["media"]
    for i in range(len(media)):
        id_title_dict[media[i]["id"]] = media[i]["title"]
    return id_title_dict


def fuzzy_compare(id_title_dict, search_str):
    curr_highest = [0, -1]  # simple list to hold id and similarity rate
    for id in id_title_dict:
        list = []
        for titles in id_title_dict[id].values():
            if titles is not None:
                list.append(fuzz.token_sort_ratio(search_str.lower(),
                                                  titles.lower()))
            else:
                list.append(0)
        highest = max(list)
        if highest >= curr_highest[1]:
            curr_highest[0] = id
            curr_highest[1] = highest
    return curr_highest[0]


def search(search):
    variables = {
        'search': search
    }
    response = requests.post(api_url, json={'query': query,
                                            'variables': variables})
    json_dict = json.loads(response.text)
    id = fuzzy_compare(data_to_dict(json_dict), search)
    link = url + str(id)
    return link


if __name__ == "__main__":
    print(search("kimi no nawa"))
