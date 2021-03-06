from django.db import models
from django.template import loader
from django.shortcuts import get_object_or_404, render
from codegen.util.template_utils import render_template

from codegen.exceptions import CodeGenerationError

from dventities.models import *




class HubTableGenerator():
    def __init__(self, hub):
        self.hub = hub
        self.hello = 'Hello'
        self.field_list = []
        self.field_list.append(self.hub.get_hash_key_field())
        self.field_list.append(self.hub.get_load_time_field())
        self.field_list.append(self.hub.get_record_source_field())
        
        for f in hub.hubkeyfield_set.all():
            self.field_list.append(f)
        

    def get_artifact_text(self):
        ctx  = {'hub_table_generator' : self }
        return loader.render_to_string('codegen/hub/HubTable.txt', context=ctx)

class HubLatestViewGenerator():

    def __init__(self, hub):
        self.hub = hub
        self.hello = 'Hello'
        self.satelites = self.hub.hubsatelite_set.all()
        
        self.field_list = []
        self.field_list.append(self.hub.get_hash_key_field())
        self.field_list.append(self.hub.get_load_time_field())
        self.field_list.append(self.hub.get_record_source_field())
        self.schema = 'gdelt_hana'
        self.view_name = '{}_latest'.format( self.hub.table_name)
        
        for f in hub.hubkeyfield_set.all():
            self.field_list.append(f)


        self.sat_field_column_names = []
        #for sat in self.satelites:
            
        

    def get_artifact_text(self):
        ctx  = {'gen' : self }
        return loader.render_to_string('codegen/hub/HubLatestViewGenerator.txt', context=ctx)

class HubPITProcGenerator():

    def __init__(self, hub):
        self.hub = hub
        self.hello = 'Hello'
        self.satelites = self.hub.hubsatelite_set.all()
        

        self.schema = 'gdelt_hana'
        self.pit_proc_name = '{}_pit_populate'.format( self.hub.table_name)
        self.pit_table_name = "{}_pit".format(convert_entity_name_to_table_name(self.hub.name))
        self.pit_view_name = self.pit_table_name + '_view'
        

    def get_artifact_text(self):
        ctx  = {'gen' : self }
        return loader.render_to_string('codegen/hub/HubPITProcedure.txt', context=ctx)

    def generate_pit_view_definition(self):
        ctx  = {'gen' : self }
        return loader.render_to_string('codegen/hub/HubPITViewGenerator.txt', context=ctx)

    
class HubSateliteTableGenerator():
    def __init__(self, satelite):
        self.sat = satelite
        self.field_list = []
        self.field_list.append(self.sat.hub.get_hash_key_field())
        self.field_list.append(self.sat.get_load_time_field())
        self.field_list.append(self.sat.get_record_source_field())
        self.field_list.append(self.sat.get_diff_key_field())
        
        for f in self.sat.hubsatelitefield_set.all():
            self.field_list.append(f)



        self.primary_key_fields = []
        self.primary_key_fields.append(self.sat.hub.get_hash_key_field())
        self.primary_key_fields.append(self.sat.get_load_time_field())
        

    def get_artifact_text(self):
        ctx  = {'sat_table_generator' : self }
        #return loader.render_to_string('codegen/hub/HubSateliteTableGenerator.txt', context=ctx)
        return render_template('codegen/hub/HubSateliteTableGenerator.txt', ctx)

class HubSateliteREDTGenerator():
    def __init__(self, satelite):
        self.sat = satelite

    def get_redt_text(self):
        ctx  = {'gen' : self }
        #return loader.render_to_string('codegen/hub/HubSateliteTableGenerator.txt', context=ctx)
        return render_template('codegen/hub/HubSateliteREDTGenerator.txt', ctx)


    
class HubPITGenerator():
    def __init__(self, hub):
        self.hub = hub
        self.hub_satelites = self.hub.hubsatelite_set.all().order_by('pk')
        self.hub_satelites_to_include_in_pit = []
        self.pit_table_primary_key_field = None
        self.hub_hash_key = self.hub.get_hash_key_field()
        self.satelite_hash_key_fields = []
        self.satelite_load_time_fields = []
        self.pit_table_schema = 'gdelt_hana'
        self.pit_table_name = "{}_pit".format(convert_entity_name_to_table_name(hub.name))

        self.hub_satelites_to_include_in_pit = self.hub_satelites # Include all satelites - might change
        self.pit_table_primary_key_field = self.hub.get_pit_table_primary_key_field()
        self.snapshot_field = FieldNonPersistent.create_snapshot_time_field()

        for sat in self.hub_satelites_to_include_in_pit:
            self.satelite_hash_key_fields.append(sat.get_pit_table_hash_key_field())
            self.satelite_load_time_fields.append(sat.get_pit_table_load_time_field())
            

        
        

    def get_pit_table_definition(self):
        ctx  = {'gen' : self }
        #return loader.render_to_string('codegen/hub/HubSateliteTableGenerator.txt', context=ctx)
        return render_template('codegen/hub/HubPITGenerator_TableDefinition.txt',
                               ctx,
                               format_sql=True)
    


    
# Create your models here.
