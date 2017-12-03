import urllib.parse
from bs4 import BeautifulSoup
import re
import self_get_post
from tldextract import extract
common_subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2",
                         "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog",
                         "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3", "mail2", "new", "mysql",
                         "old", "lists", "support", "mobile", "mx", "static", "docs", "beta", "shop", "sql",
                         "secure", "demo", "cp", "calendar", "wiki", "web", "media", "email", "images", "img",
                         "www1", "intranet", "portal", "video", "sip", "dns2", "api", "cdn", "stats", "dns1", "ns4",
                         "www3", "dns", "search", "staging", "server", "mx1", "chat", "wap", "my", "svn", "mail1",
                         "sites", "proxy", "ads", "host", "crm", "cms", "backup", "mx2", "lyncdiscover", "info", "apps",
                         "download", "remote", "db", "forums", "store", "relay", "files", "newsletter", "app", "live",
                         "owa", "en", "start", "sms", "office", "exchange", "ipv4"]

def remove_subdomain(domain):
    for i in common_subdomains:
        if domain.startswith(i):
            return domain[len(i)+1:]
    return domain

def get_subdomain(url):
    list = []

    tsd, td, tsu = extract(url)  # subdomain, hostname, com
    new_url = urllib.parse.urlparse(url)

    for subdomain in common_subdomains:
        URL = new_url.scheme + "://"+ subdomain + '.' + td + '.' + tsu #+ new_url.path
        list.append(URL)
    result = []
    for u in list:
        try:
            response = self_get_post.get_method(u,None)
            #print(u + " works")
            result+=[u]
        except:
            pass
    #print(result)
    return result

def checkRobots(url):

    response = self_get_post.get_responses(url+"/robots.txt",None)
    if self_get_post.get_return_code(response).decode() == '200':
        return True
    return False

def getRobotsLists(url):
    response = self_get_post.get_method(url + "/robots.txt",None)
    page = response.decode()
    list = page.split('\n')
    pattern = re.compile("Allow:")
    result = []
    for item in list:
        if pattern.match(item):
            result+=[url+item.split(' ')[1]]
    print(result)
    return result



