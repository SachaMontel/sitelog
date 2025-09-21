from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # Login
    path('fichiers/', include('fichiers.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('gl/', views.gl, name='gl'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Signup
    path('signup/', views.signup, name='signup'),

    # Home
    path('home/', views.home, name='home'),

    # CDC
    path('cdc/', views.cdc, name='cdc'),

    path('logistique/', views.logistique, name='logistique'),
    path('anbb/', views.anbb, name='anbb'),
    path('anbc/', views.anbc, name='anbc'),
    path('anbm/', views.anbm, name='anbm'),
    path('anbp/', views.anbp, name='anbp'),
    path('anrgl/', views.anrgl, name='anrgl'),
    path('statbb/', views.statbb, name='statbb'),
    path('statbc/', views.statbc, name='statbc'),
    path('statbm/', views.statbm, name='statbm'),
    path('statbp/', views.statbp, name='statbp'),
    path('bcstats/', views.bcstats, name='bcstats'),
    path('bmstats/', views.bmstats, name='bmstats'),
    path('glstats/', views.glstats, name='glstats'),
    path('camp/<str:numero>/', views.camp_detail, name='camp_detail'),
    path('upload/<str:file_type>/<str:camp_id>/', views.upload_file, name='upload_file'),
    path('upload_qg/<str:file_type>/<str:camp_id>/', views.upload_file_qg, name='upload_file_qg'),
    path('delete_file/<str:file_type>/<str:camp_id>/', views.delete_file, name='delete_file'),
    path('delete_file_qg/<str:file_type>/<str:camp_id>/', views.delete_file_qg, name='delete_file_qg'),
    path('update_file_state/<str:file_type>/<str:camp_id>/', views.update_file_state, name='update_file_state'),
    path('update_file_state_cdc/<str:file_type>/<str:camp_id>/', views.update_file_state_cdc, name='update_file_state_cdc'),
    path('modifier_commentaire/<str:file_type>/<str:camp_id>/', views.modifier_commentaire, name='modifier_commentaire'),
    path('change_etat/', views.change_etat, name='change_etat'),
    path('update_comment/', views.update_comment, name='update_comment'),
    path('bc/', views.bc, name='bc'),
    path('bm/', views.bm, name='bm'),
    path('log/', views.log, name='log'),
    path('cga/', views.cga, name='cga'),
    path('gl2/<str:username>/', views.gl2, name='gl2'),
    path('simulation/', views.simulation, name='simulation'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
