import json
from serpapi import GoogleSearch

def run_search(params):
    search = GoogleSearch(params)
    response = search.get_dict()
    return response

def main():
    params = {
        "engine": "google",
        "q": "Tango With Django",
        "cc": "US",
        "api_key": "c9b92333d3e9f7d617755077e280adfd9a06374f3dee726c8562850d09754e7b"
    }

    response = run_search(params)
    print('----------')
    for k, v in response.items():
        print(k)
    
    result_list = response['organic_results']
    for r in result_list:
     title = r['title']
     link = r['link']
     snippet = r['snippet']
     print(title)
     print(snippet)
     print(link)
     print('----------')    

    with open('search.json', 'w') as f:
        json.dump(response, f)

def read_serpapi_key():
    """
    reads the SERPAPI key from a file called 'serpapi.key'
    returns: a string which is either None, i.e. no key found, or with a key
    remember to put serpapi.key in your .gitignore file to avoid committing it.
    Below we use the "with" command when opening documents
    As recommended by the Python Anti-Patterns site, see
    http://bit.ly/twd-antipattern-open-files
    it is a really neat site for showing you how to avoid writing poor python code.
    """
    serp_api_key = None
    try:
      with open('serpapi.key','r') as f:
          serp_api_key = f.readline().strip()
    except:
      raise IOError('serpapi.key file not found')
    
    if not serp_api_key:
     raise KeyError('SerpApi key not found')

    return serp_api_key

def run_query(search_terms):
    """
    search_terms: the query string that you'd like to submit to the search engine
    See the SerpApi's documentation on other parameters that you can set.
    http://bit.ly/twd-serp-api
    returns: None or a list of results
    (where each result is a dictionary containing a title, url and snippet
    """

    key = read_serpapi_key()
    params = {
     "engine": "duckduckgo",
     "q": search_terms,
     "cc": "US",
     "api_key": key
    }
    search = GoogleSearch(params)
    response = search.get_dict()
    results = None
    if 'organic_results' in response:
     results = response['organic_results']

    return results

# 👇 THIS GOES AT THE VERY BOTTOM (outside all functions)
if __name__ == "__main__":
    main()