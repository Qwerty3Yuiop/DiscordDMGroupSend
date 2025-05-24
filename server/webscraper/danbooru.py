import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_html(http:str):
    r = requests.get(http)  
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_post(soup:BeautifulSoup):
    target_link = soup.find('a', class_='post-preview-link')

    if not target_link:
        return ""
    
    post_link = target_link.get("href")
    if not post_link:
        return ""
    
    post_link:str = post_link.split('?')[0]
    return "https://danbooru.donmai.us" + post_link

def get_post_tags(soup:BeautifulSoup):
    tags_ul = soup.find("ul", class_="general-tag-list")
    tag_entries = tags_ul.find_all("a", class_="search-tag")
    if tag_entries:
        return [tag_item.get_text() for tag_item in tag_entries]
    
def format_link(link:str):
    known_links = {
        'x.com':'source:https://twitter.com',
        'twitter.com': 'source:https://twitter.com',
        'pixiv.com': 'pixiv:'
    }

    link = link.removeprefix("https://")
    link = link.removeprefix("http://")
    domain = link.split('/')[0]

    if domain in known_links:
        link = known_links[domain]+ "/" + "/".join(link.split('/')[1:])
        return 'https://danbooru.donmai.us/posts?tags=' + quote(link, safe="")
    
    else:
        return ""
        
def search_and_get_link_tags(link:str):
    soup = get_html(link)
    post = get_post(soup)
    if not post:
        return "", []
    soup = get_html(post)
    tags = get_post_tags(soup)
    if not tags:
        return post, []
    return post, tags

if __name__ == "__main__":
    link = format_link("https://twitter.com/palizyok/status/1904168220363272638")
    print(link)
    soup = get_html(link)
    post = get_post(soup)
    print(post)
    soup = get_html(post)
    tags = get_post_tags(soup)
    print(tags)