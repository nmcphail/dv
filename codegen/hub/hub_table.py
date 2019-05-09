from django.db import models
from django.template import loader
from django.shortcuts import get_object_or_404, render
from codegen.util.template_utils import render_template
from dventities.models import Hub, HubKeyField, HubSatelite




class HubTableGenerator():
    def __init__(self, hub):
        self.hub = hub
        self.hello = 'Hello'
        self.field_list = []
        self.field_list.append(self.hub.get_hash_key_field())
        self.field_list.append(self.hub.get_load_time_field())
        self.field_list.append(self.hub.get_record_source_field())
        
        for f in hub.key_fields.all():
            self.field_list.append(f)
        

    def get_artifact_text(self):
        ctx  = {'hub_table_generator' : self }
        return loader.render_to_string('codegen/hub/HubTable.txt', context=ctx)

class HubSateliteTableGenerator():
    def __init__(self, satelite):
        self.sat = satelite
        self.field_list = []
        self.field_list.append(self.sat.hub.get_hash_key_field())
        self.field_list.append(self.sat.get_load_time_field())
        self.field_list.append(self.sat.get_record_source_field())
        
        for f in self.sat.fields.all():
            self.field_list.append(f)



        self.primary_key_fields = []
        self.primary_key_fields.append(self.sat.hub.get_hash_key_field())
        self.primary_key_fields.append(self.sat.get_load_time_field())
        

    def get_artifact_text(self):
        ctx  = {'sat_table_generator' : self }
        #return loader.render_to_string('codegen/hub/HubSateliteTableGenerator.txt', context=ctx)
        return render_template('codegen/hub/HubSateliteTableGenerator.txt', ctx)
        
# Create your models here.
