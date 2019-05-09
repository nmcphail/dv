from django.test import TestCase
from codegen.hub import hub_table
from dventities.models import Hub

# Create your tests here.
class HubTests(TestCase):

    def test_table_creation1(self):
        """
        """
        h = Hub(name='hub')
        ht = hub_table.HubTable(h)
        print(ht.get_artifact_text())
        h.save()
        print(h.name)
        self.assertEqual(1,1)
        
