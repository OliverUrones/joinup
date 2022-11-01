from apps.users.api.v1.urls import urlpatterns as users_urls

urlpatterns = []

urls_list = [users_urls]

for url in urls_list:
    urlpatterns += url
