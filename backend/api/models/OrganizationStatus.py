"""
    REST API Documentation for the NRS TFRS Credit Trading Application

    The Transportation Fuels Reporting System is being designed to streamline compliance reporting for transportation fuel suppliers in accordance with the Renewable & Low Carbon Fuel Requirements Regulation.

    OpenAPI spec version: v1
        

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from django.db import models

from auditable.models import Auditable
from api.managers.OrganizationStatusManager import OrganizationStatusManager

class OrganizationStatus(Auditable):
    status = models.CharField(max_length=25,
                              unique=True,
                              db_comment='Enumerated value to describe the organization status.')
    description = models.CharField(max_length=1000,
                                   blank=True,
                                   null=True,
                                   db_comment='Description of the organization status. This is the displayed name.')
    display_order = models.IntegerField(db_comment='Relative rank in display sorting order')
    effective_date = models.DateField(blank=True, null=True, db_comment='The calendar date that the organization status type value became valid.')
    expiration_date = models.DateField(blank=True, null=True, db_comment='The calendar date that the organization status type value is no longer valid.')
    objects = OrganizationStatusManager()

    def natural_key(self):
        return (self.status,)

    class Meta:
        db_table = 'organization_status'

    db_table_comment = 'Possible statuses an organization may be in' \
                       ' (ex. Active, Inactive, Archived)'
