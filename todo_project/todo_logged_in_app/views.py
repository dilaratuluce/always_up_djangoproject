import datetime
from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import TodoForm
from .models import Todo

from django.http import HttpResponseRedirect


class LogOutRequest(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/")


class FormPage(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        form = TodoForm
        return render(request, "todo_logged_in_app/index.html", {'form': form})

    def post(self, request):
        form = TodoForm(request.POST or None)
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
        tomorrow_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()-timedelta(days=1))
        two_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=2))
        three_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=3))
        four_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=4))
        five_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=5))
        six_later_creators_todos = Todo.objects.filter(creator=request.user, date=datetime.date.today()+timedelta(days=6))
        return render(request, "todo_logged_in_app/my_to_dos.html",
                      {'today_creators_todos': today_creators_todos,
                       'tomorrow_creators_todos': tomorrow_creators_todos,
                       'two_later_creators_todos': two_later_creators_todos,
                       'three_later_creators_todos': three_later_creators_todos,
                       'four_later_creators_todos': four_later_creators_todos,
                       'five_later_creators_todos': five_later_creators_todos,
                       'six_later_creators_todos': six_later_creators_todos,
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


def add_time(clock, time):
    result_clock = clock + timedelta(minutes=time)
    return result_clock


class MakeSchedule(LoginRequiredMixin, View):
    def get(self, request):
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
                      {'todo_and_clock_list': todo_and_clock_list})


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
