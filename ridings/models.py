"""
ResistbotCA

Copyright (c) 2017 franciskung.com consulting ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""


from django.db import models

class Riding(models.Model):

  riding_id = models.IntegerField(blank=True, null=True)
  riding_name = models.CharField(max_length=255, blank=True, null=True)
  city = models.CharField(max_length=255, blank=True, null=True)
  province = models.CharField(max_length=2, blank=True, null=True)
  
  representative_name = models.CharField(max_length=255, blank=True, null=True)
  representative_email = models.CharField(max_length=255, blank=True, null=True)
  representative_phone = models.CharField(max_length=255, blank=True, null=True)
  representative_fax = models.CharField(max_length=255, blank=True, null=True)
  representative_party = models.CharField(max_length=255, blank=True, null=True)
  
  raw_response = models.TextField(blank=True, null=True)


class FederalRiding(Riding):
  pass


class PreselectRidingManager(models.Manager):
  def get_queryset(self):
    return super(PreselectRidingManager, self).get_queryset().select_related('federal_riding')
    
class PostalCode(models.Model):
  postal_code = models.CharField(max_length=6, db_index=True)
  lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, db_index=True)
  lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, db_index=True)

  city = models.CharField(max_length=255, blank=True, null=True)
  federal_riding = models.ForeignKey(FederalRiding)

  #provincial_riding = models.ForeignKey(ProvincialRiding)
  #municipal_ward = models.ForeignKey(MunicipalWard)
  
  objects = PreselectRidingManager

