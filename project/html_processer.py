from self_get_post import post_method, get_method
import self_get_post
import html_parser
from tldextract import extract

class HtmlProcesser():

    def download(self, url):
        if url is None:
            return None
        try:
            response = get_method(url,None)
        except:
            print("URL Error")
            return None
        return response

    def upload(self, user_agent,url, var_name, dataSet):
        password = var_name[1]
        account = var_name[0]
        count = 1
        for one_password in dataSet:

            input_data = {}
            input_data[account] = user_agent
            input_data[password] = one_password
            try:
                httpP = ""
                if url.startswith("https://"):
                    httpP = "https://"
                else:
                    httpP = "http://"
                response = post_method(httpP+ self_get_post.get_domain(url)+'/'+var_name[2],input_data,url)
                if self.check_valid_password(response,var_name):
                    print(str(count)+"Account: " + user_agent + "   Password: " +one_password+" --> " + "True")
                    return True
            except:
                print("URL Error")
            print(str(count)+". Account: "+user_agent+"   Password: "+one_password+" --> "+ "False")
            count += 1
        return False

    def check_valid_password(self,response,var_name):
        parser = html_parser.HtmlParser()
        if parser.checkLoginForm(response):
            var_name_check = tuple(parser.getLoginFormDataName(response))

            if var_name == var_name_check:
                return False
            else:
                return True

        else:
            return True

