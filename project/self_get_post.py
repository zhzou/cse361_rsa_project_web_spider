import ssl
import socket

def get_method(url,cookie_set):
    responses = get_responses(url,cookie_set)
    while get_return_code(responses).decode() == "301" or get_return_code(responses).decode() == "302":
        responses = get_responses(get_redirect(responses,cookie_set))
    return responses[-1]

def get_redirect(responses_list):
    for i in responses_list:
        l = i.decode().split(' ')
        if l[0] == 'Location:':
            return l[1]

def get_responses(url,cookie_list):
    if url.startswith("http://"):
        port = 80
    elif url.startswith("https://"):
        port = 443
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((get_domain(url), port))
    if port == 443:
        s = ssl.wrap_socket(s, None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                            ssl_version=ssl.PROTOCOL_SSLv23)
    cookies = ""
    if cookie_list == None:
        cookies = ""
    else:
        cookies = generateCookieHeader(cookie_list)
    s.sendall(('GET '+get_path(url)+' HTTP/1.1\r\nHost: '+get_domain(url)+'\r\nProxy-Connection: keep-alive\r\nConnection: close\r\n'
                                                                          'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/38.0.2125.104 Safari/537.36\r\n'
                                                                          'Accept-Language: en-US,en;q=0.8\r\nAccept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n\r\n').encode())
    total = ''.encode()
    while True:
        n = s.recv(4096)
        if not n:
            s.close()
            break
        total += n
    responses = process_response(total)
    return responses

def get_return_code(list):
    str = list[0]
    str_list = str.split(" ".encode())
    return str_list[1]

def process_response(response_total):
    total_list = response_total.split("\r\n".encode())
    return total_list

def get_domain(url):
    end_index = -1
    domain = ""
    if url.startswith("http:"):

        for i in range(7,len(url)):
            if url[i] == '/':
                end_index = i
                break
        if end_index<0:
            domain = url[7:]
        else:
            domain = url[7:end_index]
    elif url.startswith("https://"):
        for i in range(8,len(url)):
            if url[i] == '/':
                end_index = i
                break
        if end_index<0:
            domain = url[8:]
        else:
            domain = url[8:end_index]
    else:
        for i in range(8,len(url)):
            if url[i] == '/':
                end_index = i
                break
        if end_index<0:
            domain = url[8:]
        else:
            domain = url[8:end_index]
    return domain

def get_path(url):
    path = ""
    if url.startswith("http://"):
        path = url[7+len(get_domain(url)):]
    elif url.startswith("https://"):
        path = url[8 + len(get_domain(url)):]
    else:
        path = url[len(get_domain(url)):]
    if path == "":
        path = "/"
    return path

def post_method(url,data_dict,referer):
    responses = post_responses(url,data_dict,referer)
    while get_return_code(responses).decode() == "301" or get_return_code(responses).decode() == "302":
        responses = get_responses(get_redirect(responses),generateCookieSet(responses))
    return responses[-1]

def generateCookieSet(responses):
    result = None
    for i in responses:
        if i.decode().startswith("Set-Cookie: "):
            if result is None:
                result = [i.decode()[12:]]
            else:
                result += [i.decode()[12:]]
    return result

def post_responses(url,data_dict,referer):
    if url.startswith("http://"):
        port = 80
    elif url.startswith("https://"):
        port = 443
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((get_domain(url), port))
    if port == 443:
        s = ssl.wrap_socket(s, None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                            ssl_version=ssl.PROTOCOL_SSLv23)

    s.sendall(('POST '+get_path(url)+' HTTP/1.1\r\nHost: '+get_domain(url)+'\r\nConnection: close\r\nCache-Control: max-age=0\r\n'
                                                                          'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/38.0.2125.104 Safari/537.36\r\n'
                                                                          'Accept-Language: en-US,en;q=0.8\r\nAccept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
                                                                          'Referer: '+referer+'\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: '+str(len(construct_data_field(data_dict)))+'\r\n'
                                                                          '\r\n'
                                                                          ''+construct_data_field(data_dict)+'\r\n').encode())

    total = ''.encode()
    while True:
        n = s.recv(4096)
        if not n:
            s.close()
            break
        total += n
    responses = process_response(total)
    return responses

def construct_data_field(data_dict):
    result = ""
    for i in data_dict:
        result += i+'='+data_dict[i]+'&'
    return result[:-1]

def generateCookieHeader(cookie_list):
    result = "Cookie: "
    for i in cookie_list:
        result += i + '; '
    return result

#print(len(construct_data_field({'log':'z','pwd':'PU28aPuDGaEY','wp-submit':'Log+In','wp-submit':'Log+In'})))
#get_method("http://google.com/")
# post_method("http://www.1point3acres.com/wp-login.php",
#             {'log':'z','pwd':'PU28aPuDGaEY'},
#             "http://www.1point3acres.com/wp-login.php")
#print(post_method("http://cse361-2017-rsa.club/action_page.php",{'uname':'admin','psw':'Just1fy','submit':''},"http://cse361-2017-rsa.club/login.html"))