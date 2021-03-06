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


class CreditTradeZeroReason(Auditable):
    reason = models.CharField(max_length=25,
                              db_comment='Enumerated value to describe the credit trade zero reason.')
    description = models.CharField(max_length=1000, db_comment='Description of the credit trade zero reason. This is the displayed name.')
    display_order = models.IntegerField(db_comment='Relative rank in display sorting order')
    effective_date = models.DateField(blank=True, null=True, db_comment='The calendar date the credit trade zero reason type value became valid.')
    expiration_date = models.DateField(blank=True, null=True, db_comment='The calendar date the credit trade zero reason type value is no longer valid.')

    class Meta:
        db_table = 'credit_trade_zero_reason'

    db_table_comment = 'Contains a list of reasons for Credit Transfer Proposals that have a fair market value of zero dollars per credit. For example: the fuel suppliers are affiliated or an "Other" reason. If "Other" is selected, a comment is required explaining why the credits being transferred have a fair market value of zero dollars.'
