from django.db import models
from django.template import loader
from codegen.util.template_utils import render_template
from dventities.models import Link, LinkField, LinkSatelite




class LinkTableGenerator():
    def __init__(self, link):
        self.link = link
        self.field_list = []
        self.field_list.append(self.link.get_hash_key_field())
        self.field_list.append(self.link.get_load_time_field())
        self.field_list.append(self.link.get_record_source_field())

        if self.link.create_diff_key:
            self.field_list.append(self.link.get_diff_key_field())

        for hr in self.link.linkhubreference_set.all().order_by('id'):
            self.field_list.append(hr.get_hash_key_field_for_alias())
                
        
        for f in link.linkfield_set.all().order_by('id'):
            self.field_list.append(f)
        

    def get_artifact_text(self):
        ctx  = {'link_table_generator' : self }
        return render_template('codegen/link/LinkTable.txt', ctx)

class LinkSateliteTableGenerator():
    def __init__(self, satelite):
        self.sat = satelite
        self.field_list = []
        #self.field_list.append(self.sat.link.get_hash_key_field())
        self.field_list.append(self.sat.get_load_time_field())
        self.field_list.append(self.sat.get_record_source_field())

        if self.sat.create_diff_key:
            self.field_list.append(self.sat.get_diff_key_field())
        
        for f in self.sat.linksatelitefield_set.all():
            self.field_list.append(f)



        self.primary_key_fields = []
        self.primary_key_fields.append(self.sat.link.get_hash_key_field())
        self.primary_key_fields.append(self.sat.get_load_time_field())
        

    def get_artifact_text(self):
        ctx  = {'sat_table_generator' : self }
        #return loader.render_to_string('codegen/link/LinkSateliteTableGenerator.txt', context=ctx)
        return render_template('codegen/link/LinkSateliteTableGenerator.txt', ctx)
        
# Create your models here.
