from colorama import Fore

def req_prettify(status, url: str):
		# handles
        if status in [200,201,204]:
            print(f"{Fore.BLUE}[{Fore.RED}200{Fore.BLUE}]{Fore.WHITE} Ok {Fore.RED}:{Fore.WHITE} {Fore.BLUE}{url}{Fore.WHITE}")
            return True
        elif status == 429:
            print(f"{Fore.BLUE}[{Fore.RED}429{Fore.BLUE}]{Fore.WHITE} RateLimited {Fore.RED}:{Fore.WHITE} {Fore.BLUE}{url}{Fore.WHITE}")
            return False
        elif status in [401,400,402]:
            print(f"{Fore.BLUE}[{Fore.RED}400{Fore.BLUE}]{Fore.WHITE} Bad Request {Fore.RED}:{Fore.WHITE} {Fore.BLUE}{url}{Fore.WHITE}")
			#return
        elif status == 403:
            print(f"{Fore.BLUE}[{Fore.RED}400{Fore.BLUE}]{Fore.WHITE} No Permission To Resource {Fore.RED}:{Fore.WHITE} {Fore.BLUE}{url}{Fore.WHITE}")
			#return
        else:
            print(f"{Fore.BLUE}[{Fore.RED}{status}{Fore.BLUE}]{Fore.WHITE} Undefined Returned Status {Fore.RED}:{Fore.WHITE} {Fore.BLUE}{url}{Fore.WHITE}")