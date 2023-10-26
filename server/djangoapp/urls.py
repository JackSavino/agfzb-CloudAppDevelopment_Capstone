from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for static view
    path('static-view/', views.static_view, name='static-view'),

    # path for about view
    path('about/', views.about, name='about'),

    # path for contact us view
    path('contact/', views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logout
    path('index/', views.logout_request, name='logout'),

    # path for all dealerships view
    path(route='dealership-package/get_dealerships', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealership-package/get_reviews', view=views.get_dealer_details, name='get-reviews'),

    # path for add a review view
    # path(route='dealership-package/post_review', view=views.post_review, name='post-review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)