import re
import urllib.parse
from tldextract import extract
from bs4 import BeautifulSoup

class HtmlParser(object):
    def __init__(self):
        self.word_list = set()
        self.host = ""

    def get_new_url_list(self, page_url, soup):
        new_url_list = set()
        # find links that are within the domain using regex
        links = soup.find_all('a')
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            if self.host in new_full_url and "pdf" not in new_full_url:
                new_url_list.add(new_full_url)
        return new_url_list

    def leet_speak(self, word):
        dict = {
            'a': '4',
            'A': '4',
            'e': '3',
            'E': '3',
            'l': '1',
            'L': '1',
            't': '7',
            'T': '7',
            'o': '0',
            'O': '0'
        }
        word = ''.join(dict.get(s, s) for s in word)
        return word

    def process_word(self, word):
        if word not in self.word_list:
            self.word_list.add(word)
            self.word_list.add(word.upper())
            self.word_list.add(word.lower())
            self.word_list.add(word[::-1])
            self.word_list.add(self.leet_speak(word))

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    def get_new_data(self, page_url, soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(self.visible, texts)
        for text in list(visible_texts):
            text = text.strip()
            if len(text) != 0:
                word_list = text.replace('\n',' ').split(' ')
                for word in word_list:
                    word = word.strip()
                    if len(word) != 0:
                        if "www" not in word and '<' not in word and '>' not in word:
                            self.process_word(word)
        return self.word_list


    def parse(self, page_url, page_content):

        if page_url is None or page_content is None:
            return
        soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8')
        tsd, td, tsu = extract(page_url)
        self.host = td
        new_url_list = self.get_new_url_list(page_url, soup)
        new_data = self.get_new_data(page_url, soup)
        return new_url_list, new_data

    def checkLoginForm(self, page_content):
        try:
            soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8')
            links = soup.find_all('form')
            password_count = 0
            text_count = 0
            for sub_form in links:
                form_list = sub_form.prettify().split("\n")
                for i in form_list:
                    if 'type=\"password\"' in i:
                        password_count += 1
                    if 'type=\"text\"' in i:
                        text_count += 1
                if password_count==1 and text_count == 1:
                    return True
            return False

        except:
            print("Error")

    def getLoginFormDataName(self, page_content):
        try:
            list = ["","",""]
            soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8')
            links = soup.find_all('form')
            for sub_form in links:


                form_list = sub_form.prettify().split("\n")
                for i in form_list:
                    if 'type=\"password\"' in i:
                        index = i.find('name=\"') + len('name=\"')
                        end_index = i.find('\"',index)
                        list[1] = i[index:end_index]
                        list[2] = sub_form['action']
                    if 'type=\"text\"' in i:
                        index = i.find('name=\"') + len('name=\"')
                        end_index = i.find('\"', index)
                        list[0] = i[index:end_index]
            return list

        except:
            print("Error")
