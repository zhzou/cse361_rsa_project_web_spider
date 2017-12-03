class UrlList():
    def __init__(self,):
        self.unprocessed_urls = set()
        self.processed_urls = set()
        self.login_urls = set()
        #login_vars : login form, var names for the input tag
        self.login_vars = set()

    def add_one_url(self,root):
        if root not in self.unprocessed_urls and root not in self.processed_urls and root is not None:
            self.unprocessed_urls.add(root)

    def add_one_login_url(self,url,l):
        if url not in self.login_urls and url is not None:

            self.login_urls.add(url)

            self.login_vars.add(tuple(l))


    def has_login_url(self):
        return len(self.login_urls) > 0

    def get_one_login_url(self):
        return self.login_urls.pop()

    def get_one_login_vars(self):
        return self.login_vars.pop()

    def add_new_url_list(self, new_url_list):
        if new_url_list is None or len(new_url_list) == 0:
            return
        for url in new_url_list:
            if url not in self.unprocessed_urls and url not in self.processed_urls and url is not None:
                self.unprocessed_urls.add(url)

    def unprocessed_size(self):
        return len(self.unprocessed_urls)

    def has_new_url(self):
        return self.unprocessed_size() > 0

    def get_one_url(self):
        url = self.unprocessed_urls.pop()
        self.processed_urls.add(url)
        return url
