import requests
from settings import API_KEY, CX
import click
import pandas as pd
import arrow

"""
This quick program is a command line interface to searching google. You'll need to get an API key from Google,
so you can programmatically search.

Example:

>>> python google_searcher.py "John Connelly"

That will search for John Connelly.
"""

def basic_google_search(query, start=1):

    u = r'https://www.googleapis.com/customsearch/v1'

    params = {
        'cx': CX,
        'q': query,
        'key': API_KEY,
        'start': start
    }

    r = requests.get(u, params=params)
    return r.json()


def google_search(query, pages=5):
    results = []
    formatted_results = []
    urls = []
    cnt = 1
    dbl = 0
    for p in range(pages):

        if p == 0:
            p = 1
        else:
            p *= 10

        google_results = basic_google_search(query, start=p)
        items = google_results.get('items')
        if items is not None:
            for ix, res in enumerate(items):
                res['query'] = query
                results.append(res)
                # print(res.keys())
                link = res.get('link')
                htmlFormattedUrl = res.get('htmlFormattedUrl')
                htmlSnippet = res.get('htmlSnippet')
                formattedUrl = res.get('formattedUrl')
                htmlTitle = res.get('htmlTitle')
                kind = res.get('kind')
                displayLink = res.get('displayLink')
                title = res.get('title')
                cacheId = res.get('cacheId')
                snippet = res.get('snippet')
                pagemap = res.get('pagemap')

                if link not in urls:
                    urls.append(link)
                    formatted_results.append([title, link, snippet, query])
                    cnt += 1
                else:
                    dbl += 1

    return results, formatted_results


@click.command()
@click.option('--search', help='Enter your search term...')
@click.option('--pages', default=2, help="The number of pages you'd like to return...")
@click.option('--url', default=False, help="Type True if you want the url instead of the title...")
def main(search, pages, url):
    results, formatted_results = google_search(search, pages=pages)
    click.echo('Searching for {}...'.format(search))
    for row in formatted_results:
        print_item = row[0]
        if url:
            print_item = row[1] # url
        try:
            print('\t', print_item)
        except UnicodeDecodeError:
            pass

    df = pd.DataFrame(formatted_results, columns=['search_title', 'search_url', 'search_blurb', 'search_term'])
    writer = pd.ExcelWriter('search_results_{}.xlsx'.format(arrow.now().format('MMDDYYYY_hhmmss')))
    df.to_excel(writer)


if __name__ == '__main__':
    main()