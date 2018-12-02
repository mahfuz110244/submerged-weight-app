# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SubmergedWeightForm
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

def SubmergedWeightCreateForm(request):
    template_name = 'spreadsheet/post_form.html'
    # if form is submitted
    if request.method == 'POST':
        # will handle the request later
        form = SubmergedWeightForm(request.POST)

        # checking the form is valid or not
        if form.is_valid():
        # if valid rendering new view with values
        # the form values contains in cleaned_data dictionary
            return render(request, template_name, {'form':form})
            # return render(request, 'result.html', {
            #     'name': form.cleaned_data['name'],
            #     'email': form.cleaned_data['email'],
            # })
    else:
        # creating a new form
        form = SubmergedWeightForm()
    return render(request, template_name, {'form':form})