from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Home view for items.  Items are displayed in a list.
class NewModelListView(ListView):
    template_name='index.html'
    context_object_name='newmodel_list'
    queryset = NewModel.objects.all()

#Detail view (view item detail)
class NewModelDetailView(DetailView):
    model = NewModel
    template_name = 'newmodel_detail.html'

#Create view (create item)
class NewModelCreateView(CreateView):
    model = NewModel
    template_name = 'newmodel_add.html'
    fields = '__all__'
    success_url = reverse_lazy('newmodel-list')

# Update view (update item)
class NewModelUpdateView(UpdateView):
    model = NewModel
    template_name = 'newmodel_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('newmodel-list')

#Delete view (delete a item)
class NewModelDeleteView(DeleteView):
    model = NewModel
    template_name = 'newmodel_delete.html'
    success_url = reverse_lazy('newmodel-list')
