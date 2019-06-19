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
        self.field_list_for_augmented_table = []
        self.primary_key_fields = []
        self.hub_loaders = self.stage_table.hubloader_set.all()
        self.hub_satelite_loaders = self.stage_table.hubsateliteloader_set.all()

        self.schema = stage_table.schema
        
        self.hub_load_procedure_names = []
        self.hub_satelite_load_procedure_names = []
        self.link_load_procedure_names = []
        self.link_satelite_load_procedure_names = []


        # These fields are useful in the tempate 
        self.load_date_field = FieldNonPersistent.create_load_time_field()
        self.record_source_field = FieldNonPersistent.create_record_source_field()
        self.load_time_field = FieldNonPersistent.create_load_time_field()
        self.processed_field = FieldNonPersistent.create_processed_field()

        # This hub loader object and associated field lists will be populated every time
        # a hub loader proc is generated
        self.hub_loader = None
        self.hub_key_fields = []
        self.hub_key_fields_from_stage_table = []
        self.hub_loader_proc_name = ''

        # This hub satelite loader object and associated field lists will be populated every time
        # a hub satlite loader proc is generated
        self.hub_satelite_loader = None
        self.hub_satelite_fields = []
        self.hub_satelite_fields_from_stage_table = []
        self.hub_satelite_loader_proc_name = ''


        # This link loader object and associated field lists will be populated every time
        # a link loader proc is generated
        self.link_loader = None
        self.link_fields = []
        self.link_fields_from_stage_table = []
        self.link_loader_proc_name = ''

        # This link satelite loader object and associated field lists will be populated every time
        # a link loader proc is generated
        self.link_satelite_loader = None
        self.link_satelite_fields = []
        self.link_satelite_fields_from_stage_table = []
        self.link_satelite_loader_proc_name = ''
        
        self.link_loaders = self.stage_table.linkloader_set.all()
        self.link_loaders_that_require_diff_fields = []
        

        
        for ll in self.link_loaders:
            if ll.link.create_diff_key:
                self.link_loaders_that_require_diff_fields.append(ll)

                
        self.link_satelite_loaders = self.stage_table.linksateliteloader_set.all()

        self.augmented_table_name = "{}_aug".format(
            self.stage_table.table_name)
        
        self.augmented_table_insert_proc_name = "{}_insert".format(self.augmented_table_name)

        self.combined_view_name = "{}_cv".format(
            self.stage_table.table_name) 

        self.call_all_loads_proc_name = self.stage_table.table_name + '_load_all'

        self.stage_table_fields_physical = \
            self.stage_table.stagetablefield_set.filter(usage='physical' )
        
        for f in self.stage_table.stagetablefield_set.all():
            if f.stage_table_primary_key:
                self.primary_key_fields.append(f)
                
        if len(self.primary_key_fields) == 0:
            raise CodeGenerationError("""
             Generating an augmented table for {}
             but no fields in the staging table are flagged as primary key fields.  Choose at least one field
             and flag it as a primary key field """.format( self.stage_table ) )

#        for f in self.primary_key_fields:
#            self.field_list_for_augmented_table.append(f)
        
        self.field_list_for_augmented_table.append( self.load_date_field )
        self.field_list_for_augmented_table.append(self.processed_field )
        
        for hl in self.hub_loaders:
            self.field_list_for_augmented_table.append(hl.hub.get_hash_key_field())

        for hsl in self.hub_satelite_loaders:
            if hsl.hub_satelite.create_diff_key:
                self.field_list_for_augmented_table.append(hsl.hub_satelite.get_diff_key_field())

        for ll in self.link_loaders:
            self.field_list_for_augmented_table.append(ll.link.get_hash_key_field())

        for ll in self.link_loaders_that_require_diff_fields:
            self.field_list_for_augmented_table.append(ll.link.get_diff_key_field())
            
        for lsl in self.link_satelite_loaders:
            if lsl.link_satelite.create_diff_key:
                self.field_list_for_augmented_table.append(lsl.link_satelite.get_diff_key_field())
                

                
        

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
        self.hub_key_fields = []
        self.hub_loader_proc_name = self.stage_table.table_name + '_load_' + self.hub_loader.hub.table_name
        self.hub_load_procedure_names.append(  self.hub_loader_proc_name )

        self.hub_loader.hub.hubkeyfield_set.all().order_by('pk')

        for hub_loader_field in \
            self.hub_loader.hubloaderfield_set.all().order_by('pk'):
                if hub_loader_field.purpose != 'hub key field':
                    continue

                hub_field = hub_loader_field.get_corresponding_hub_field()
                if hub_field is None:
                    raise CodeGenerationError('''Processing hub loader "{}" and while processing 
                                                 field "{}" failed to find a corresponding hub  field
                                                 either because there was not a field in the hub with 
                                                 the same name, or the hub_field_name property was not
                                                 present '''.format ( self.hub_loader, hub_loader_field ))
                self.hub_key_fields.append(hub_field)
                self.hub_key_fields_from_stage_table.append(hub_loader_field.stage_table_field)

        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_HubLoaderProc.txt', ctx, format_sql=True)

    def get_hub_satelite_loader_proc_text(self, hub_satelite_loader):
        self.hub_satelite_fields_from_stage_table = []
        self.hub_satelite_loader = hub_satelite_loader
        self.hub_satelite_fields = []
        for hub_satelite_loader_field in \
            self.hub_satelite_loader.hubsateliteloaderfield_set.all().order_by('pk'):
                sat_field = hub_satelite_loader_field.get_corresponding_hub_satelite_field()
                if sat_field is None:
                    raise CodeGenerationError('''Processing hub satelite loader "{}" and while processing 
                                                 field "{}" failed to find a corresponding hub satlite field
                                                 either because there was not a field in the satelite with 
                                                 the same name, or the satelite_field_name property was not
                                                 present '''.format ( self.hub_satelite_loader, hub_satelite_loader_field ))
                self.hub_satelite_fields.append(sat_field)
                self.hub_satelite_fields_from_stage_table.append(hub_satelite_loader_field.stage_table_field)
                
        self.hub_satelite_loader_proc_name = "{}_load_{}".format(self.stage_table.table_name,
                                                                 self.hub_satelite_loader.hub_satelite.table_name)

        self.hub_satelite_load_procedure_names.append(self.hub_satelite_loader_proc_name)
        
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_HubSateliteLoaderProc.txt', ctx, format_sql=True)


    def get_link_loader_proc_text(self, link_loader):
        self.link_fields_from_stage_table = []
        self.link_loader = link_loader
        self.link_fields = []
        for link_loader_field in \
            self.link_loader.linkloaderfield_set.all().order_by('pk'):
                link_field = link_loader_field.get_corresponding_link_field()
                if link_field is None:
                    raise CodeGenerationError('''Processing link loader "{}" and while processing 
                                                 field "{}" failed to find a corresponding link field
                                                 either because there was not a field in the link with 
                                                 the same name, or the link_field_name property was not
                                                 present '''.format ( self.link_loader, link_loader_field ))
                self.link_fields.append(link_field)
                self.link_fields_from_stage_table.append(link_loader_field.stage_table_field)
                
        self.link_loader_proc_name = "{}_load_{}".format(self.stage_table.table_name,
                                                         self.link_loader.link.table_name)
        self.link_load_procedure_names.append(self.link_loader_proc_name)
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_LinkLoaderProc.txt', ctx, format_sql=True)

    def get_link_satelite_loader_proc_text(self, link_satelite_loader):
        self.link_satelite_fields_from_stage_table = []
        self.link_satelite_loader = link_satelite_loader
        self.link_satelite_fields = []
        for link_satelite_loader_field in \
            self.link_satelite_loader.linksateliteloaderfield_set.all().order_by('pk'):
                link_satelite_field = link_satelite_loader_field.get_corresponding_link_satelite_field()
                if link_satelite_field is None:
                    raise CodeGenerationError('''Processing link satelite loader "{}" and while processing 
                                                 field "{}" failed to find a corresponding link satelite field
                                                 either because there was not a field in the satelite with 
                                                 the same name, or the link_satelite_field_name property was not
                                                 present '''.format ( self.link_satelite_loader, link_satelite_loader_field ))
                self.link_satelite_fields.append(link_satelite_field)
                self.link_satelite_fields_from_stage_table.append(link_satelite_loader_field.stage_table_field)
                
        self.link_satelite_loader_proc_name = "{}_load_{}".format( self.stage_table.table_name,
                                                                   self.link_satelite_loader.link_satelite.table_name)
        self.link_satelite_load_procedure_names.append(self.link_satelite_loader_proc_name)
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_LinkSateliteLoaderProc.txt', ctx, format_sql=True)

    def get_call_load_procedures_text(self):
        ctx  = {'gen' : self }
        return render_template('codegen/stage_table/StageTableCodeGenerator_CallLoadProcedures.txt', ctx, format_sql=False)
    
    
# Create your models here.
