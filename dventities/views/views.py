from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Submit, Row, Column

from dventities.models import *

        
    
def index(request):
    return("Hello, world. You're at the  index.")

def stage_tables(request):
    stage_tables = StageTable.objects.all()
    
    
    return render(request, 'dventities/stage_table_list.html', None)


class StageTableForm(ModelForm):
    class Meta:
        model = StageTable
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


class StageTableList(ListView):
    model = StageTable
    template_name = 'dventities/stage_table_list.html'
    
    def get(self, request, *args, **kwargs):
        stage_tables = StageTable.objects.all()
        st = StageTable.objects.first()
        form = StageTableForm(instance=st)
        return render(request,  self.template_name, { 'stage_tables' : stage_tables, 'form' : form } )
        
    def post(self, request, *args, **kwargs):
        stage_tables = StageTable.objects.all()
        stage_table_forms = []
        for st in stage_tables:
            stage_table_forms.append(StageTableForm(instance=st))
            
        st = StageTable.objects.first()
        form = StageTableForm(instance=st)
        return render(request,  self.template_name, { 'stage_tables' : stage_tables,
                                                      'form' : form,
                                                      'stage_table_forms' : stage_table_forms } )


class StageTableFieldList(ListView):
    model = StageTableField
    template_name = 'dventities/stage_table_field_list.html'
    
    def get(self, request, stage_table_id , *args, **kwargs):
        st = StageTable.objects.get(pk=stage_table_id)
        stage_table_fields = st.stagetablefield_set.all()
        return render(request,  self.template_name, { 'stage_table_fields' : stage_table_fields } )
    
