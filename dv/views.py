from django.shortcuts import render
from django.forms import ModelForm

# Create your views here.
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.views.generic import ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Submit, Row, Column

from dventities.models import *


class HubList(ListView):
    model = Hub
    template_name = 'dv/hub_list.html'
    
#    def get(self, request, *args, **kwargs):
#        hubs = Hub.objects.all()
#        st = StageTable.objects.first()
#        form = StageTableForm(instance=st)
#        return render(request,  self.template_name, )
        


class HubForm(ModelForm):
    class Meta:
        model = Hub
        fields = ['name', 'table_name']
        helptexts = {}
        readonly_fields = ['name', 'vault']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            
            
        self.helper = FormHelper()
        
        #self.helper.form_id = 'id-exampleForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = 'stage_tables'
        self.helper.help_text_inline = True
        self.helper.add_input(Submit('submit', 'Submit'))
        #self.helper.layout = Layout(
        #    Row(
        #        Column('name', css_class='form-group col-md-6 mb-0'),
        #        Column('vault', css_class='form-group col-md-6 mb-0'),
        #        Column('schema', css_class='form-group col-md-6 mb-0'),
        #        css_class='form-row'
        #    ),
        #    Row(
        #        Column('table_name', css_class='form-group col-md-6 mb-0'),
        #        Column('table_alias', css_class='form-group col-md-4 mb-0'),
        #        css_class='form-row'
        #    ),
        #    'root_name',
        #    Submit('submit', 'Sign in')
        #)
