from django.urls import path
from . import views
from django_cas_ng import views as cas_views
from django.urls import include # only for uni auth cas
#from django.conf.urls import url # only for uni auth cas

urlpatterns = [
    path('', views.index, name='index'),
    path('report/<uuid:itemid>', views.itemreported, name='report'),
    path("account/", views.account, name="account"), 
    path("inspectitem/", views.inspectitem, name="inspectitem"),
    #path("inspectitem/propose/areusure/", views.areusure, name="areusure"), 
    path("postitem/itemposted/", views.itemposted, name="itemposted"),
    path("inspectitem/propose/postitem/itemposted/", views.itemposted, name="itemposted"),  
    path("inspectitem/report/itemreported", views.itemreported, name="itemreported"), 
    path("account/proposal/swaprejected/report/itemreported", views.itemreported, name="itemreported"), 
    path("inspectitem/'<uuid:itemid>/processproposal/", views.processproposal, name="processproposal"),
    path("inspectitem/propose/proposalsent/", views.proposalsent, name="proposalsent"), #**********
    path("account/proposal/swaprejected/", views.swaprejected, name="swaprejected"), 
    path("account/proposal/swapsuccessful/", views.swapsuccessful, name="swapsuccessful"), 
    path("postitem/", views.postitem, name="postitem"),
    path("inspectitem/propose/postitem/", views.postitem, name="postitem"),
    path("account/proposal/", views.proposal, name="proposal"),
    path("account/proposal/report/", views.report, name="report"),
    path("account/proposal/<uuid:proposalid>/proposalacceptance/", views.proposalacceptance, name="proposalacceptance"),
    # path("account/proposal/proposalacceptance/", views.proposalacceptance, name="proposalacceptance"),
    path("account/proposal/proposalrejection/", views.proposalrejection, name="proposalrejection"),
    path("inspectitem/propose/", views.propose, name="propose"),
    path("inspectitem/report/", views.report, name="report"),
    path("account/proposal/swaprejected/report/", views.report, name="report"),
    path('login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
     path('logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
     path('accountstatus/', views.account_status, name= 'accountstatus'),
      path("inspectitem/'<uuid:itemid>/edititem/", views.edit_item, name="edit_item"),
    path('get_item_data/<uuid:item_id>/', views.get_item_data, name='get_item_data'),
    path('settings/', views.settings, name='settings'),
    path('<uuid:proposalid>rescindproposal/', views.rescind_proposal, name='rescind_proposal'),
    path('searchresults', views.get_results, name = 'get_results'),
    path("inspectitem/<uuid:itemid>/deleteitem/", views.delete_item, name="delete_item"),
    path("deleteitem/", views.delete_item, name="delete_item"),
     path("help/", views.help, name="help"),
     
    
    # inspectitem/propose/postitem/cancel should take you back to propose page but instead takes you to home page
    # inspectitem/propose/postitem should take you back to propose page but instead takes you to item posted page
    # account/proposal/swaprejected/report/cancel should take you to account but takes you to inspectitem page
    # account/proposal/swaprejected/report/itemreported/okay should take you to account but takes you to home page
]