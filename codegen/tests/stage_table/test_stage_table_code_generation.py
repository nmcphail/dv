from django.test import TestCase

from dventities.models import Hub, HubKeyField, HubSatelite, HubSateliteField
from dventities.models import Link, LinkField, LinkSatelite, LinkSateliteField, LinkHubReference
from dventities.models import *

from codegen.exceptions import CodeGenerationError
from codegen.stage_table.stage_table_code_generation import *
#from codegen.tests.util import strip_unnecessary_whitespace_and_convert_to_lowercase

        
class StageTableTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


        cls.stage_table = StageTable(name='stage_table_1')
        cls.stage_table.clean()
        cls.stage_table.save()

        f1 = StageTableField(field_name='field1', field_type='string', field_length=20)
        f1.stage_table = cls.stage_table
        f1.clean()
        f1.save()
        
        cls.test_link = Link(name='link1', create_diff_key=True)
        cls.test_link.clean()
        cls.test_link.save()
        f1 = LinkField(field_name='link1_field1',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        f1.clean()
        f1.link = cls.test_link
        f1.save()


        
        cls.test_sat = LinkSatelite(name='link sat', create_diff_key=True)
        cls.test_sat.link = cls.test_link
        cls.test_sat.clean()
        cls.test_sat.save()

        cls.sat_field1 = LinkSateliteField(field_name='f1', field_type='string' ,field_length=20)
        cls.sat_field1.sat = cls.test_sat
        cls.sat_field1.clean()
        cls.sat_field1.save()

        cls.hub1 = Hub(name='hub1')
        cls.hub1.clean()
        cls.hub1.save()

        h1f1 = HubKeyField(field_name='hub1 key field 1', field_type='string', field_length=20)
        h1f1.hub=cls.hub1
        h1f1.clean()
        h1f1.save()

        cls.hub2 = Hub(name='hub2')
        cls.hub2.clean()
        cls.hub2.save()

        cls.hub_ref1 = LinkHubReference(hub_alias='hub1')
        cls.hub_ref1.hub = cls.hub1
        cls.hub_ref1.link = cls.test_link
        cls.hub_ref1.clean()
        cls.hub_ref1.save()


        cls.link1 = Link(name='link1', create_diff_key=True)
        cls.link1.clean()
        cls.link1.save()
        f1 = LinkField(field_name='link1_field1',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        f1.clean()
        f1.link = cls.link1
        f1.save()

        cls.link1sat1 = LinkSatelite(name='sat1', create_diff_key=True)
        cls.link1sat1.link = cls.link1
        cls.link1sat1.clean()
        cls.link1sat1.save()

        cls.link1sat1f1 = LinkSateliteField(field_name='link1_sat1_f1')
        cls.link1sat1f1.sat = cls.link1sat1
        cls.link1sat1f1.clean()
        cls.link1sat1f1.save()

    def test_augmented_table_creation1(self):
        """
        """
        #print(dir(LinkTests.test_link))
        st = StageTableTests.stage_table
        hub1 = StageTableTests.hub1
        link1 = StageTableTests.link1
        link1sat1 = StageTableTests.link1sat1
        
        hl = HubLoader(stage_table=st, hub=hub1)
        hl.clean()
        hl.save()

        stf = st.stagetablefield_set.first()
        stf.save()

        hlf = HubLoaderField(hub_loader = hl)
        hlf.stage_table_field = stf
        hlf.clean()
        hlf.save()

        hs1 = HubSatelite(name='hub sat 1', hub=hub1)
        hs1.create_diff_key = True
        hs1.clean()
        hs1.save()

        hs1f1 = HubSateliteField(field_name='hs1f1', field_type='string', field_length=20)
        hs1f1.sat = hs1
        hs1f1.clean()
        hs1f1.save()

        hsl = HubSateliteLoader(stage_table=st )
        hsl.hub=hub1
        hsl.hub_satelite=hs1
        hsl.hub_loader = hl
        hsl.clean()
        hsl.save()

        hslf = HubSateliteLoaderField(hub_satelite_loader=hsl)
        hslf.stage_table_field = stf
        hslf.clean()
        hslf.save()

        
        ll = LinkLoader(stage_table=st, link=link1)
        ll.clean()
        ll.save()
        ll.hub_loaders.add(hl)
        llf = LinkLoaderField(link_loader = ll)
        llf.stage_table_field = stf
        llf.clean()
        llf.save()

        
        lsl = LinkSateliteLoader(stage_table=st )
        lsl.link_loader = ll
        lsl.link_satelite=link1sat1
        lsl.clean()
        lsl.save()

        lslf = LinkSateliteLoaderField(link_satelite_loader=lsl)
        lslf.stage_table_field = stf
        lslf.clean()
        lslf.save()


        
        try:
           atg = StageTableCodeGenerator(StageTableTests.stage_table)
        except CodeGenerationError:
            pass
        else:
            self.fail('Expecting a code gen error to be raised due to lack of primary key')
            
        # Set a primary key indicator on the first field
        f1 = st.stagetablefield_set.first()
        f1.stage_table_primary_key = True
        f1.save()
        atg = StageTableCodeGenerator(StageTableTests.stage_table)
        
        generated_text = atg.get_augmented_table_text().replace('\n', ' ').lower().replace('  ', ' ')

        # Expecting a field name for the hub1 aliasing hub 1
        self.assertIn( 'create table', generated_text)
        self.assertIn( 'alter table {}.{}_aug'.format(st.schema, st.table_name).lower(), generated_text)
        
        generated_text = atg.get_augmented_table_insert_proc_text().lower()
        self.assertIn( 'create or replace procedure', generated_text)
        self.assertIn( 'hash_input', generated_text)
        self.assertIn( 'hub1_hub_hk', generated_text)


        try:    
            generated_text = atg.get_hub_loader_proc_text(hl).lower()
        except CodeGenerationError:
            pass
        else:
            self.fail(msg='Expected a failure becasue the stage table field was field 1 and there was no "field1" in the hub - the field in the hub is "hub1 key field 1" ')

        #hslf.satelite_field_name = 'hs1f1'
        #hslf.clean()
        #hslf.save()
        hlf = hl.hubloaderfield_set.first()
        hlf.hub_field_name = 'hub1 key field 1'
        hlf.clean()
        hlf.save()
    
        generated_text = atg.get_hub_loader_proc_text(hl).lower()
        #print(generated_text)
        self.assertIn( 'stagetablecodegenerator_hubloaderproc', generated_text)
        

        generated_text = atg.get_combined_view_text().lower()
        self.assertIn( 'stagetablecodegenerator_combinedview', generated_text)
        self.assertIn( 'create view {}'.format(atg.combined_view_name) , generated_text)
        self.assertIn( 'join {}'.format(atg.augmented_table_name) , generated_text)
        for f in atg.stage_table.stagetablefield_set.filter(usage='physical'):
            self.assertIn('st.{}'.format(f.column_name), generated_text)

        try:    
            generated_text = atg.get_hub_satelite_loader_proc_text(hsl).lower()
        except CodeGenerationError:
            pass
        else:
            self.fail(msg='Expected a failure becasue the stage table field was field 1 and there was no "field1" in the satelite')

        hslf.satelite_field_name = 'hs1f1'
        hslf.clean()
        hslf.save()

        generated_text = atg.get_hub_satelite_loader_proc_text(hsl).lower()
        
        self.assertIn( 'stagetablecodegenerator_hubsateliteloaderproc', generated_text)
        self.assertIn( 'create or replace procedure {}'.format(atg.hub_satelite_loader_proc_name) , generated_text)
        for f in atg.hub_satelite_fields_from_stage_table:
            self.assertIn(hslf.stage_table_field.field_name, generated_text)
        
        #print(generated_text)
        try:    
            generated_text = atg.get_link_loader_proc_text(ll).lower()

        except CodeGenerationError:
            pass
        else:
            self.fail(msg='Expected a failure becasue the stage table field was field 1 and there was no "field1" in the satelite')

        llf.link_field_name = 'link1_field1'
        llf.clean()
        llf.save()
        
        generated_text = atg.get_link_loader_proc_text(ll).lower()
        #print(generated_text)
        #print(atg.get_augmented_table_insert_proc_text())
        try:    
            generated_text = atg.get_link_satelite_loader_proc_text(lsl).lower()

        except CodeGenerationError:
            pass
        else:
            self.fail(msg='Expected a failure becasue the stage table field was field 1 and there was no "field1" in the satelite')
        lslf.link_satelite_field_name = 'link1_sat1_f1'
        lslf.clean()
        lslf.save()

        
        generated_text = atg.get_link_satelite_loader_proc_text(lsl).lower()
        #print(generated_text)
        
        
