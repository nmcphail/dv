from dventities.models import Hub, HubKeyField, HubSatelite, HubSateliteField

from codegen.hub import hub_table
import os



class Manager():

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
            


class HubManager(Manager):
    def __init__(self,hub, artifact_location):
        self.hub = hub
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.hub.root_name

    def generate_table(self):
        file_prefix = 'aaa '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub.table_name + '.sql'
        file_contents = hub_table.HubTableGenerator(self.hub).get_artifact_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
  
    def generate_default_pit_table(self):
        file_prefix = 'aaaaa '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub.table_name + '_pit.sql'
        file_contents = hub_table.HubPITGenerator(self.hub).get_pit_table_definition()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
        
    def generate_code(self):
        self.generate_table()
        for s in self.hub.hubsatelite_set.all():
            sm = HubSateliteManager(s, self.artifact_location)
            sm.generate_code()
        self.generate_default_pit_table()    

            
        
class HubSateliteManager(Manager):
    def __init__(self,hub_satelite, artifact_location):
        self.hub_satelite = hub_satelite
        self.artifact_location = artifact_location
        self.root_dir = self.artifact_location + os.sep + self.hub_satelite.hub.root_name

    def generate_table(self):
        file_prefix = 'aaaa '
        file_path = self.root_dir + os.sep + file_prefix + ' ' + self.hub_satelite.table_name + '.sql'
        file_contents = hub_table.HubSateliteTableGenerator(self.hub_satelite).get_artifact_text()
        self.write_to_file_if_file_does_not_exist(file_path, file_contents)
        
    def generate_code(self):
        self.generate_table()    


class ModelManager():

    def __init__(self):
        self.hubs = Hub.objects.all()
        self.artifact_location = 'c:\\users\\nmcphail\\Documents\\codegenstuff\\'
        

    def generate_code_for_all_hubs(self):
        pass
        
            
        
        
