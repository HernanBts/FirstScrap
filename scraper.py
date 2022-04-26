import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.infobae.com'

XPATH_ARTICLE_LINKS = '//a[@class="cst_ctn"]/@href'
XPATH_TITLE = '//h1[@class="article-headline"]/text()'
XPATH_SUMMARY = '//h2[@class="article-subheadline"]/text()'
XPATH_BODY = '//article[@class="article"]/div/p[not(last)]//text()'

def parse_article(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            article = response.content.decode('utf-8')
            parsed = html.fromstring(article)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summery = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summery)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')   
        else: 
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_articles = parsed.xpath(XPATH_ARTICLE_LINKS)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_articles:
                link = f'{HOME_URL}{link}'
                # print(link)
                parse_article(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()
