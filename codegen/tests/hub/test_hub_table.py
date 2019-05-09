from django.test import TestCase


from dventities.models import Hub, HubKeyField, HubSatelite, HubSateliteField

from codegen.hub import hub_table

        
class HubTests(TestCase):

    def test_table_creation1(self):
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

            
        ht = hub_table.HubTableGenerator(h)
        #print(ht.get_artifact_text())
        h.save()
        #print(h.name)
        self.assertEqual(1,1)

class HubSateliteTests(TestCase):

    def test_table_creation1(self):
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

        st = hub_table.HubSateliteTableGenerator(s)
        table_text = st.get_artifact_text().replace('\n', ' ').lower()
        self.assertIn( 'create table {}.{} ('.format(s.schema, s.table_name),
                       table_text)
        self.assertIn(  'alter table', table_text )
        
        #print(st.get_artifact_text())
        h.save()
        #print(h.name)
        self.assertEqual(1,1)
# Create your tests here.
