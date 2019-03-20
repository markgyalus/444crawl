from requests_html import HTMLSession
import logging

'''Log setup'''
article_logger = logging.getLogger(__name__)
article_logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s\t%(funcName)s\t%(asctime)s\t%(name)s\t%(message)s')

article_handler = logging.FileHandler('_article_class.log', encoding='utf-8')
article_handler.setFormatter(formatter)

article_logger.addHandler(article_handler)

''''''

class Article:

    def __init__(self, url, header, p, author, category):
        self.url = url
        self.header = header
        self.p = p
        self.author = author
        self. category = category

    def __str__(self):
        return (f'{self.url}\n=== {self.header} ===\n{self.p}\nby {self.author} in {self.category}\n\n')

    def get_link(self):
        return self.url

    def get_summary(self):
        return self.__str__()

    def get_full_article(self):
        try:
            r = HTMLSession().get(url=self.url)
            r = r.html.find('article', first=True)
            to_return = ''

            for p in r.find('p'):
                to_return = to_return + p.text + '\n'

            return to_return

        except Exception as e:
            article_logger.error(f'Probléma a cikk kinyerésekor:\n{e}')
            return None