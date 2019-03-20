import requests_html as req
import os
import logging
from classes import Article

'''LOG SETUP'''
crawl_logger = logging.getLogger(__name__)
crawl_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s')

crawl_handler = logging.FileHandler('_crawler.log', encoding='utf-8')
crawl_handler.setFormatter(formatter)

crawl_logger.addHandler(crawl_handler)

''''''

def crawl_444():
    '''
    A függvény felkeresi a 444.hu-t és legyűjti a főoldalon elérhető cikkeket Article objektumként.
    :return: list(Article)
    '''
    sess = req.HTMLSession()
    r = sess.get('https://444.hu')

    articles_collection = []
    articles = r.html.find('article')

    for article in articles:
        header = None
        p = None
        author = None
        category = None
        url = None

        try:
            header = article.find('header', first=True).text
        except Exception as e:
            crawl_logger.error(f'Probléma a fejléc begyűjtésekor:\n{e}')

        try:
            p = article.find('p', first=True).text
        except Exception as e:
            crawl_logger.error(f'Probléma az alcím begyűjtésekor:\n{e}')

        try:
            footer = article.find('footer', first=True)
            footer = footer.find('div')
            footer = [foot for foot in footer if foot.attrs.get('class') == ('byline__info',)][0]
            for item in footer.find('span'):
                if item.attrs.get('class') == ('byline__authors',):
                    author = item.text
                if item.attrs.get('class') == ('byline__category',):
                    category = item.text
        except Exception as e:
            crawl_logger.error(f'Probléma a szerző/kategória begyűjtésekor:\n {e}')

        for link in article.absolute_links:
            if link.find('444.hu/2019') > 0 and link.find('#comments') == -1:
                url = link

        articles_collection.append(Article(url, header, p, author, category))

    return articles_collection


def save_articles_by_category(articles_collection, url_list_file, save_summary=True):

    try:
        with open(url_list_file, 'r+', encoding='utf-8') as url_list:
            already_collected_urls = url_list.readlines()
            orig_cwd = os.getcwd()

            for item in articles_collection:

                if (item.get_link() + '\n') not in already_collected_urls:

                    crawl_logger.info(f'{item.get_link()} legyűjtve')

                    if save_summary:
                        with open('category-save_test_444_short_collection.txt', 'a', encoding='utf-8') as sum_file:
                            sum_file.write(item.get_summary())

                    url_list.write(item.get_link() + '\n')
                    os.chdir(f'{orig_cwd}\\data')
                    try:
                        os.chdir(f'{item.category.upper()}')
                    except Exception:
                        os.makedirs(f'{item.category.upper()}')
                        os.chdir(f'{item.category.upper()}')
                    finally:
                        with open(f'{item.url.split("/")[-1]}.txt', 'w', encoding='utf-8') as full_article_file:
                            full_article_file.write(item.get_full_article())

                    os.chdir(orig_cwd)

                else:
                    crawl_logger.info(f'!!!\t{item.get_link()} már korábban le lett gyűjtve!')
    except Exception as e:
        crawl_logger.error(f'HIBA:\n{e}')

def main():

    print('A program elindult')
    cikkek = crawl_444()
    save_articles_by_category(cikkek, 'category-save_test_url_list.txt')
    print('A futás véget ért')


if __name__ == '__main__':

    main()