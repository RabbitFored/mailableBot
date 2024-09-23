import dns.resolver

def get_mx_server(domain):
   try:
        mail_servers = dns.resolver.resolve(domain, 'MX')
        mail_servers = list(set([data.exchange.to_text()[:-1] if data.exchange.to_text().endswith('.') else data.exchange.to_text() for data in mail_servers]))
        return mail_servers
   except:
        return([], [])