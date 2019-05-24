from django.urls import path

from .views import views, hub_change

app_name = 'dventities'

urlpatterns = [
    path('', views.index, name='index'),
    path('stage_tables', views.StageTableList.as_view(), name='stage_tables' ),
    path('hub/<int:pk>/change', hub_change.HubChangeView.as_view(), name='hub_change'),
    path('stage_table_fields/<int:stage_table_id>', views.StageTableFieldList.as_view(), name='stage_table_field_list' ),
    
    
]

