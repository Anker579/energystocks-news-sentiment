from trafilatura import fetch_url, extract

def get_fulltext(url):
    page = fetch_url(url)
    ft = extract(page)
    return ft