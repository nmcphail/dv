import os

from dventities.models import Hub, HubKeyField, HubSatelite, HubSateliteField

from codegen.hub import hub_table
from codegen.stage_table.stage_table_code_generation import *
from codegen.link.link_code_generation import *





class Manager():


    def __init__(self):
        self.drop_statements = []
        

    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write_to_file_if_file_does_not_exist(self, file_path, file_contents):
        self.ensure_dir(file_path)
        if not os.path.exists(file_path) or True:
            f = open( file_path, 'w')
            f.write(file_contents)
            f.close()
            
    def write_deployment_batch_file(self, path):
        batch_file_text = '''
set orig_dir=%cd%
echo  %orig_dir%
cd "C:\\Users\\NMcPhail\\Documents\\RhodeCode\\hana_deployment\\hana_deployment"
python deploy_all_sql_files_in_dir.py %orig_dir%  %orig_dir%\deployement_log.txt
cd %orig_dir%



'''
        batch_file_name = path + os.sep + 'deploy1.bat'
        with open( batch_file_name, 'w') as f:
            f.write(batch_file_text)




    def write_drop_statements_sql_file(self, path):
        file_text = '\n'.join(self.drop_statements)
        file_name = path + os.sep + 'a drop statements.sql'
        with open( file_name, 'w') as f:
            f.write(file_text)
            

class HubManager(Manager):
    def __init__(self,hub, artifact_location):
        self.hub = hub
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.hub.root_name

    def generate_table(self):
        file_prefix = 'aaa t '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub.table_name + '.sql'
        file_contents = hub_table.HubTableGenerator(self.hub).get_artifact_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
  
    def generate_default_pit_table(self):
        file_prefix = 'ppp t'
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub.table_name + '_pit.sql'
        file_contents = hub_table.HubPITGenerator(self.hub).get_pit_table_definition()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
        
    def generate_code(self):
        self.generate_table()
        for s in self.hub.hubsatelite_set.all():
            sm = HubSateliteManager(s, self.artifact_location)
            sm.generate_code()
        self.generate_default_pit_table()
        self.write_deployment_batch_file(self.root_dir)

class LinkManager(Manager):
    def __init__(self,link, artifact_location):
        self.link = link
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.link.root_name

    def generate_table(self):
        file_prefix = 'aaa t '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.link.table_name + '.sql'
        file_contents = LinkTableGenerator(self.link).get_artifact_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
  
        
    def generate_code(self):
        self.generate_table()
#        for s in self.hub.hubsatelite_set.all():
#            sm = HubSateliteManager(s, self.artifact_location)
#            sm.generate_code()
        self.write_deployment_batch_file(self.root_dir)
            
        
class HubSateliteManager(Manager):
    def __init__(self,hub_satelite, artifact_location):
        self.hub_satelite = hub_satelite
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.hub_satelite.hub.root_name

    def generate_table(self):
        file_prefix = 'aas t'
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub_satelite.table_name + '.sql'
        file_contents = hub_table.HubSateliteTableGenerator(self.hub_satelite).get_artifact_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_redt_view(self):
        file_prefix = 'aas v'
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub_satelite.table_name + '_redt.sql'
        file_contents = hub_table.HubSateliteREDTGenerator(self.hub_satelite).get_redt_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
        
    def generate_code(self):
        self.generate_table()
        self.generate_redt_view()


class ModelManager():

    def __init__(self):
        self.hubs = Hub.objects.all()
        self.artifact_location = 'c:\\users\\nmcphail\\Documents\\codegenstuff\\'
        super().__init__()
        

    def generate_code_for_all_hubs(self):
        pass
        
            
class StageTableManager(Manager):
    def __init__(self,stage_table, artifact_location):
        self.stage_table = stage_table
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.stage_table.root_name
        self.code_generator = StageTableCodeGenerator(self.stage_table)
        self.drop_statements = []
 
    def generate_augmented_table(self):
        file_prefix = 'aaa t '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.augmented_table_name + '.sql'
        file_contents = self.code_generator.get_augmented_table_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_combined_view(self):
        file_prefix = 'aaa v '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.combined_view_name + '.sql'
        file_contents = self.code_generator.get_combined_view_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_augmented_table_insert_proc(self):
        file_prefix = 'aaaap '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.augmented_table_insert_proc_name + '.sql'
        file_contents = self.code_generator.get_augmented_table_insert_proc_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_hub_loader_proc(self, hub_loader):
        file_prefix = 'aahhp '
        file_contents = self.code_generator.get_hub_loader_proc_text(hub_loader)
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.hub_loader_proc_name + '.sql'
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_hub_satelite_loader_proc(self, hub_satelite_loader):
        file_prefix = 'aahsp '
        file_contents = self.code_generator.get_hub_satelite_loader_proc_text(hub_satelite_loader)
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.hub_satelite_loader_proc_name + '.sql'
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
        
    def generate_link_loader_proc(self, link_loader):
        file_prefix = 'aallp '
        file_contents = self.code_generator.get_link_loader_proc_text(link_loader)
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.link_loader_proc_name + '.sql'
        print('Link Loader', link_loader,  self.code_generator.link_loader_proc_name )
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)

    def generate_all_load_proc(self):
        file_prefix = 'bbbbp '
        file_contents = self.code_generator.get_call_load_procedures_text()
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.code_generator.call_all_loads_proc_name + '.sql'
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)


    def generate_code(self):
        self.generate_augmented_table()

        self.generate_augmented_table_insert_proc()
        
        self.generate_combined_view()
        
        for hl in self.stage_table.hubloader_set.all():
            self.generate_hub_loader_proc(hl)

            for sl in hl.hubsateliteloader_set.all():
                self.generate_hub_satelite_loader_proc(sl)

        for ll in self.stage_table.linkloader_set.all():
            self.generate_link_loader_proc(ll)

        self.generate_all_load_proc()
        
        # Generate all drop statements
        
        self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, self.code_generator.augmented_table_insert_proc_name))
        self.drop_statements.insert(0, 'drop view {}.{};'.format( self.code_generator.schema, self.code_generator.combined_view_name))
        self.drop_statements.insert(0, 'drop table {}.{};'.format( self.code_generator.schema, self.code_generator.augmented_table_name))

        self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, self.code_generator.call_all_loads_proc_name))

        for ds in self.code_generator.hub_load_procedure_names:
            self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, ds))

        for ds in self.code_generator.hub_satelite_load_procedure_names:
            self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, ds))

        for ds in self.code_generator.link_load_procedure_names:
            self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, ds))
            
        for ds in self.code_generator.link_satelite_load_procedure_names:
            self.drop_statements.insert(0, 'drop procedure {}.{};'.format( self.code_generator.schema, ds))

            
        self.write_deployment_batch_file(self.root_dir)
        self.write_drop_statements_sql_file(self.root_dir)
        
