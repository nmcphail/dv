from django.db import models
from django.template import loader
from codegen.util.template_utils import render_template
from codegen.exceptions import CodeGenerationError

from dventities.models import FieldNonPersistent

from dventities.models import Link, LinkField, LinkSatelite
from dventities.models import Hub, HubKeyField, HubSatelite

from dventities.models import StageTable, StageTableField, HubLoader, HubSateliteLoader




class StageTableCodeGenerator():
    def __init__(self, stage_table):
        self.stage_table = stage_table
        self.field_list = []
        self.primary_key_fields = []
        self.hub_loaders = self.stage_table.hubloader_set.all()
        self.hub_satelite_loaders = self.stage_table.hubsateliteloader_set.all()
        self.link_loaders = self.stage_table.linkloader_set.all()
        self.link_loaders_that_require_diff_fields = []

        # This hub loader object and associated field lists will be populated every time
        # a hub loader proc is generated
        self.hub_loader = None
        self.hub_key_fields = []
        self.hub_key_fields_from_stage_table = []
        self.hub_loader_proc_name = ''

        for ll in self.link_loaders:
            if ll.link.create_diff_key:
                self.link_loaders_that_require_diff_fields.append(ll)
                
        self.link_satelite_loaders = self.stage_table.linksateliteloader_set.all()
        self.augmented_table_name = "{}.{}_aug".format(
            self.stage_table.schema,
            self.stage_table.table_name)
        
        self.augmented_table_insert_proc_name = "{}_insert".format(self.augmented_table_name)

        self.combined_view_name = "{}.{}_cv".format(
            self.stage_table.schema,
            self.stage_table.table_name) 


        self.stage_table_fields_physical = \
            self.stage_table.stagetablefield_set.filter(usage='physical' )

        self.load_date_field = FieldNonPersistent.create_load_time_field()
        self.record_source_field = FieldNonPersistent.create_record_source_field()
        self.load_time_field = FieldNonPersistent.create_load_time_field()
        self.processed_field = FieldNonPersistent.create_processed_field()
        
        
        for f in self.stage_table.stagetablefield_set.all():
            if f.stage_table_primary_key:
                self.primary_key_fields.append(f)

                
        if len(self.primary_key_fields) == 0:
            raise CodeGenerationError("""
             Generating an augmented table for {}
             but no fields in the staging table are flagged as primary key fields.  Please choose at least one field
             and flag it as a primary key field """.format( self.stage_table ) )

        for f in self.primary_key_fields:
            self.field_list.append(f)
        
        self.field_list.append( self.load_date_field )
        
        for hl in self.hub_loaders:
            #print(hl)
            self.field_list.append(hl.hub.get_hash_key_field())

        for hsl in self.hub_satelite_loaders:
            # print(hsl)
            if hsl.hub_satelite.create_diff_key:
                self.field_list.append(hsl.hub_satelite.get_diff_key_field())

        for ll in self.link_loaders:
            #print(ll)
            self.field_list.append(ll.link.get_hash_key_field())

        for ll in self.link_loaders_that_require_diff_fields:
            print(ll.link.get_diff_key_field())
            self.field_list.append(ll.link.get_diff_key_field())
            
    
        for lsl in self.link_satelite_loaders:
            #print(lsl)
            if lsl.link_satelite.create_diff_key:
                self.field_list.append(lsl.link_satelite.get_diff_key_field())
                

                
        

    def get_augmented_table_text(self):
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_AugmentedTable.txt', ctx, format_sql=True)

    def get_augmented_table_insert_proc_text(self):
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_AugmentedTableInsertProc.txt', ctx, format_sql=True)


    def get_combined_view_text(self):
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_CombinedView.txt', ctx, format_sql=True)

    def get_hub_loader_proc_text(self, hub_loader):
        self.hub_key_fields_from_stage_table = []
        self.hub_loader = hub_loader
        self.hub_key_fields = self.hub_loader.hub.hubkeyfield_set.all().order_by('pk')
        self.hub_loader_proc_name = "{}.{}_{}_loader".format(self.stage_table.schema, self.stage_table.table_name, self.hub_loader.hub.table_name)
        #print(dir(hub_loader))
        for f in hub_loader.hubloaderfield_set.all().order_by('pk'):
            if f.purpose == 'hub key field':
                self.hub_key_fields_from_stage_table.append(f.stage_table_field)

        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_HubLoaderProc.txt', ctx, format_sql=True)





    
    
# Create your models here.
