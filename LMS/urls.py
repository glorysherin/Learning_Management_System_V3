from django.contrib import admin 
from django.urls import path, include
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

app_name = 'base' # add this line to define your app_name


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
    
]

handler500 = 'base.Routes.study.fivehundrederror'
handler404 = 'base.Routes.study.fournotfourerror'
handler403 = 'base.Routes.study.fournotthree'
handler400 = 'base.Routes.study.fourhundred'
