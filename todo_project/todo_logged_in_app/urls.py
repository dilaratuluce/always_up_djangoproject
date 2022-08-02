from django.urls import path

from . import views

urlpatterns = [
    #   path('', views.Index.as_view(), name="index"),
    path('', views.FormPage.as_view(), name="index"),
    path("logout/", views.LogOutRequest.as_view(), name="logout"),
    path('my-to-dos/', views.my_to_dos, name="my_to_dos"),
    path('delete/<Todo_id>', views.delete, name='delete'),
    path('change_is_finished/<Todo_id>', views.change_is_finished, name="change_is_finished"),
    path('make-schedule/', views.make_schedule, name='make_schedule'),
    path('my-daily-graph/', views.my_daily_graph, name='my_daily_graph'),
    path('my-weekly-graph/', views.my_weekly_graph, name='my_weekly_graph'),
    path('my-week/', views.my_week, name='my_graphs'),
]
