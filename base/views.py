from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class TaskLoginView(LoginView):
    template_name = 'base/tasklogin.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegistrationPage(FormView):
    template_name = 'base/registration_page.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegistrationPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegistrationPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/detailview.html'
    # context_object_name = 'task'

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/deletetask.html'
    success_url = reverse_lazy('tasks')