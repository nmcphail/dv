from django.shortcuts import render
import django.forms as forms
from django.forms import ModelForm
from django.forms import formset_factory, modelformset_factory, BaseFormSet, BaseModelFormSet
from django.urls import reverse, reverse_lazy

from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Submit, Row, Column

from dventities.models import *


class HubSateliteForm(ModelForm):
    #edit = forms.URLField(required=False, )
        
    class Meta:
        model = HubSatelite
        fields = ['hub', 'name', 'table_name']
        #hidden_fields = ['hub']

    def __init__(self, hub, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub = hub

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

        if self.hub is not None:
            self.fields['hub'].initial = hub
    
        self.helper = FormHelper()
        self.helper.form_tag = False
        

class HubSateliteFormsetBase(BaseModelFormSet):
    def clean(self):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Row(
                Column('hub', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
    

    
HubSateliteFormset = modelformset_factory(
    HubSatelite,
    formset=HubSateliteFormsetBase,
    form=HubSateliteForm,
    extra=1,
    can_delete=True,
    can_order=True)


class HubKeyFieldForm(ModelForm):
    #edit = forms.URLField(required=False, )
        
    class Meta:
        model = HubKeyField
        fields = ['hub', 'field_name', ]
        #hidden_fields = ['hub']

    def __init__(self, hub, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub = hub

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

        if self.hub is not None:
            self.fields['hub'].initial = hub
    
        self.helper = FormHelper()
        self.helper.form_tag = False
        

class HubKeyFieldFormsetBase(BaseModelFormSet):
    def clean(self):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Row(
                Column('hub', css_class='form-group col-md-6 mb-0'),
                Column('field_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
    

    
HubKeyFieldFormset = modelformset_factory(
    HubKeyField,
    formset=HubKeyFieldFormsetBase,
    form=HubKeyFieldForm,
    extra=1,
    can_delete=True,
    can_order=True)




class HubChangeForm(ModelForm):
    class Meta:
        model = Hub
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
    
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = '' #reverse('hub_list')
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                #Column('id', type='Hidden'),
                Column('vault', css_class='form-group col-md-6 mb-0'),
                Column('schema', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('table_name', css_class='form-group col-md-6 mb-0'),
                Column('table_alias', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

#            Submit('submit', 'Save')
            
        )

        
    
class HubChangeView(FormView):
    model = Hub
    #fields = '__all__'
    template_name = 'dventities/hub_change.html'
    form_class = HubChangeForm

    def get_success_url(self):
        return reverse('hub_list')       
    
    def get(self, request, pk,  *args, **kwargs):
        
        hub = Hub.objects.get(pk=pk)
        form = HubChangeForm(instance=hub, prefix='hub_form')
        hub_satelite_formset = HubSateliteFormset(
            prefix='hub_satelite_formset',
            queryset=hub.hubsatelite_set.all(),
            form_kwargs={'hub': hub} )
        hub_key_field_formset = HubKeyFieldFormset(
            prefix='hub_key_field_formset',
            queryset=hub.hubkeyfield_set.all(),
            form_kwargs={'hub': hub} )
        
        return render(request, 'dventities/hub_change.html', {'form': form, 'sat_form' : None ,
                                                              'hub_satelite_formset' : hub_satelite_formset,
                                                              'hub_key_field_formset' : hub_key_field_formset })


    def post(self, request, pk,   *args, **kwargs):
        hub = Hub.objects.get(pk=pk)
        hub_form = HubChangeForm(request.POST, prefix='hub_form')
        
        if hub_form.is_valid():
            hub_form.instance.id = pk
            #print('is bound', hub_form.instance.id)
            hub_form.clean()
            hub_form.save()
        else:
            print('hub form not valid')
            print(hub_form.errors)

        hub_satelite_formset = HubSateliteFormset(
            request.POST,
            prefix='hub_satelite_formset',
            form_kwargs={'hub': hub} )

        if hub_satelite_formset.is_valid():
            hub_satelite_formset.clean()
            hub_satelite_formset.save()
        else:
            print(hub_satelite_formset.errors)

        hub_key_field_formset = HubKeyFieldFormset(
            request.POST,
            prefix='hub_key_field_formset',
            form_kwargs={'hub': hub} )

        if hub_key_field_formset.is_valid():
            hub_key_field_formset.clean()
            hub_key_field_formset.save()
        else:
            print(hub_key_field_formset.errors)
    
        return HttpResponseRedirect( self.get_success_url())



    
        
    
