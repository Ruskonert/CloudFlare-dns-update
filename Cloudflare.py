import sys, requests, time

from json import load, dumps

# Input your cloudflare zone id. It can be change the value.
# It need to input the zone id you want to.
ZONE_ID = 'a0bb2d04c8e6e66a2aecc9bbd1741f51'

# Input the cloudflare api key. (It will be Private key)
# It needs to input your key.
API_KEY = '0000000000000000000000000000000000000000'

# Getting your information from email address.
EMAIL = 'ruskonert@gmail.com'

CONTENT_TYPE = 'application/json'

CLOUDFLARE_API_ZONE_URL = 'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_identifier}'

def get_response_header():
    headers = {'Content-Type': CONTENT_TYPE, 'Accept-Charset': 'UTF-8', 'X-Auth-Email': EMAIL, 'X-Auth-Key': API_KEY}
    return headers

def get_public_ip():
    try:
        req_string = requests.get('https://jsonip.com/')
        json_string = req_string.json()
        public_address_ip = json_string['ip']
        if public_address_ip is not None or len(public_address_ip) > 0:
            return public_address_ip
        else:
            return None
    except Exception as ex:
        raise ValueError("CANNOT_GET_JSON_IP_VALUES") from ex

def search_dns_records(record_id = None):
    header = get_response_header()
    response = requests.get(CLOUDFLARE_API_ZONE_URL.format(zone_id = ZONE_ID, record_identifier = ''), headers = header)
    result = response.json()
    content_value = None
    if result['success']:
        for index, value in enumerate(result['result']):
            if value['id'] == record_id:
                content_value = value['content'] 
            print('{0}. ({1}-{2}): {3}'.format(index, value['id'], value['type'], value['name']))
    if content_value is not None:
        return content_value


def update_dns_record(record_id, dns_record_type, name, content, optional = None):
    """
    DNS records for a zone update dns record, It refers to here:
        PUT zones/:zone_identifier/dns_records/:identifier
    """
    header = get_response_header()
    
    data = {'type': dns_record_type, 'name': name, 'content': content }
    json_data = dumps(data)
    response = requests.put(CLOUDFLARE_API_ZONE_URL.format(zone_id = ZONE_ID, record_identifier = record_id), headers = header, data=json_data)
    result = response.json()['success']
    if result is None:
        raise requests.RequestException("Request failed")
    else:
        return result

def main():
    print("Public IP register with Cloudflare")
    print("Copyright 2019, ruskonert all rights reserved.")
    record_id = '5f0ba8bc43ac35062a354e5ea02f6da8'
    time.sleep(1)
    
    # Gets the user's public IP.
    public_ip = get_public_ip()
    
    if public_ip is None:
        raise requests.RequestException("Not connected to the Internet. Please try again later.")
    else:
        print("Your public ip: {0}".format(public_ip))
        print("Searching the registered DNS Records ...")

        # Gets the previously registered public IP value.
        before_public_ip = search_dns_records(record_id)

        # Connect the DNS record.
        result = update_dns_record(record_id, 'A', 'home', get_public_ip())
        if result:
            print('Connected the dynamic IP to the domain through the DNS server [{0}] -> [{1}]'.format(before_public_ip, public_ip))
            time.sleep(2)
            sys.exit(0)
        else:
            print("Failed to change ip address, Please check the url rule:")
            print("Refer: https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record")
            sys.exit(-1)

if __name__ == "__main__":
    main()
