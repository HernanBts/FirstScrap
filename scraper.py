import requests
import lxml.html as html

HOME_URL = 'https://www.infobae.com/'

XPATH_ARTICLE_LINKS = '//a[@class="cst_ctn"]/@href'
XPATH_TITLE = '//h1[@class="article-headline"]/text()'
XPATH_SUMMARY = '//h2[@class="article-subheadline"]/text()'
XPATH_BODY = '//article[@class="article"]/div/p[not(last)]//text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_articles = parsed.xpath(XPATH_ARTICLE_LINKS)
            print(links_to_articles)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()
