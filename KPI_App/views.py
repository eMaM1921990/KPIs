from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from KPI_App.salesforce import SalesforceIntegrations


def KPISalesDashboard(request):

    sales_force_integration = SalesforceIntegrations()
    target_date = request.GET.get('period',sales_force_integration.TODAY)
    email_sents = sales_force_integration.query_all_email_sent_count(create_date=target_date)
    print('number of emails sent {}'.format(email_sents))

    close_home_no = sales_force_integration.get_property_count(status='Closed',created_date=target_date)
    print('Number of closed home is {}'.format(close_home_no))

    won_home_no = sales_force_integration.get_property_count(status='Won',created_date=target_date)
    print('Number of home won is {}'.format(won_home_no))

    no_of_calls = sales_force_integration.query_all_call_count(created_date=target_date)
    print('Number of calls are {}'.format(no_of_calls))

    no_of_sms = sales_force_integration.query_all_sms_count(created_date=target_date)
    print('Number of sms sent is {}'.format(no_of_sms))
    context = {
        'emailsCount':email_sents.get('records')[0]['expr0'] if email_sents.get('records')[0]['expr0']>0 else None,
        'homeClosedCount':close_home_no.get('records')[0]['expr0'] if close_home_no.get('records')[0]['expr0'] >0 else None,
        'homeWonCount':won_home_no.get('records')[0]['expr0'] if won_home_no.get('records')[0]['expr0'] >0 else None,
        'callsCount':no_of_calls.get('records')[0]['expr0'] if no_of_calls.get('records')[0]['expr0']>0 else None,
        'smsCount':no_of_sms.get('records')[0]['expr0'] if no_of_sms.get('records')[0]['expr0'] >0 else None,
        'campaigns':sales_force_integration.query_all_sms_campaing(created_date=target_date)[:50],

    }

    return render(template_name='sales.html',context=context,request=request)