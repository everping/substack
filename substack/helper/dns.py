import dnslib
import socket
import struct
from substack.data.logger import logger
from substack.data.exceptions import DnsQueryException


def query(host_name, query_type='ANY', name_server='8.8.8.8', tcp=True):
    """
    This method override the query method of dnslib
    :return: a list of info that we got
    """
    # logger.info("Querying %s with type %s and name server %s" % (host_name, query_type, name_server))
    results = []
    try:
        _query = dnslib.DNSRecord.question(host_name, query_type.upper().strip())
        response_raw = _query.send(name_server, tcp=tcp, timeout=2)
        response_parsed = dnslib.DNSRecord.parse(response_raw)

        for r in response_parsed.rr:
            try:
                _type = str(dnslib.QTYPE[r.rtype])
            # Server sent an unknown type:
            except dnslib.dns.DNSError:
                _type = str(r.rtype)
            _host = str(r.rname).rstrip(".")
            _data = str(r.rdata)
            result = {'host': _host,
                      'type': _type,
                      'data': _data}
            results.append(result)

    except socket.error:
        logger.error("The query meet timeout, so i broke it")
    except struct.error:
        logger.error("Could not decode the response of dns query")
    except:
        raise DnsQueryException
    return results


def get_authoritative(host_name):
    """
    Get the authoritative name server of host_name
    :return: a list of name server
    """
    result = []
    name_servers = query(host_name, query_type="NS")
    for ns in name_servers:
        if ns['type'] == "NS":
            a_lookups = query(ns['data'].rstrip("."), 'A')
            for lookup in a_lookups:
                result.append(lookup['data'])
    return result


def translate(domain_name, name_server):
    """
    Translates the domain into the IP address
    """
    try:
        lookup = query(domain_name, name_server=name_server, query_type="A")
        return lookup[0]['data']
    except IndexError:
        return None
    except:
        raise
