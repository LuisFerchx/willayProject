from django.urls import path

from web_services.views import *

urlpatterns = [
    path('',HomePage,name='formulario'),
    path('inspection/',ws_inspection.as_view(),name='inspection'),
    path('inspection_file/s3_upload/',ws_sendToS3.as_view(),name='s3_upload'),
    # path('case/inspection/',ws_controller.as_view(),name='inspection'),
]