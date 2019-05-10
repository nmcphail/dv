from django.test import TestCase

from dventities.models import *
#from dventities.models import Link, LinkField, LinkSatelite, LinkSateliteField, LinkHubReference


        
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

    def test_hub_creation1(self):
        """
        """
        pass

    def test_hub_creation1(self):
        """
        """
        hub1 = Hub(name='hub1')
        hub1.clean()
        hub1.save()
        hub1.hubkeyfield_set.create(field_name='f1', field_type='string', field_length=20)
        #print(dir(hub1))
        
        hub_sat1 = HubSatelite(name='sat1')
        hub_sat1.hub = hub1
        hub_sat1.clean()
        hub_sat1.save()

        st = StageTable(name='stage table 1')
        st.clean()
        st.save()

        f1 = st.stagetablefield_set.create(field_name='f1', field_type='string', field_length=20)
        f2 = st.stagetablefield_set.create(field_name='f2', field_type='string', field_length=20)

        hl = HubLoader()
        hl.hub = hub1
        hl.stage_table = st
        hl.clean()
        hl.save()
        hlf = HubLoaderField()
        hlf.hub_loader = hl
        hlf.stage_table_field = f1
        hlf.clean()
        hlf.save()

        #print(dir(f1))
        print('Field used in hubloaders')
        for f in f1.hubloaderfield_set.all():
            print(f)
            
        print('Field used in hub satelite loaders')
        for f in f1.hubsateliteloaderfield_set.all():
            print(f)

        print('Field used in link loaders')
        for f in f1.linkloaderfield_set.all():
            print(f)

        print('Field used in link satelite loaders')
        for f in f1.linksateliteloaderfield_set.all():
            print(f)
    

        
        #print(st.stagetablefield_set.all())
        #print(st)
        pass

    print('hello')

