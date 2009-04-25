from pyactiveresource.activeresource import ActiveResource

BASE_URL = 'https://%s@api.slicehost.com/'

# MX Records for Google Apps.
GOOGLE_MX_RECORDS = (
   ('ASPMX.L.GOOGLE.COM.',      10),
   ('ALT1.ASPMX.L.GOOGLE.COM.', 20),
   ('ALT2.ASPMX.L.GOOGLE.COM.', 20),
   ('ASPMX2.GOOGLEMAIL.COM.',   30),
   ('ASPMX3.GOOGLEMAIL.COM.',   30),
   ('ASPMX4.GOOGLEMAIL.COM.',   30),
   ('ASPMX5.GOOGLEMAIL.COM.',   30),
)

SLICEHOST_NS = 'ns%s.slicehost.net'

class Slice(ActiveResource): 
    pass

class Zone(ActiveResource):
    
    def setup(self, ip_or_slice):
        """
        Helper that creates default NS/A records pointing to Slichost,
        and MX records pointing to Google Apps.
        """
        self.setup_slicehost_ns()
        self.create_A_record(ip_or_slice)
        self.setup_google_apps()
    
    def create_A_record(self, ip_or_slice):
        """
        Creates two A records pointing a Zone to Slicehost (domain and wildcard subdomain).
        Returns a two-tuple, with each tuple containing `(record, created)`
            `record` is the Record object
            `created` is a boolean indicating if the Record was created (True) or retrieved (False).
        """
        results = []
        if isinstance(ip_or_slice, Slice):
            ip_address = ip_or_slice.ip_address
        else:
            ip_address = str(ip_or_slice)
        r1_data = {"data": ip_address, "record_type": 'A', "zone_id": self.id, "name": self.origin}
        r2_data = {"data": ip_address, "record_type": 'A', "zone_id": self.id, "name": "*.%s" % self.origin}
        r1 = Record.find_first(**r1_data)
        created = False
        if r1 is None:
            r1 = Record(r1_data)
            r1.save()
            created = True
        results.append((r1, created))
        r2 = Record.find_first(**r2_data)
        created = False
        if r2 is None:
            r2 = Record(r2_data)
            r2.save()
            created = True
        results.append((r1, created))
        return results
    
    def setup_slicehost_ns(self, ttl=86400):
        """
        Creates and returns NS three records:
            ns1.slicehost.com - ns3.slicehost.com
        """
        records = []
        for i in range(1,4):
            r = Record({
                "data": SLICEHOST_NS % i,
                "record_type": 'NS',
                "zone_id": self.id,
                "name": self.origin,
                "ttl": ttl
            })
            r.save()
            records.append(r)
        return records

    def setup_google_apps(self):
        """
        Creates and returns MX records necessary
        for Google Apps email hosting.
        """
        records = []
        for record in GOOGLE_MX_RECORDS:
            r = Record({
                "data": record[0],
                "record_type": 'MX',
                "aux": record[1],
                "zone_id": self.id,
                "name": self.origin
            })
            r.save()
            records.append(r)
        return records
            
class Record(ActiveResource):
    pass
    
RESOURCES = {}
for r in [Slice, Zone, Record]:
    RESOURCES.update({r.__name__: r})
    
class Slicehost(object):
    
    def __init__(self, api_key):
        self.api_key = api_key
        for klass in RESOURCES.values():
            setattr(klass, 'site', BASE_URL % self.api_key)
    
    def __getattr__(self, key):
        if key in RESOURCES:
            return RESOURCES[key]
