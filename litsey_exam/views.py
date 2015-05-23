__author__ = 'shuhrat'
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

@login_required
def MainRedirect(request):
    return HttpResponseRedirect(reverse('journal:home'))
