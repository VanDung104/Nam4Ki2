import time
import random

class ServerTimeout(Exception):
    pass

class AuthoritativeServer:
    def __init__(self, records, fail=False):
        self.records = records
        self.fail = fail

    def resolve(self, subdomain):
        if self.fail:
            raise ServerTimeout("Authoritative server failed")
        time.sleep(0.1)
        return self.records.get(subdomain, None)

class TLDServer:
    def __init__(self, domains, fail=False):
        self.domains = domains  # domain_name -> AuthoritativeServer
        self.fail = fail

    def get_authoritative(self, domain_name):
        if self.fail:
            raise ServerTimeout("TLD server failed")
        time.sleep(0.1)
        return self.domains.get(domain_name, None)

class RootServer:
    def __init__(self, tlds):
        self.tlds = tlds  # tld_name -> TLDServer

    def get_tld_server(self, tld):
        time.sleep(0.1)
        return self.tlds.get(tld, None)

def resolve_domain(domain, root_server):
    parts = domain.split(".")
    if len(parts) < 2:
        print("Invalid domain")
        return None

    subdomain = ".".join(parts[:-2])
    domain_name = ".".join(parts[-2:])
    tld = parts[-1]

    try:
        start = time.time()
        tld_server = root_server.get_tld_server(tld)
        print(f"→ Root resolved .{tld} in {round(time.time() - start, 3)}s")

        start = time.time()
        authoritative_server = tld_server.get_authoritative(domain_name)
        print(f"→ TLD resolved {domain_name} in {round(time.time() - start, 3)}s")

        start = time.time()
        ip = authoritative_server.resolve(subdomain)
        print(f"→ Authoritative resolved {domain} = {ip} in {round(time.time() - start, 3)}s")
        return ip
    except ServerTimeout as e:
        print(f"Error: {e}")
        return None

# Sample data
auth_example = AuthoritativeServer({
    "www": "192.0.2.1",
    "mail": "192.0.2.2",
    "shop": "192.0.2.3"
})

auth_myorg = AuthoritativeServer({
    "mail": "192.0.3.1",
    "shop": "192.0.3.2"
}, fail=False)  # you can test fail=True

tld_com = TLDServer({
    "example.com": auth_example
})
tld_org = TLDServer({
    "myorg.org": auth_myorg
}, fail=False)  # you can test fail=True

root = RootServer({
    "com": tld_com,
    "org": tld_org
})

# Run test cases
print("\n--- Resolving www.example.com ---")
resolve_domain("www.example.com", root)

print("\n--- Resolving mail.myorg.org ---")
resolve_domain("mail.myorg.org", root)

print("\n--- Resolving shop.myorg.org (simulate TLD fail) ---")
tld_org.fail = True
resolve_domain("shop.myorg.org", root)
