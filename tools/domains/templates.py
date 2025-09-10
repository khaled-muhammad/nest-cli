from colorama import Fore, Style


domain_connection_guide = """
To connect your domain to Nest, please follow these steps:
* Add a CNAME record to your domain pointing to <username>.hackclub.app
OR
* If you're using a root domain and you can't add a CNAME record, you can add an A record pointing to the following IP addresses:
A record: 37.27.51.34
AAAA record: 2a01:4f9:3081:399c::4
TXT record: domain-verification=<YOUR_NEST_USERNAME>

If you have already done this, please wait a few minutes sometimes upto 24 hours for DNS records to propagate.
"""

domain_connection_guide_styled = f"""
{Fore.CYAN + Style.BRIGHT}┌───────────────────────────────────────────────┐
│   To connect your domain to Nest, follow:     │
└───────────────────────────────────────────────┘{Style.RESET_ALL}

{Fore.YELLOW + Style.BRIGHT}▶ Add a CNAME record:{Style.RESET_ALL}
    {Fore.GREEN}<username>.hackclub.app{Style.RESET_ALL}

{Fore.YELLOW + Style.BRIGHT}▶ Or, if you're using a root domain:{Style.RESET_ALL}
    {Fore.BLUE}A record:{Style.RESET_ALL}      37.27.51.34
    {Fore.BLUE}AAAA record:{Style.RESET_ALL}   2a01:4f9:3081:399c::4

{Fore.YELLOW + Style.BRIGHT}▶ Add a TXT record for verification:{Style.RESET_ALL}
    {Fore.MAGENTA}domain-verification=<username>{Style.RESET_ALL}

If you have already done this, please wait a few minutes sometimes upto 24 hours for DNS records to propagate.
"""