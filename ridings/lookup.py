import requests
from ridings.models import PostalCode, FederalRiding

def postal_code_lookup(postal_code, riding='federal'):

  # attempt to see if we already have this postal code cached
  pcode_cache = PostalCode.objects.filter(postal_code=postal_code).first()

  if not pcode_cache:

    # do an OpenNorth call to get the riding info
    url = "https://represent.opennorth.ca/postcodes/{0}/?sets=federal-electoral-districts".format(postal_code)
    response = requests.get(url)
    
    if response.status_code != 200:
      return None
      
    raw_riding = response.json()
    
    # set up a new cache object to avoid future OpenNorth calls on this postal code
    pcode_cache = PostalCode()
    pcode_cache.postal_code = postal_code
    pcode_cache.city = raw_riding['city']
    pcode_cache.lat = raw_riding['centroid']['coordinates'][1]
    pcode_cache.lng = raw_riding['centroid']['coordinates'][0]
    
    # get (or create) riding details
    riding = FederalRiding.objects.filter(riding_id=raw_riding['boundaries_centroid'][0]['external_id']).first()
    if not riding:
      riding = FederalRiding(riding_id=raw_riding['boundaries_centroid'][0]['external_id'],
                             riding_name=raw_riding['boundaries_centroid'][0]['name'],
                             city=raw_riding['city'],
                             province=raw_riding['province'],
                             representative_name=raw_riding['representatives_centroid'][0]['name'],
                             representative_email=raw_riding['representatives_centroid'][0]['email'],
                             representative_party=raw_riding['representatives_centroid'][0]['party_name'],
                             raw_response=response.text)

      # some lil' fun to get the rep's phone/fax number:
      # prefer their constituency office, but if that isn't present, take any numbers we can find
      backup_phone = None
      backup_fax = None

      for office in raw_riding['representatives_centroid'][0]['offices']:
        if office['type'] == 'constituency':
          riding.representative_phone = office['tel']
          riding.representative_fax = office['fax']
        else:
          if office['tel']:
            backup_phone = office['tel']
          if office['fax']:
            backup_fax = office['fax']
      if backup_phone and not riding.representative_phone:
        riding.representative_phone = backup_phone
      if backup_fax and not riding.representative_fax:
        riding.representative_fax = backup_fax
        
      # save it all
      riding.save()
      
    # final saving
    pcode_cache.federal_riding = riding
    pcode_cache.save()

  # return None on error, or the federal riding (only federal is supported atm)  
  if not pcode_cache:
    return None
    
  if riding == 'federal':
    return pcode_cache.federal_riding
    
  return None


