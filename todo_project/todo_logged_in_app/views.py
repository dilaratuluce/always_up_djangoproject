import datetime
from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import TodoForm
from .models import Todo

# def index(request):
#    return render(request, "todo_logged_in_app/index.html")

"""
class Index(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request):
        return render(request, "todo_logged_in_app/index.html")
"""


class LogOutRequest(View):
    def get(self, request):
        logout(request)
        return redirect("/")


"""
şimdi burayı kapattım:
def form_page(request):
    if request.method == "POST":
        todo_form = TodoForm(request.POST or None)
        if todo_form.is_valid():
            todo_form.save()
            todos = Todo.objects.all()
            return render(request, "todo_logged_in_app/index.html", {'todos': todos})
        else:
            todos = Todo.objects.all()
            return render(request, "todo_app/index.html", {'todos': todos})
    else:
        todos = Todo.objects.all()
        return render(request, "todo_logged_in_app/index.html", {'todos': todos})
"""


class FormPage(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        todos = Todo.objects.all()
        return render(request, "todo_logged_in_app/index.html", {'todos': todos})

    def post(self, request):
        todo_form = TodoForm(request.POST or None)
        if todo_form.is_valid():
            instance = todo_form.save(commit=False)
            instance.creator = request.user
            instance.save()
            messages.success(request, "Todo is added succesfully.")

            todos = Todo.objects.all()
            return render(request, "todo_logged_in_app/index.html", {'todos': todos})
        else:
            messages.warning(request, "Todo is not added, please fill all the fields.")
            todos = Todo.objects.all()
            return render(request, "todo_logged_in_app/index.html", {'todos': todos})


"""
class FormPage(View):
    def post(self, request):
        todo_form = TodoForm(request.POST or None)
        if todo_form.is_valid():
            todo_form.save()
            todos = Todo.objects.all()
        #    return render(request, "todo_logged_in_app/index.html", {'todos': todos})
        #    return render(request, "todo_logged_in_app/index.html", {'todos': todos})
            return render(request=request, template_name="todo_logged_in_app/index.html", context={'todos': todos})

    def get(self, request):
        todos = Todo.objects.all()
    #    return render(request, "todo_logged_in_app/index.html", {'todos': todos})
        return render(request=request, template_name="todo_logged_in_app/index.html", context={'todos': todos})
      #  return render(request, "todo_logged_in_app/index.html")
   #     return render(request, "todo_logged_in_app/index.html", {'todos': todos})
   #     return render(request=request, template_name="todo_logged_in_app/index.html",
   #                   context={'todos': todos})
"""


def find_today_creators_todos(request):
    all_todos = Todo.objects.all()
    today_creators_todos = []
    for todo in all_todos:
        if todo.creator == request.user and todo.date == datetime.date.today():
            today_creators_todos.append(todo)
    return today_creators_todos


def my_to_dos(request):
    today_creators_todos = find_today_creators_todos(request)
    return render(request, "todo_logged_in_app/my_to_dos.html", {'today_creators_todos': today_creators_todos})


def delete(request, Todo_id):
    todo = Todo.objects.get(pk=Todo_id)
    todo.delete()
    return redirect("/user/my-to-dos")


def change_is_finished(request, Todo_id):
    todo = Todo.objects.get(pk=Todo_id)

    if todo.is_finished:
        todo.is_finished = False
        todo.save()
    else:
        todo.is_finished = True
        todo.save()
    return redirect("/user/my-to-dos")


def add_time(clock, time):
    result_clock = clock + timedelta(minutes=time)
    return result_clock


def make_schedule(request):
    begin_finish_clocks = []
    today_creators_todos = find_today_creators_todos(request)
    clock = datetime.datetime.now()
    today_creators_todos_notfinished = []
    for i in today_creators_todos:
        if not i.is_finished:
            today_creators_todos_notfinished.append(i)
    for i in today_creators_todos_notfinished:
        remaining_to_ten = add_time(clock, 10).minute % 10
        begin_clock = add_time(clock, 10 + (
                    10 - remaining_to_ten))  # 10 dk sonrasından itibaren en yakın 10 a bölünen dakikada başlatıyor
        finish_clock = add_time(begin_clock, i.length)
        todo_begin_finish_clock = [begin_clock.strftime("%H:%M"), finish_clock.strftime("%H:%M")]
        begin_finish_clocks.append(todo_begin_finish_clock)
        clock = finish_clock

    todo_and_clock_list = []
    for todo, begin_finish_clock in zip(today_creators_todos_notfinished, begin_finish_clocks):
        todo_and_clock_list.append([todo, begin_finish_clock])
    return render(request, "todo_logged_in_app/make_schedule.html",
                  {'today_creators_todos_notfinished': today_creators_todos_notfinished,
                   'begin_finish_clocks': begin_finish_clocks,
                   'todo_and_clock_list': todo_and_clock_list})


def my_daily_graph(request):
    today_creators_todos = find_today_creators_todos(request)
    finished = 0
    unfinished = 0
    for i in today_creators_todos:
        if i.is_finished:
            finished += 1
        else:
            unfinished += 1
    return render(request, "todo_logged_in_app/my_daily_graph.html", {'finished': finished, 'unfinished': unfinished})


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


def my_week_helper(num):
    if num < 0:
        return num + 7
    else:
        return num


def my_week(request):
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


def my_weekly_graph(request):
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
