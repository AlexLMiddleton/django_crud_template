from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

