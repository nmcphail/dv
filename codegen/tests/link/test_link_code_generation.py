from django.test import TestCase

from dventities.models import Hub
from dventities.models import Link, LinkField, LinkSatelite, LinkSateliteField, LinkHubReference

from codegen.link.link_code_generation import *
#from codegen.tests.util import strip_unnecessary_whitespace_and_convert_to_lowercase

        
class LinkTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_link = Link(name='my test link', create_diff_key=True)
        cls.test_link.clean()
        cls.test_link.save()
        f1 = LinkField(field_name='f1',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        f1.clean()
        f1.link = LinkTests.test_link
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

        cls.hub2 = Hub(name='hub2')
        cls.hub2.clean()
        cls.hub2.save()

        cls.hub_ref1 = LinkHubReference(hub_alias='hub1')
        cls.hub_ref1.hub = cls.hub1
        cls.hub_ref1.link = cls.test_link
        cls.hub_ref1.clean()
        cls.hub_ref1.save()

    def test_table_creation1(self):
        """
        """
        #print(dir(LinkTests.test_link))
        ltg = LinkTableGenerator(LinkTests.test_link)
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower() 
        #print(generated_text)
        # Check for the presence of a diff key 
        self.assertIn(LinkTests.test_link.table_name + '_dk', generated_text)

        # check for the presence of create table
        self.assertIn('create table {}.{} ('.format(LinkTests.test_link.schema,
                                                    LinkTests.test_link.table_name), generated_text)

        # check for the presence of a primary key constraint  
        self.assertIn('alter table  {}.{}    add  constraint'.format(LinkTests.test_link.schema,
                                                    LinkTests.test_link.table_name), generated_text)

        # Now flag the link as not needing a diff key field
        LinkTests.test_link.create_diff_key = False
        ltg = LinkTableGenerator(LinkTests.test_link)
        # print(ltg.get_artifact_text())
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower()
        # Check that there is no diff key field in the table definition
        self.assertNotIn(LinkTests.test_link.table_name + '_dk', generated_text)


        hub_ref_with_alias = LinkHubReference(hub_alias='hub2')
        hub_ref_with_alias.hub = LinkTests.hub1
        hub_ref_with_alias.link = LinkTests.test_link
        hub_ref_with_alias.clean()
        hub_ref_with_alias.save()

        hub_ref_with_alias = LinkHubReference(hub_alias='hub2')
        hub_ref_with_alias.hub = LinkTests.hub1
        hub_ref_with_alias.link = LinkTests.test_link
        hub_ref_with_alias.clean()
        hub_ref_with_alias.save()
        

        ltg = LinkTableGenerator(LinkTests.test_link)
        #print(ltg.get_artifact_text())
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower()

    def test_table_creation_with_multiple_hub_refs(self):
        """
        """
        #print(dir(LinkTests.test_link))
        ltg = LinkTableGenerator(LinkTests.test_link)
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower() 

        hub_ref1 = LinkHubReference(hub_alias='hub1')
        hub_ref1.hub = LinkTests.hub1
        hub_ref1.link = LinkTests.test_link
        hub_ref1.clean()
        hub_ref1.save()

        hub_ref2 = LinkHubReference(hub_alias='hub2')
        hub_ref2.hub = LinkTests.hub2
        hub_ref2.link = LinkTests.test_link
        hub_ref2.clean()
        hub_ref2.save()
        
        hub_ref3 = LinkHubReference(hub_alias='hub2')
        hub_ref3.hub = LinkTests.hub1
        hub_ref3.link = LinkTests.test_link
        hub_ref3.clean()
        hub_ref3.save()

        hub_ref4 = LinkHubReference()
        hub_ref4.hub = LinkTests.hub1
        hub_ref4.link = LinkTests.test_link
        hub_ref4.clean()
        hub_ref4.save()

        ltg = LinkTableGenerator(LinkTests.test_link)
        #print(ltg.get_artifact_text())
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower()

        self.assertIn('hub1_hub1_hk', generated_text)
        self.assertIn('hub2_hub2_hk', generated_text)
        self.assertIn('hub1_hub2_hk', generated_text)
        self.assertIn('hub1_hk', generated_text)
        
        
    def test_table_creation_link_satelite(self):
        """
        """
        #print(dir(LinkTests.test_sat))
        ltg = LinkSateliteTableGenerator(LinkTests.test_sat)
        generated_text = ltg.get_artifact_text().replace('\n', ' ').lower()
        #print(ltg.get_artifact_text())
        #print(generated_text)
        #print(LinkTests.test_sat.table_name)
        
        # Check for the presence of a diff key 
        self.assertIn(LinkTests.test_sat.table_name+'_dk', generated_text)

        # check for the presence of create table
        self.assertIn('create table {}.{} ('.format(LinkTests.test_sat.schema,
                                                    LinkTests.test_sat.table_name), generated_text)

        # check for the presence of a primary key constraint  
        self.assertIn('alter table  {}.{}    add  constraint'.format(LinkTests.test_sat.schema,
                                                    LinkTests.test_sat.table_name), generated_text)

