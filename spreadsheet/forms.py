from django import forms
from django.utils.translation import gettext_lazy as _


class SubmergedWeightForm(forms.Form):
    pipe_outside_diameter = forms.FloatField(label=_('Pipe Outside Diameter (OD) (in)'), required=True, initial=10.75)
    pipe_wall_thickness = forms.FloatField(label=_('Pipe Wall Thickness (t) (in)'), required=True, initial=0.5)
    pipe_density = forms.FloatField(label=_('Pipe Density (lb/ft3)'), required=True, initial=490)
    corrosion_allowance = forms.FloatField(label=_('Corrosion Allowance (in)'), required=True, initial=0.125)

    # External Coating Data
    coating_thickness = forms.FloatField(label=_('Thickness (in)'), required=True, initial=0.0118110236220472)
    coating_density = forms.FloatField(label=_('Density (lb/ft3)'), required=True, initial=81.156348)

    # Pipeline Contents Data
    installation_empty_air_density = forms.FloatField(label=_('Installation Empty Air Density (lb/ft3)'), required=True, initial=0)
    flooded_water_density = forms.FloatField(label=_('Flooded Water Density (lb/ft3)'), required=True, initial=64)
    hydrotest_sea_water_density = forms.FloatField(label=_('Hydrotest Sea Water Density (lb/ft3)'), required=True, initial=64.7)

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
    #     super(ErequestForm, self).__init__(*args, **kwargs)
    #
    #     # Remove some field based on user
    #     if user.user_type=="Employee":
    #         fields_to_delete = ['status','hr_comments', 'management_comments' ]
    #     else:
    #         fields_to_delete = []
    #     if fields_to_delete:
    #         for field in fields_to_delete:
    #             del self.fields[field]
    #
    #     # Set read only base on user
    #     if user.user_type=="HR":
    #         self.fields['subject'].widget.attrs['readonly'] = True
    #         self.fields['description'].widget.attrs['readonly'] = True
    #         self.fields['file'].widget.attrs['readonly'] = True
    #         self.fields['management_comments'].widget.attrs['readonly'] = True
    #
    #     if user.user_type=="Management":
    #         self.fields['subject'].widget.attrs['readonly'] = True
    #         self.fields['description'].widget.attrs['readonly'] = True
    #         self.fields['file'].widget.attrs['readonly'] = True
    #         self.fields['hr_comments'].widget.attrs['readonly'] = True

class SignupForm(forms.Form):
 #django gives a number of predefined fields
 #CharField and EmailField are only two of them
 #go through the official docs for more field details
 name = forms.CharField(label='Enter your name', max_length=100)
 email = forms.EmailField(label='Enter your email', max_length=100)