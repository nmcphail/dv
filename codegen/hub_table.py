from django.db import models
from django.template import loader
from django.shortcuts import get_object_or_404, render

from dventities.models import Hub





class HubTable():
    def __init__(self, hub):
        self.hub = hub

        
    def say_hello(self):
        print ( loader.render_to_string('codegen/hub_table/hub_table.txt', context=None))
        
        print('hellllllo')
        
# Create your models here.
