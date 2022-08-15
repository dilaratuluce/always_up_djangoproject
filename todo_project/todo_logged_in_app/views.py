import datetime
from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import TodoForm, CategoryForm
from .models import Todo, TodoCategory

from django.http import HttpResponse, JsonResponse


class LogOutRequest(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/")


class FormPage(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        form = TodoForm
        form.base_fields['category'].limit_choices_to = {'creator': request.user}
        return render(request, "todo_logged_in_app/index.html", {'form': form})

    def post(self, request):
        form = TodoForm(request.POST or None)
  #      form.base_fields['category'].limit_choices_to = {'creator': request.user}
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
            messages.success(request, "Todo is added succesfully.")

            return render(request, "todo_logged_in_app/index.html", {'form': form})
        else:
            messages.warning(request, "Todo is not added, please fill all the fields.")
            return render(request, "todo_logged_in_app/index.html", {'form': form})


def find_today_creators_todos(request):
    today_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today())
    return today_creators_todos


def my_week_helper(num):
    if num < 0:
        return num + 7
    elif num > 6:
        return num - 7
    else:
        return num


def sort_by_category(todo_list, request):
    creators_categories = find_creators_categories(request)
    sorted_list = []
    for category in creators_categories:
        for todo in todo_list:
            if todo.category == category:
                sorted_list.append(todo)
    for todo in todo_list:
        if not todo.category:
            sorted_list.append(todo)
    return sorted_list


class MyToDos(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        todays_num = today.weekday()
        one_later_num = my_week_helper(todays_num + 1)
        two_later_num = my_week_helper(todays_num + 2)
        three_later_num = my_week_helper(todays_num + 3)
        four_later_num = my_week_helper(todays_num + 4)
        five_later_num = my_week_helper(todays_num + 5)
        six_later_num = my_week_helper(todays_num + 6)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today())
        tomorrow_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=1))
        two_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=2))
        three_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=3))
        four_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=4))
        five_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=5))
        six_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=6))
        return render(request, "todo_logged_in_app/my_to_dos.html",
                      {'today_creators_todos': sort_by_category(today_creators_todos, request),
                       'tomorrow_creators_todos': sort_by_category(tomorrow_creators_todos, request),
                       'two_later_creators_todos': sort_by_category(two_later_creators_todos, request),
                       'three_later_creators_todos': sort_by_category(three_later_creators_todos, request),
                       'four_later_creators_todos': sort_by_category(four_later_creators_todos, request),
                       'five_later_creators_todos': sort_by_category(five_later_creators_todos, request),
                       'six_later_creators_todos': sort_by_category(six_later_creators_todos, request),
                       'today': days[todays_num],
                       'tomorrow': days[one_later_num],
                       'two_later_day': days[two_later_num],
                       'three_later_day': days[three_later_num],
                       'four_later_day': days[four_later_num],
                       'five_later_day': days[five_later_num],
                       'six_later_day': days[six_later_num]})


class Delete(LoginRequiredMixin, View):
    def get(self, request, Todo_id):
        todo = Todo.objects.get(pk=Todo_id)
        todo.delete()
        return redirect("/user/my-to-dos")


class ChangeIsFinished(LoginRequiredMixin, View):
    def get(self, request, Todo_id):
        todo = Todo.objects.get(pk=Todo_id)
        if todo.is_finished:
            todo.is_finished = False
            todo.save()
        else:
            todo.is_finished = True
            todo.save()
        return redirect("/user/my-to-dos")


def change_finished(request, Todo_id):  # şu an kullanılmıyor, deneme için yazıldı
    todo = Todo.objects.get(pk=Todo_id)
    if todo.is_finished:
        todo.is_finished = False
        todo.save()
    else:
        todo.is_finished = True
        todo.save()
    todos = Todo.objects.all()
    return JsonResponse({"todos": list(todos.values())})


class ChangeFinished(View):   # şu an kullanılmıyor, deneme için yazıldı
    def get(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            todo = Todo.objects.get(pk=pk)
            if todo.is_finished:
                todo.is_finished = False
                todo.save()
            else:
                todo.is_finished = True
                todo.save()
            return JsonResponse({'message:': "success"})
        return JsonResponse({"message": "Wrong route"})


def add_time(clock, time):
    result_clock = clock + timedelta(minutes=time)
    return result_clock


def find_today_creators_todos_notfinished(request):
    today_creators_todos = find_today_creators_todos(request)
    today_creators_todos_notfinished = []
    for i in today_creators_todos:
        if not i.is_finished:
            today_creators_todos_notfinished.append(i)
    return today_creators_todos_notfinished


def set_schedule_clocks(request, list):
    begin_finish_clocks = []
    clock = datetime.datetime.now()
    for i in list:
        remaining_to_ten = add_time(clock, 10).minute % 10
        begin_clock = add_time(clock, 10 + (
                10 - remaining_to_ten))  # 10 dk sonrasından itibaren en yakın 10 a bölünen dakikada başlatıyor
        finish_clock = add_time(begin_clock, i.length)
        todo_begin_finish_clock = [begin_clock.strftime("%H:%M"), finish_clock.strftime("%H:%M")]
        begin_finish_clocks.append(todo_begin_finish_clock)
        clock = finish_clock

    todo_and_clock_list = []
    for todo, begin_finish_clock in zip(list, begin_finish_clocks):
        todo_and_clock_list.append([todo, begin_finish_clock])
    return todo_and_clock_list


def make_schedule_default_order(request):
    today_creators_todos_notfinished = find_today_creators_todos_notfinished(request)
    todo_and_clock_list = set_schedule_clocks(request, today_creators_todos_notfinished)
    return todo_and_clock_list


def make_schedule_short_first(request):
    today_creators_todos_notfinished = find_today_creators_todos_notfinished(request)
    for i in range(len(today_creators_todos_notfinished)):
        for j in range(len(today_creators_todos_notfinished) - 1):
            if today_creators_todos_notfinished[j].length > today_creators_todos_notfinished[j + 1].length:
                today_creators_todos_notfinished[j], today_creators_todos_notfinished[j + 1] = today_creators_todos_notfinished[j + 1], today_creators_todos_notfinished[j]

    todo_and_clock_list = set_schedule_clocks(request, today_creators_todos_notfinished)
    return todo_and_clock_list


def make_schedule_long_first(request):
    today_creators_todos_notfinished = find_today_creators_todos_notfinished(request)
    for i in range(len(today_creators_todos_notfinished)):
        for j in range(len(today_creators_todos_notfinished) - 1):
            if today_creators_todos_notfinished[j].length < today_creators_todos_notfinished[j + 1].length:
                today_creators_todos_notfinished[j], today_creators_todos_notfinished[j + 1] = today_creators_todos_notfinished[j + 1], today_creators_todos_notfinished[j]

    todo_and_clock_list = set_schedule_clocks(request, today_creators_todos_notfinished)
    return todo_and_clock_list


def make_schedule_important_first(request):
    priority_dict = {'low': 1,
                     'normal': 2,
                     'high': 3,
                     'very_high': 4}

    today_creators_todos_notfinished = find_today_creators_todos_notfinished(request)
    for i in range(len(today_creators_todos_notfinished)):
        for j in range(len(today_creators_todos_notfinished) - 1):
            if priority_dict[today_creators_todos_notfinished[j].priority] < priority_dict[today_creators_todos_notfinished[j + 1].priority]:
                today_creators_todos_notfinished[j], today_creators_todos_notfinished[j + 1] = today_creators_todos_notfinished[j + 1], today_creators_todos_notfinished[j]

    todo_and_clock_list = set_schedule_clocks(request, today_creators_todos_notfinished)
    return todo_and_clock_list


def length_score(length):
    if length<=15:
        return 4
    elif length<=30:
        return 3
    elif length<=50:
        return 2
    else:
        return 1


def make_schedule_suggested_schedule(request):
    priority_dict = {'low': 1,
                     'normal': 2,
                     'high': 3,
                     'very_high': 4}

    today_creators_todos_notfinished = find_today_creators_todos_notfinished(request)
    for i in range(len(today_creators_todos_notfinished)):
        for j in range(len(today_creators_todos_notfinished) - 1):
            priority_score1 = priority_dict[today_creators_todos_notfinished[j].priority]
            length_score1 = length_score(today_creators_todos_notfinished[j].length)
            priority_score2 = priority_dict[today_creators_todos_notfinished[j+1].priority]
            length_score2 = length_score(today_creators_todos_notfinished[j+1].length)
            todo1_score = priority_score1 + length_score1
            todo2_score = priority_score2 + length_score2
            if todo1_score < todo2_score:
                today_creators_todos_notfinished[j], today_creators_todos_notfinished[j + 1] = today_creators_todos_notfinished[j + 1], today_creators_todos_notfinished[j]

    todo_and_clock_list = set_schedule_clocks(request, today_creators_todos_notfinished)
    return todo_and_clock_list


class MakeSchedule(LoginRequiredMixin, View):
    def get(self, request):
        todo_and_clock_list = make_schedule_default_order(request)
        todo_and_clock_list_short_first = make_schedule_short_first(request)
        todo_and_clock_list_long_first = make_schedule_long_first(request)
        todo_and_clock_list_important_first = make_schedule_important_first(request)
        todo_and_clock_list_suggested = make_schedule_suggested_schedule(request)
        return render(request, "todo_logged_in_app/make_schedule.html",
                      {'todo_and_clock_list': todo_and_clock_list,
                       'todo_and_clock_list_short_first': todo_and_clock_list_short_first,
                       'todo_and_clock_list_long_first': todo_and_clock_list_long_first,
                       'todo_and_clock_list_important_first': todo_and_clock_list_important_first,
                       'todo_and_clock_list_suggested': todo_and_clock_list_suggested})


class MyDailyGraph(LoginRequiredMixin, View):
    def get(self, request):
        today_creators_todos = find_today_creators_todos(request)
        finished = 0
        unfinished = 0
        for i in today_creators_todos:
            if i.is_finished:
                finished += 1
            else:
                unfinished += 1
        return render(request, "todo_logged_in_app/my_daily_graph.html",
                      {'finished': finished, 'unfinished': unfinished})


def find_history_todos(request):
    today_todos = []
    one_before_todos = []
    two_before_todos = []
    three_before_todos = []
    four_before_todos = []
    five_before_todos = []
    six_before_todos = []

    today = date.today()
    one_before = today - timedelta(days=1)
    two_before = today - timedelta(days=2)
    three_before = today - timedelta(days=3)
    four_before = today - timedelta(days=4)
    five_before = today - timedelta(days=5)
    six_before = today - timedelta(days=6)
    creators_todos = find_creators_todos(request)
    for todo in creators_todos:
        if todo.date == today:
            today_todos.append(todo)
        elif todo.date == one_before:
            one_before_todos.append(todo)
        elif todo.date == two_before:
            two_before_todos.append(todo)
        elif todo.date == three_before:
            three_before_todos.append(todo)
        elif todo.date == four_before:
            four_before_todos.append(todo)
        elif todo.date == five_before:
            five_before_todos.append(todo)
        elif todo.date == six_before:
            six_before_todos.append(todo)
    return today_todos, one_before_todos, two_before_todos, three_before_todos, four_before_todos, five_before_todos, six_before_todos


def find_creators_todos(request):
    all_todos = Todo.objects.all()
    creators_todos = []
    for todo in all_todos:
        if todo.creator == request.user:
            creators_todos.append(todo)
    return creators_todos

"""
def my_week_helper(num):
    if num < 0:
        return num + 7
    else:
        return num
"""

class MyWeek(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        todays_num = today.weekday()
        one_day_ago_num = my_week_helper(todays_num - 1)
        two_days_ago_num = my_week_helper(todays_num - 2)
        three_days_ago_num = my_week_helper(todays_num - 3)
        four_days_ago_num = my_week_helper(todays_num - 4)
        five_days_ago_num = my_week_helper(todays_num - 5)
        six_days_ago_num = my_week_helper(todays_num - 6)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(todays_num, days[todays_num])
        print(two_days_ago_num, days[two_days_ago_num])
        print(six_days_ago_num, days[six_days_ago_num])

        today_todos, one_before_todos, two_before_todos, three_before_todos, four_before_todos, five_before_todos, six_before_todos = find_history_todos(
            request)
        return render(request, "todo_logged_in_app/my_week.html", {'one_before_todos': one_before_todos,
                                                                   'two_before_todos': two_before_todos,
                                                                   'three_before_todos': three_before_todos,
                                                                   'four_before_todos': four_before_todos,
                                                                   'five_before_todos': five_before_todos,
                                                                   'six_before_todos': six_before_todos,
                                                                   'today': days[todays_num],
                                                                   'yesterday': days[one_day_ago_num],
                                                                   'two_days_ago': days[two_days_ago_num],
                                                                   'three_days_ago': days[three_days_ago_num],
                                                                   'four_days_ago': days[four_days_ago_num],
                                                                   'five_days_ago': days[five_days_ago_num],
                                                                   'six_days_ago': days[six_days_ago_num]})


class MyWeeklyGraph(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        todays_num = today.weekday()
        one_day_ago_num = my_week_helper(todays_num - 1)
        two_days_ago_num = my_week_helper(todays_num - 2)
        three_days_ago_num = my_week_helper(todays_num - 3)
        four_days_ago_num = my_week_helper(todays_num - 4)
        five_days_ago_num = my_week_helper(todays_num - 5)
        six_days_ago_num = my_week_helper(todays_num - 6)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(todays_num, days[todays_num])
        print(two_days_ago_num, days[two_days_ago_num])
        print(six_days_ago_num, days[six_days_ago_num])

        today_todos, one_before_todos, two_before_todos, three_before_todos, four_before_todos, five_before_todos, six_before_todos = find_history_todos(
            request)
        todos_per_day_list = [today_todos, one_before_todos, two_before_todos, three_before_todos, four_before_todos,
                              five_before_todos, six_before_todos]
        days_scores_list = []
        for todo_list in todos_per_day_list:
            finished = 0
            unfinished = 0
            for todo in todo_list:
                if todo.is_finished:
                    finished += 1
                else:
                    unfinished += 1
            if finished or unfinished:
                day_score = round((finished / (finished + unfinished)) * 100, 1)
            else:
                day_score = 0
            days_scores_list.append(day_score)
        return render(request, "todo_logged_in_app/my_weekly_graph.html", {'todays_score': days_scores_list[0],
                                                                           'one_before_score': days_scores_list[1],
                                                                           'two_before_score': days_scores_list[2],
                                                                           'three_before_score': days_scores_list[3],
                                                                           'four_before_score': days_scores_list[4],
                                                                           'five_before_score': days_scores_list[5],
                                                                           'six_before_score': days_scores_list[6],
                                                                           'today': days[todays_num],
                                                                           'yesterday': days[one_day_ago_num],
                                                                           'two_days_ago': days[two_days_ago_num],
                                                                           'three_days_ago': days[three_days_ago_num],
                                                                           'four_days_ago': days[four_days_ago_num],
                                                                           'five_days_ago': days[five_days_ago_num],
                                                                           'six_days_ago': days[six_days_ago_num]})


def find_creators_categories(request):
    creators_categories = TodoCategory.objects.filter(creator=request.user)
    return creators_categories


class MyCategories(View):
    def get(self, request):
        categories = find_creators_categories(request)
        form = CategoryForm
        return render(request, "todo_logged_in_app/categories.html", {'form': form, 'categories': categories})

    def post(self, request):
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
            categories = TodoCategory.objects.all()
            return JsonResponse({"categories2": list(categories.values()),
                                 "added_category": form.instance.id})
      #      return render(request, "todo_logged_in_app/categories.html", {'form': form, 'categories': categories})
        else:
            messages.warning(request, "Category is not added.")
            categories = TodoCategory.objects.all()
            return render(request, "todo_logged_in_app/categories.html", {'form': form, 'categories': categories})


class MyCategoriesDelete(View):
    def post(self, request):
        deleted_id = request.POST.get('deleted_id')
        print(deleted_id)
        TodoCategory.objects.get(pk=deleted_id).delete()
        categories = TodoCategory.objects.all()
        return JsonResponse({"categories3": list(categories.values())})





