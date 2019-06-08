from django.test import TestCase


from dventities.models import Hub, HubKeyField, HubSatelite, HubSateliteField

from codegen.hub import hub_table
from codegen.manager import manager

        
class ManagerTests(TestCase):

    def test_hub_code_gen(self):
        """
        """
        h = Hub(name='my test hub')
        h.clean()
        h.save()
        f1 = HubKeyField(field_name='f1',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        f1.clean()
        f1.hub = h
        #print(dir(h))
        f1.save()
        s = HubSatelite(name='s1')
        s.hub = h
        s.clean()
        s.save()
        sf1 = HubSateliteField(field_name = 'sf1',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        sf1.sat = s
        sf1.clean()
        sf1.save()


        sf2 = HubSateliteField(field_name = 'sf2',
                         field_precision=0,
                         field_scale=0,
                         field_type='string',
                         field_length=30)
        sf2.sat = s
        sf2.clean()
        sf2.save()

        h.save()
        #print(h.name)
        self.assertEqual(1,1)
        mm = manager.ModelManager()
        hm = manager.HubManager(h, mm.artifact_location)
        hm.generate_code()
        

