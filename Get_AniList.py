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
            description
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
    id_dict = {}
    media = json_result["data"]["Page"]["media"]
    for i in range(len(media)):
        id_dict[media[i]["id"]] = {}
        id_dict[media[i]["id"]]["title"] = media[i]["title"]
        id_dict[media[i]["id"]]["description"] = media[i]["description"]
    return id_dict


def fuzzy_compare(id_dict, search_str):
    curr_highest = {}  # simple list to hold id and similarity rate
    curr_highest["id"] = 0
    curr_highest["ratio"] = -1
    # look through all the ids
    for id in id_dict:
        # look through each name in id ie. romaji or english
        for titles in id_dict[id]["title"].values():
            if titles is not None:
                ratio = fuzz.token_sort_ratio(search_str.lower(),
                                              titles.lower())
                if ratio > curr_highest["ratio"]:
                    curr_highest["name"] = titles
                    curr_highest["id"] = id
                    curr_highest["ratio"] = ratio
    curr_highest["description"] = id_dict[curr_highest["id"]]["description"]
    return curr_highest


def search(search):
    variables = {
        'search': search
    }
    response = requests.post(api_url, json={'query': query,
                                            'variables': variables})
    json_dict = json.loads(response.text)
    info = fuzzy_compare(data_to_dict(json_dict), search)
    link = url + str(info["id"])
    ans = {}
    ans["link"] = link
    ans["name"] = info["name"]
    ans["description"] = info["description"].replace("<br>", "")
    print(len(ans["description"]))

    return ans


if __name__ == "__main__":
    print(search("bakemonogatari"))
