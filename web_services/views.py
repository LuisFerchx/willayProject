import asyncio
from time import sleep

from aiohttp import ClientSession
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render
import base64
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import requests

state = 'buenas'

# Frontend
def HomePage(request):
    if request.method  == "POST":
        filename = request.FILES['file_name'].name
        filebytes = request.FILES['file_name'].read()
        filebase64 = base64.b64encode(filebytes)
        body = {
            'filename': filename,
            'fileBytesAsBase64': filebase64.decode,
        }
        sleep(5)
        ws_inspection.filesToS3LoadingStatus = 'ON_PROGRESS'
        sleep(5)
        url = 'http://127.0.0.1:8000/case/inspection_file/s3_upload/'
        response = requests.get(url,params=body)
        print(response)
        sleep(5)
        return render(request, 'home.html',context={'response': '1'})
    return render(request, 'home.html',)


# Controller
class ws_sendToS3(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    async def get(self, request):
        async with ClientSession() as session:
            try: # sucessfully
                url = 'https://rickandmortyapi.com/api/character/1' #representacion de la api AWS3
                name = await asyncio.wait_for(get_s3response(session, url=url),timeout=8)
                ws_inspection.filesToS3LoadingStatus = 'SUCESSFULLY'
                return JsonResponse({'name': 'arhchivo '+name+' subido con exito!'})
            except: # error
                ws_inspection.filesToS3LoadingStatus = 'FAILED'
                return JsonResponse({'error': 'No se ha podido subir el archivo!'})


async def get_s3response(session,url : str) -> str:
    # await asyncio.sleep(10)
    response = await session.get(url)
    json = await response.json()
    return json['name']


# Inspection
class ws_inspection(View):
    filesToS3LoadingStatus = 'PENDING'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'filesToS3LoadingStatus': self.filesToS3LoadingStatus})

