from django.conf.urls import url, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'firstapp'

urlpatterns = [
    # login default url
    url(r'^$', views.loginview, name='login'),
    url(r'^register/$', views.UserCreateView.as_view(), name='register'),
    url(r'^(?P<user_id>[0-9]+)/$', login_required(views.index), name='index'),
    url(r'addswap/$', login_required(views.AddSwapContractView.as_view()), name='add-swap'),
    url(r'swapdetails/(?P<emp_id>[0-9]+)/$', login_required(views.user_swap_details), name='swapdetails'),
    url(r'^openswapdetails/$', login_required(views.all_open_swap), name='openswapdetails'),
    url(r'^swapdelete/(?P<swap_id>[0-9]+)$', login_required(views.delete), name='swapdelete'),
    url(r'^contactpending/(?P<id_swap>[0-9]+)$', login_required(views.come_in_contract), name='contactpending'),
    url(r'^acceptcontract/(?P<accept_swap_id>[0-9]+)$', login_required(views.accept_contract), name='acceptcontract'),
    url(r'^declinecontract/(?P<decline_swap_id>[0-9]+)$', login_required(views.decline_contract), name='declinecontract'),
    url(r'^forgotpassword/$', views.forgotpasswordview, name='forgotpassword'),
    url(r'^newpassword/(?P<user_id_new_pass>[0-9]+)$', views.newpasswordview, name='newpassword'),
    url(r'^miscellaneous/$', login_required(views.pie_routing), name='miscellaneous'),
    url(r'^currencyswap/$', login_required(views.currency_swap), name='currencyswap'),
    url(r'^commodityswap/$', login_required(views.commodity_swap), name='commodityswap'),
    url(r'^derivativeswap/$', login_required(views.derivative_swap), name='derivativeswap'),
    url(r'^logout/$', views.logout, name='logout'),
]