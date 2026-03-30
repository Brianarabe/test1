from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    AboutPageView,
    ListingsPageView,
    View_propertyPageView,
    SearchPageView,
    ContactPageView,
    BasePageView,
    register_view,
    login_view,
    BrokerDashboardView,
    AgentDashboardView,
    BuyerDashboardView,
    ManageAgentsView,
    ManagepropertiesView,
    ViewBuyersView,
    agent_dashboard_view,
    add_property,
    edit_property,
    delete_property,
    add_review,
    agents,
    search_properties

)

urlpatterns = [
    # -------------------------
    # Public / General Pages
    # -------------------------
    path('', BasePageView.as_view(), name='base'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('agent/listings/', ListingsPageView.as_view(), name='listings'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('property/', View_propertyPageView.as_view(), name='property'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('search/', search_properties, name='search_properties'),

    # -------------------------
    # Broker Dashboard Section
    # -------------------------
    path('broker_dashboard/', BrokerDashboardView.as_view(), name='broker_dashboard'),

    # Broker Management Pages
    path('broker/agents/', ManageAgentsView.as_view(), name='manage_agents'),         # Manage agents
    path('broker/properties/', ManagepropertiesView.as_view(), name='manage_properties'),  # Manage properties

    # -------------------------
    # Agent Dashboard Section
    # -------------------------
    path('agent/agents/', agents, name='agents'),
    path('agent/dashboard/', agent_dashboard_view, name='agent_dashboard'),
    path('agent/add-property/', add_property, name='add_property'),
    path('agent/edit-property/<int:id>/', edit_property, name='edit_property'),
    path('agent/delete-property/<int:id>/', delete_property, name='delete_property'),
    path('agent/buyers/', ViewBuyersView.as_view(), name='view_buyers'),

    # agent Management Pages
    path('agent/buyers/', ViewBuyersView.as_view(), name='view_buyers'),   # View buyers

    path('buyer_dashboard/', BuyerDashboardView.as_view(), name='buyer_dashboard'),
    
    # Reviews
    path('add-review/', add_review, name='add_review'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)