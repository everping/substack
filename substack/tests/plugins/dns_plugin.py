from substack.helper.dns import get_authoritative
authoritative_name_servers = get_authoritative("bkav.com")
print authoritative_name_servers
