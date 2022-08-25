from django.urls import path
from . import views

urlpatterns = [
    path('', views.FormPage.as_view(), name="index"),
    path("logout/", views.LogOutRequest.as_view(), name="logout"),
    path('my-to-dos/', views.MyToDos.as_view(), name="my_to_dos"),
    path('delete/<Todo_id>/<starred_page>', views.Delete.as_view(), name='delete'),
    path('change_is_finished/<Todo_id>/<starred_page>', views.ChangeIsFinished.as_view(), name="change_is_finished"),
    path('make-schedule/', views.MakeSchedule.as_view(), name='make_schedule'),
    path('my-daily-graph/', views.MyDailyGraph.as_view(), name='my_daily_graph'),
    path('my-weekly-graph/', views.MyWeeklyGraph.as_view(), name='my_weekly_graph'),
    path('my-week/', views.MyWeek.as_view(), name='my_graphs'),
    path('mycategories/', views.MyCategories.as_view(), name='mycategories'),
    path('mycategories/delete', views.MyCategoriesDelete.as_view(), name='mycategories_delete'),
    path('star/<Todo_id>/<starred_page>', views.Star.as_view(), name='star'),
    path('starred-to-dos/', views.StarredToDos.as_view(), name="my_to_dos"),
    path('category-graph/', views.CategoryGraph.as_view(), name="my_to_dos"),
]
