# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SubmergedWeightForm
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
import math

def SubmergedWeightCreateForm(request):
    template_name = 'spreadsheet/post_form.html'
    template_details = 'spreadsheet/post_detail.html'
    # if form is submitted
    if request.method == 'POST':
        # will handle the request later
        form = SubmergedWeightForm(request.POST)

        # checking the form is valid or not
        if form.is_valid():
            # if valid rendering new view with values
            # the form values contains in cleaned_data dictionary
            pipe_outside_diameter = form.cleaned_data['pipe_outside_diameter'] #B5
            pipe_wall_thickness = form.cleaned_data['pipe_wall_thickness'] #B6
            pipe_density = form.cleaned_data['pipe_density'] #B7
            corrosion_allowance = form.cleaned_data['corrosion_allowance'] #B8

            coating_thickness = form.cleaned_data['coating_thickness'] #C11
            coating_density = form.cleaned_data['coating_density'] #D11

            installation_empty_air_density = form.cleaned_data['installation_empty_air_density'] #C15
            flooded_water_density = form.cleaned_data['flooded_water_density'] #C16
            hydrotest_sea_water_density = form.cleaned_data['hydrotest_sea_water_density'] #C17


            # Calculate now output based on input
            # E3=($Input.B5-2*$Input.B6)/2
            pipe_inside_radius = (pipe_outside_diameter - 2*pipe_wall_thickness)/2
            print(pipe_inside_radius)

            # E4=$Input.B5/2
            pipe_outside_radius = pipe_outside_diameter/2
            print(pipe_outside_radius)

            # E5=E4+$Input.C11/2
            outer_radius_of_coating = pipe_outside_radius + coating_thickness/2
            print(outer_radius_of_coating)

            # E6=E5*2
            total_pipeline_outside_diameter = outer_radius_of_coating*2
            print(total_pipeline_outside_diameter)

            # E9=PI()*(E4^2-E3^2)/144*$Input.B7
            pipe_weight = math.pi * (math.pow(pipe_outside_radius,2)- math.pow(pipe_inside_radius, 2)) / 144 * pipe_density
            print(pipe_weight)

            # E10=PI()*(E4^2-E3^2)/144*$Input.B7
            coating_weight = math.pi * (math.pow(outer_radius_of_coating, 2) - math.pow(pipe_outside_radius, 2)) / 144 * coating_density
            print(coating_weight)

            # E11=PI()*$E$3^2/144*$Input.$C$15
            content_weight = math.pi * (math.pow(pipe_inside_radius, 2)) / 144 * installation_empty_air_density
            print(content_weight)

            # E12=SUM(E9:E11)
            total_weight = pipe_weight + coating_weight + content_weight
            print(total_weight)

            # E13=PI()*E5^2/144*$Input.C17
            buoyant_force = math.pi * (math.pow(outer_radius_of_coating, 2)) / 144 * hydrotest_sea_water_density
            print(buoyant_force)

            # B18=$Output.E12-$Output.$E$13
            submerged_weight = total_weight - buoyant_force
            print(submerged_weight)

            # C18=$Output.E12/$Output.$E$13
            submerged_specific_gravity = total_weight / buoyant_force
            print(submerged_specific_gravity)

            return render(request, template_details, {
                'pipe_inside_radius': pipe_inside_radius,
                'pipe_outside_radius': pipe_outside_radius,
                'outer_radius_of_coating': outer_radius_of_coating,
                'total_pipeline_outside_diameter': total_pipeline_outside_diameter,
                'pipe_weight': pipe_weight,
                'coating_weight': coating_weight,
                'content_weight': content_weight,
                'total_weight': total_weight,
                'buoyant_force': buoyant_force,
                'submerged_weight': submerged_weight,
                'submerged_specific_gravity': submerged_specific_gravity
            })
    else:
        # creating a new form
        form = SubmergedWeightForm()
    return render(request, template_name, {'form':form})