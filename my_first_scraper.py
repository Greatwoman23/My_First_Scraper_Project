import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    return requests.get(url)

def extract(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all('article')

def transform(html_repos):
    result = []
    for i in html_repos:
        number_of_stars = ' '.join(i.select_one('span.float-sm-right').text.split())
        repository_name = ' '.join(i.select_one('h1').text.split())
        try:
            developer_name = i.select_one('img.avatar.mb-1.avatar-user')['alt']
        except (AttributeError, TypeError):
            'None name'
        result.append({'developer': developer_name, 'repository_name': repository_name, 'nbr_stars': number_of_stars})
    return result

def format(repositories_data):
    columns_names = ['Developer, Repository_ame, Number of Stars']
    for repository in repositories_data:
        dictionary_list = [repository['developer'], repository['repository_name'], repository['nbr_stars']]
        columns_names.append(', '.join(dictionary_list))
    return '\n'.join(columns_names)

def run():
    url = 'https://github.com/trending'
    page = request_github_trending(url)
    html_repos = extract(page)
    repositories_data = transform(html_repos)
    github_trending = format(repositories_data)

