from django.conf import settings
from simple_salesforce.exceptions import SalesforceMalformedRequest

__author__ = 'eMaM'
from simple_salesforce import Salesforce


class SalesforceIntegrations():
    TODAY = 'TODAY'
    YESTERDAY = 'YESTERDAY'
    THIS_MONTH = 'THIS_MONTH'
    LAST_MONTH = 'LAST_MONTH'
    THIS_YEAR = 'THIS_YEAR'
    LAST_YEAR = 'LAST_YEAR'
    LAST_WEEK = 'LAST_WEEK'

    def __init__(self):
        self.sf_client = Salesforce(username=settings.SALESFORCE_USERNAME, password=settings.SALESFORCE_PASS,
                                    security_token=settings.SALESFORCE_TOKEN)

    def get_all_leads_by_status_count(self, status, created_date):
        table = 'Lead'
        try:
            return self.sf_client.query_all(
                "Select count(Id) from {} WHERE Status='{}' AND CreatedDate={}".format(table, status, created_date))
        except SalesforceMalformedRequest as e:
            return {}

    def query_all_email_sent_count(self, create_date):
        try:
            return self.sf_client.query_all(
                " Select count(Id) from EmailMessage WHERE CreatedDate={}".format(create_date))
        except SalesforceMalformedRequest as e:
            return {}

    def query_all_sms_count(self, created_date):
        try:
            query = ' SELECT  count(Id) FROM smagicinteract__smsMagic__c'
            query += ' WHERE CreatedDate={}'
            return self.sf_client.query_all(query.format(created_date))
        except SalesforceMalformedRequest:
            return {}

    def query_all_call_count(self, created_date):
        try:
            query = " SELECT  count(Id) FROM Task WHERE Subject Like 'Call'"
            query += " AND CreatedDate={}"
            return self.sf_client.query_all(query.format(created_date))

        except SalesforceMalformedRequest:
            return {}

    def query_all_sms(self, created_date):
        try:
            query = "SELECT Id, CreatedDate,  smagicinteract__Campaign__c,  smagicinteract__Lead__c,  smagicinteract__PhoneNumber__c,  smagicinteract__Sent_On__c FROM smagicinteract__smsMagic__c WHERE CreatedDate={}".format(
                created_date)
            return self.sf_client.query_all(query)
        except SalesforceMalformedRequest:
            return {}

    def query_all_compaign(self, created_date):
        try:
            query = ' SELECT  Id,  Name FROM Campaign WHERE CreatedDate={}'.format(created_date)
            return (self.sf_client.query_all(query)).get('records')
        except SalesforceMalformedRequest:
            return {}

    def query_all_lead(self):
        try:
            query = 'SELECT  Id,  Name,Email,Phone FROM Lead'
            return (self.sf_client.query_all(query)).get('records')
        except SalesforceMalformedRequest:
            return {}

    def get_all_campaign_as_dict(self, created_date):
        campaigns_dict = {}
        data = self.query_all_compaign(created_date=created_date)
        for campiagn in data:
            campaigns_dict[campiagn['Id']] = campiagn['Name']
        return campaigns_dict

    def get_all_leads_as_dict(self):
        leadsDict = {}
        leadsDict['Id'] = {}
        leadsDict['Email'] = {}
        leadsDict['Phone'] = {}
        data = self.query_all_lead()
        for lead in data:
            leadsDict['Id'][lead['Id']] = lead['Name']
            leadsDict['Email'][lead['Id']] = lead['Email']
            leadsDict['Phone'][lead['Id']] = lead['Phone']
        return leadsDict

    def query_all_emails(self):
        try:
            query = 'SELECT  ToAddress,CreatedDate from EmailMessage '
            return self.sf_client.query_all(query)
        except SalesforceMalformedRequest:
            return {}

    def get_emails_as_dict(self):
        emailDict = {}
        email_data = self.query_all_emails()
        for email in email_data:
            emailDict[email['ToAddress']] = email['CreatedDate']
        return emailDict

    def query_all_calls(self):
        pass

    def query_all_sms_campaing(self, created_date):
        try:
            query = 'SELECT  Name,smagicinteract__Campaign__r.Id,smagicinteract__Campaign__r.Name,smagicinteract__Lead__r.Id,smagicinteract__Lead__r.Name,smagicinteract__Lead__r.Phone,smagicinteract__Lead__r.Email,smagicinteract__Name__c,smagicinteract__Sent_On__c FROM smagicinteract__smsMagic__c WHERE smagicinteract__Campaign__c != null and smagicinteract__Sent_On__c != null'
            query += ' and CreatedDate={}'.format(created_date)
            return (self.sf_client.query_all(query)).get('records')
        except SalesforceMalformedRequest:
            return {}

    def get_sales_kpi_details(self, created_date):
        campaign_dict = self.get_all_campaign_as_dict(created_date=created_date)
        lead_dict = self.get_all_leads_as_dict()
        email_dict = self.get_emails_as_dict()

    def get_response_date_for_sms(self, campaignId, leadId, date):
        try:
            query = 'SELECT CreatedDate,smagicinteract__Campaign__c,smagicinteract__Lead__c FROM smagicinteract__Incoming_SMS__c'
            query += " WHERE smagicinteract__Campaign__c='{}' and smagicinteract__Lead__c='{}' and CreatedDate >={}".format(
                campaignId, leadId, date.split('.')[0] + 'Z')
            return (self.sf_client.query_all(query)).get('records')
        except SalesforceMalformedRequest:
            return {}






    def get_email_sent_after_response(self, email, createdDate):
        try:
            query = " SELECT  CreatedDate FROM EmailMessage WHERE ToAddress='{}' AND  CreatedDate>={}".format(email,createdDate.split('.')[0] + 'Z')
            return (self.sf_client.query_all(query)).get('records')

        except SalesforceMalformedRequest:
            return {}


    def get_email_sent_after_response_count(self, email, createdDate):
        try:
            query = " SELECT  Count(Id) FROM EmailMessage WHERE ToAddress='{}' AND  CreatedDate>={}".format(email,createdDate.split('.')[0] + 'Z')
            return (self.sf_client.query_all(query)).get('records')

        except SalesforceMalformedRequest:
            return {}

    def get_call_sent_after_response(self, phone, createdDate):
        try:
            query = " SELECT  createdDate FROM Task WHERE Subject Like 'Call' AND  CreatedDate>={}".format(phone,
                                                                                                           createdDate.split(
                                                                                                               '.')[
                                                                                                               0] + 'Z')
            return (self.sf_client.query_all(query)).get('records')

        except SalesforceMalformedRequest:
            return {}


    def get_call_sent_after_response_count(self, phone, createdDate):
        try:
            query = " SELECT  count(Id) FROM Task WHERE Subject Like 'Call' AND  CreatedDate>={}".format(phone,
                                                                                                           createdDate.split(
                                                                                                               '.')[
                                                                                                               0] + 'Z')
            return (self.sf_client.query_all(query)).get('records')

        except SalesforceMalformedRequest:
            return {}


    def get_property_count(self,created_date,status):
        try:
            properties = self.sf_client.query_all("select count(Id) from Property__c where Property_Status__c = '{}' and CreatedDate={}".format(status,created_date))
            return properties
        except SalesforceMalformedRequest:
            return {}
