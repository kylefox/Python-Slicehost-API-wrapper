#! /usr/bin/python
import sys
from slicehost import *

def _get_zone(host):
    origin = raw_input("Enter the zone (domain) name: ").lower()
    if not origin.endswith('.'):
        origin += '.'
    zone = host.Zone.find_first(origin=origin)
    if zone is None:
        # Create the zone
        zone = host.Zone({"origin":origin, "ttl": 3000})
        zone.save()
        print "** Created zone \"%s\"" % origin
    else:
        print "** Found zone \"%s\"" % origin
    return zone

def _get_do_a_record(slices):
    for index in range(0, len(slices)):
        print '[%s] %s : %s' % (index+1, slices[index].name, slices[index].ip_address)
    index = raw_input("Slice to point A record to (enter to skip): ")
    try:
        return slices[int(index)-1]
    except:
        return None

def main(host):
    slices = host.Slice.find()
    zone = _get_zone(host)
    do_a_record = _get_do_a_record(slices)
    do_ns = bool(raw_input("Setup default NS records? (y/n): ").lower() == 'y')
    do_apps = bool(raw_input("Setup Google Apps MX records? (y/n): ").lower() == 'y')
    if do_a_record is not None:
        records = zone.create_A_record(do_a_record)
        print records
        # print '** Created A record to %s (%s) for %s' % (do_a_record.name, do_a_record.ip_address, ", ".join(records))
    if do_ns:
        zone.setup_slicehost_ns()
        print '** Created default Slicehost nameservers (ns1.slicehost.net - ns3.slicehost.net).'
    if do_apps:
        zone.setup_google_apps()
        print '** Created Google Apps MX records.  You must manually create the domain verification CNAME record.'
    print 'Finished!'
    
if __name__ == '__main__':
    "Usage: slicehost_test TOKEN_OR_FILENAME"
    if len(sys.argv) != 2:
        print "Usage: python %s <token_or_filename>" % sys.argv[0]
        sys.exit(1)
    token = sys.argv[1]
    try:
        token = open(token).read()
    except IOError:
        pass
    host = Slicehost(token)
    main(host)