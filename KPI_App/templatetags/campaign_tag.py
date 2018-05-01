from KPI_App.salesforce import SalesforceIntegrations

__author__ = 'eMaM'

from django import template

register = template.Library()


@register.simple_tag
def get_campaign_name(all_campaign, target_campaign):
    if target_campaign in all_campaign:
        return all_campaign[target_campaign]
    return target_campaign


@register.simple_tag
def get_lead_name(allLead, targetLead):
    if targetLead in allLead:
        return allLead['Id'][targetLead]
    return targetLead


@register.simple_tag
def get_lead_response_date(campaignId, leadId, sendDate):
    sales_force = SalesforceIntegrations()
    data = sales_force.get_response_date_for_sms(campaignId=campaignId, leadId=leadId, date=sendDate)
    if len(data) > 0:
        return data[0]['CreatedDate']
    return 'No response'

@register.simple_tag
def get_lead_email_sent(email, sendDate):
    sales_force = SalesforceIntegrations()
    data = sales_force.get_email_sent_after_response(email=email, createdDate=sendDate)
    if len(data) > 0:
        return data[0]['CreatedDate']
    return 'No Email sent'

@register.simple_tag
def get_lead_call_sent(phone, sendDate):
    sales_force = SalesforceIntegrations()
    data = sales_force.get_call_sent_after_response(phone=phone, createdDate=sendDate)
    if len(data) > 0:
        return data[0]['CreatedDate']
    return 'No Call sent'





@register.simple_tag
def get_lead_email_sent_count(email, sendDate):
    sales_force = SalesforceIntegrations()
    data = sales_force.get_email_sent_after_response_count(email=email, createdDate=sendDate)
    data = data[0]['expr0']
    return data

@register.simple_tag
def get_lead_call_sent_count(phone, sendDate):
    sales_force = SalesforceIntegrations()
    data = sales_force.get_call_sent_after_response_count(phone=phone, createdDate=sendDate)
    data = data[0]['expr0']
    return data