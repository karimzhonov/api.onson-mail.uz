from django.http.response import HttpResponsePermanentRedirect
from rest_framework.response import Response
from contrib.myid import MyId
from .models import Client

def myid_auth(request):
    url = MyId().get_auth_url(request.query_params.get('next'))
    return HttpResponsePermanentRedirect(url)



def myid_code(request, code):
    myid = MyId()
    token = myid.get_token(code)
    data = MyId().get_data_by_token(token)
    common_data = data.get('profile', {}).get('common_data', {})

    # Client.objects.update_or_create({
    #     passport=
    # }, pnfl=common_data.get('pinfl'))
    return Response("success", 200)
