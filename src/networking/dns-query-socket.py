import socket
import struct

domain = "google.com"

def build_dns_query(domain):
    """Construct a simple DNS query for an A record"""
    transaction_id = b"\xaa\xaa"  # Fixed transaction ID
    flags = b"\x01\x00"  # Standard query
    questions = b"\x00\x01"  # One question
    answer_rrs = b"\x00\x00"  # No answers
    authority_rrs = b"\x00\x00"
    additional_rrs = b"\x00\x00"

    # Convert domain to DNS format (e.g., "example.com" -> b"\x07example\x03com\x00")
    query_parts = domain.split(".")
    query = b"".join(len(part).to_bytes(1, "big") + part.encode() for part in query_parts) + b"\x00"

    qtype = b"\x00\x01"  # Type A
    qclass = b"\x00\x01"  # Class IN

    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + qtype + qclass


def parse_dns_response(response):
    """Parse a DNS response and extract the IP address"""
    header_size = 12
    answer_start = response.find(b"\xc0")  # Compressed domain pointer
    if answer_start == -1:
        return None

    answer_section = response[answer_start + 2:]  # Skip pointer
    ip_start = answer_section.find(b"\x00\x01\x00\x01")  # Look for Type A record
    if ip_start == -1:
        return None

    ip_data = answer_section[ip_start + 10:ip_start + 14]  # Extract IP bytes
    return ".".join(map(str, ip_data))


def resolve_dns(domain, dns_server="8.8.8.8"):
    """Send a DNS query to a specified DNS server"""
    query = build_dns_query(domain)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(query, (dns_server, 53))

        try:
            response, _ = sock.recvfrom(512)  # Standard UDP DNS response size
            ip_address = parse_dns_response(response)
            if ip_address:
                print(f"Resolved {domain} to {ip_address} using {dns_server}")
                return ip_address
            else:
                print(f"Failed to resolve {domain}")
                return "Nothing"
        except socket.timeout:
            print("DNS request timed out")
            return "Timeout"


# Example Usage:
resolve_dns(domain, dns_server="8.8.8.8")  # Google's public DNS
resolve_dns(domain, dns_server="1.1.1.1")  # Cloudflare's DNS
