import asyncio
import json
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup


async def get_page(session, url):
    async with session.get(url) as resp:
        return await resp.text(), url


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data


def get_xml_page(results):
    xml_links = []
    for html in results:
        soup = BeautifulSoup(html[0], 'html.parser')
        for link in soup.findAll('a', href=True):
            if 'rss' in link['href']:
                if len(link['href']) < 20:
                    xml_links.append(html[1] + link['href'].replace('/', '', 1))
                else:
                    xml_links.append(link['href'])
    return list(set(xml_links))


def parse_xml_to_json(request):
    dct = {}
    for req in request:
        soup = BeautifulSoup(req[0], 'html.parser')

        # https://www.phoronix.com/rss.php
        # https://www.theverge.com/rss/index.xml
        # https://www.engadget.com/rss.xml
        # https://es.gizmodo.com/rss
        titles = [title.text for title in soup.find_all('title')[1:11]]

        if soup.find_all('pubDate'):
            pub_dates = [datetime.fromisoformat(pub_date.text).strftime('%Y-%m-%d %H:%M')
                         for pub_date in soup.find_all('pubDate')[1:11]]
        elif soup.find_all('pubdate'):
            try:
                # https://www.phoronix.com/rss.php
                # https://www.engadget.com/rss.xml
                pub_dates = [datetime.strptime(pub_date.text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
                         for pub_date in soup.find_all('pubdate')[1:11]]
            except ValueError:
                # https://es.gizmodo.com/rss
                pub_dates = [datetime.strptime(pub_date.text, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')
                             for pub_date in soup.find_all('pubdate')[1:11]]
        else:
            # https://www.theverge.com/rss/index.xml
            pub_dates = [datetime.fromisoformat(pub_date.text).strftime('%Y-%m-%d %H:%M')
                         for pub_date in soup.find_all('published')[0:10]]

        try:
            # https://www.theverge.com/rss/index.xml
            links = [link['href'] for link in soup.find_all('link')[1:11]]
        except KeyError:
            links = []
            if soup.find_all('link') and soup.find_all('link')[1].decode() == '<link/>':
                for link in soup.find_all('link')[1:11]:
                    if 'Read more...' in link.fetchNextSiblings()[0].text:
                        # https://es.gizmodo.com/rss
                        start_link_str = link.fetchNextSiblings()[0].text.find('<p><a href="') + len('<p><a href="')
                        end_link_str = link.fetchNextSiblings()[0].text.find('">Read')
                        links.append(link.fetchNextSiblings()[0].text[start_link_str:end_link_str])
                    else:
                        # https://www.engadget.com/rss.xml
                        # https://www.phoronix.com/rss.php
                        links.append(link.next.strip())

        for index_dt, date in enumerate(pub_dates):
            for index_tit, title in enumerate(titles):
                for index_link, link in enumerate(links):
                    dct[date] = {'title': title, 'link': link}
                    if index_dt == index_link:
                        break
                if index_tit == index_dt:
                    break

    with open('feeds.json', 'w') as json_file:
        json.dump(dct, json_file, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    urls = ['https://www.theverge.com/',
            'https://www.phoronix.com/',
            'https://es.gizmodo.com/',
            'https://www.engadget.com/']

    results = asyncio.run(main(urls))
    xml_pages = get_xml_page(results)
    req = asyncio.run(main(xml_pages))
    parse_xml_to_json(req)
