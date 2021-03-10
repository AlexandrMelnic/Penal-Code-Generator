import requests
from bs4 import BeautifulSoup


'''
The structure of the wiki page to crawl is:
    libro1:
        titolo1
            text
        titolo2
            text
           ... 
           ...
           ...
    libro2:
       ...   
       ...
       ...

'''

class WebScraper:
    '''
        After instantiating the class use the method return_scraped_pages
        to get the full text. The text is saved in the path specified as 
        input parameter.
        The class uses Beautifoul soup to perform the scraping.
    '''

    def __init__(self, PATH):

        self.wiki_link = 'https://it.wikisource.org'
        self.PATH = PATH

    def get_soup(self, link):

        '''
            Given a specific link returns the soup object.
        '''

        link = self.wiki_link + link
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "lxml")
        return soup

    def get_links(self, link):

        '''
            Method that allows to enter in the different sections titolo1, titolo2,... 
            given the link of the current node.

        '''

        soup = self.get_soup(link)
        links = []
        for elem in soup.find('div', {'class':'testi diritto'}).find_all('li'):
            links.append(elem.find('a', href=True)['href'])
        return links

    def get_texts(self, link):

        '''
            Given the link of one section this method gets the texts defined
            by the tag <p>, <h3> and <dd>.

        '''
        soup = self.get_soup(link)
        texts = []
        for elem in soup.find('div', {'class':'testi diritto'}).find_all(['h3','p', 'dd']):
            texts.append(elem.text)
        return texts
        
    def save_scraped_pages(self):

        file = open(self.PATH, 'w')

        '''
            Get all the texts for all sections and save in file.

        '''
        text = []
        for link in self.get_links('/wiki/Codice_penale')[:-1]:
            for link2 in self.get_links(link):
                file.write(' '.join(self.get_texts(link2)))
        
        file.close()