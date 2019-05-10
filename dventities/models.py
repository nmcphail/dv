from django.db import models

# Create your models here.

def convert_person_readable_fieldname(fieldname):
    f = fieldname.replace(' ', '_')
    return f

class DVEntity(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='This will be the name that the Hub, Satelite, Link etc will be known as')
    #last_mod_date = models.DateTimeField('last modified date', blank=True)
    vault = models.CharField(max_length=200,
                             blank=True,
                             choices=(('Raw', 'Raw'), ('Bus', 'Business')),
                             default='raw',
                             help_text = 'Determines the vault, and hence schema this entity resides in')

    schema = models.CharField(
        max_length=200,
        blank=True,
        help_text='Can be supplied directly, otherwise, derived from the Vault field'
    )
    table_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Can be entered explicitly, but if blank will be derived from name, and table_naming rules')
    table_alias = models.CharField(
        max_length=200,
        blank=True,
        help_text="table Alias will be used when this table is used in joins, and select statements")

    def get_load_time_field(self):
        return FieldNonPersistent.create_load_time_field()

    def get_record_source_field(self):
        return FieldNonPersistent.create_record_source_field()

    def get_diff_key_field(self):
        f = FieldNonPersistent(
            field_name = self.name + 'Diff Key',     
            field_type = 'string',       
            field_precision = 0, 
            field_scale = 0,  
            field_description = 0,
            field_length = 32,
            column_name = self.table_name + '_dk'
        )
        return f
    
    def __str__(self):
        return self.name

    def clean(self):
        self.schema = self.vault
        if self.table_name is None or self.table_name == '':
            self.table_name = self.name.replace(' ', '_').lower()

        if self.table_alias is None or self.table_alias == '':
            self.table_alias = self.name.replace(' ', '_').lower()

    class Meta():
        abstract = True


class RootEntity(DVEntity):
    root_name = models.CharField(max_length=200, blank=True)

    class Meta():
        abstract = True


class Field(models.Model):
    field_name = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200,
                                  choices = (('string', 'string'),
                                             ('int', 'int'),
                                             ('float', 'float'),
                                             ('date', 'date'),
                                             ('datetime', 'datetime'), )  )
    
    field_precision = models.IntegerField(blank=True, null=True)
    field_scale = models.IntegerField(blank=True, null=True)
    field_description = models.CharField(max_length=200, blank=True, null=True)
    field_length = models.IntegerField(blank=True, null=True)
    column_name = models.CharField(max_length=200, blank=True)

    class Meta():
        abstract = True


    def clean(self):
        super().clean()
        if self.column_name is None or self.column_name == '':
            self.column_name = convert_person_readable_fieldname(self.field_name)

        if self.field_precision is None:
            self.field_precision = 0
            
        if self.field_scale is None:
            self.field_scale = 0

            
class FieldNonPersistent():

    def __init__(self,
                 field_name=None,
                 field_type = None,
                 field_precision=None,
                 field_scale = None,
                 field_description=None,
                 field_length=None,
                 column_name=None,
                 dventity = None):
    
        self.field_name = field_name     
        self.field_type = field_type      
        self.field_precision = field_precision 
        self.field_scale =    field_scale  
        self.field_description = field_description
        self.field_length = field_length
        self.column_name = column_name
        self.dventity = dventity

        if self.column_name is None or self.column_name == '':
            self.column_name = convert_person_readable_fieldname(self.field_name)

        if self.field_precision is None:
            self.field_precision = 0
            
        if self.field_scale is None:
            self.field_scale = 0

        

    def create_from_model_field(model_field):
        f = FieldNonPersistent(
            field_name = model_field.field_name,     
            field_type = model_field.field_type,      
            field_precision = model_field.field_precision, 
            field_scale = model_field.field_scale,  
            field_description = model_field.field_description,
            field_length = model_field.field_length,
            column_name = model_field.column_name
        )
        return f

    def create_load_time_field():
        f = FieldNonPersistent(
            field_name = 'Load Time',     
            field_type = 'datetime',       
            field_precision = 0, 
            field_scale = 0,  
            field_description = 0,
            field_length = None,
            column_name = 'rldt'
        )
        return f

    def create_record_source_field():
        f = FieldNonPersistent(
            field_name = 'Load Time',     
            field_type = 'datetime',       
            field_precision = 0, 
            field_scale = 0 , 
            field_description = 0,
            field_length = 4,
            column_name = 'rsrc'
        )
        return f

    
    
class Satelite(DVEntity):
    source = models.CharField(max_length=200, blank=True)
    rate_of_change = models.CharField(max_length=200, blank=True)
    create_diff_key = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        help_text = '''If Yes, this satelite will contain a difference field to look for situations where
                       this satelite should be replaced with a more recent record ''' )

    class Meta():
        abstract = True


class Hub(RootEntity):
    pass

    def clean(self):
        super().clean()
        self.schema = self.vault
        if self.root_name is None or self.root_name == '':
            self.root_name = ('hub' + \
                               '_' + \
                               self.name).replace(' ', '_').lower()

        if self.table_name is None or self.table_name == '':
            self.table_name = self.name.replace(' ', '_').lower() + '_hub'
    
    #@property        
    def get_hash_key_field(self):
        f = FieldNonPersistent(
            field_name = 'Hash Key',     
            field_type = 'string',       
            field_precision = 0, 
            field_scale = 0,  
            field_description = 0,
            field_length = 32,
            column_name = self.table_name + '_hk'
        )
        return f

            
class HubKeyField(Field):
    hub = models.ForeignKey(Hub,
                            on_delete=models.CASCADE )
    
    def __str__(self):
        return self.field_name

class HubSatelite(Satelite):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

    def clean(self):
        self.schema = self.vault
        if self.table_name is None or self.table_name == '':
            self.table_name = (self.hub.name + \
                               '_' + \
                               self.name + \
                               '_sat').replace(' ', '_').lower()

        if self.table_alias is None or self.table_alias == '':
            self.table_alias = self.name.replace(' ', '_').lower()

class HubSateliteField(Field):
    sat = models.ForeignKey(HubSatelite,
                            on_delete=models.CASCADE,
                            related_name='fields' )
    
    def __str__(self):
        return self.field_name

class Link(RootEntity):
    create_diff_key = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text = '''If True, this link will contain a difference field to look for situations where
                       this link should be end dated, or reversed                             
                                                                 ''' )

    
    def clean(self):
        super().clean()
        self.schema = self.vault
        if self.root_name is None or self.root_name == '':
            self.root_name = ('link' + \
                               '_' + \
                               self.name).replace(' ', '_').lower()
        if self.table_name is None or self.table_name == '':
            self.table_name = self.name.replace(' ', '_').lower() + '_link'

    def get_hash_key_field(self):
        f = FieldNonPersistent(
            field_name = self.name + 'Hash Key',     
            field_type = 'string',       
            field_precision = 0, 
            field_scale = 0,  
            field_description = 0,
            field_length = 32,
            column_name = self.table_name + '_hk'
        )
        return f

    

class LinkField(Field):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    
class LinkHubReference(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    hub_alias = models.CharField(max_length=200, blank=True)

    forms_part_of_driving_key = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text = '''This hub forms part of the driving key, and will trigger
                       a new link if  a record comes through with the same driving 
                       key but with a differet dif key.  the existing record will be
                       either end-dated or reversed                                                           
                                                                 ''' )
    class Meta():
        ordering = ['id']

    def get_hash_key_field_for_alias(self):
        mf = self.hub.get_hash_key_field()
        f = FieldNonPersistent.create_from_model_field(mf)
        if self.hub_alias is None or self.hub_alias == '':
            return f
            
        else:
            f.name = f.field_name + 'Hash Key'
            f.column_name = f.column_name.replace('_hk', '_{}_hk'.format(self.hub_alias))
            return f
        

class LinkSatelite(Satelite):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

class LinkSateliteField(Field):
    sat = models.ForeignKey(LinkSatelite,
                            on_delete=models.CASCADE )

    
class StageTable(RootEntity):
    def clean(self):
        super().clean()
        self.schema = self.vault
        if self.root_name is None or self.root_name == '':
            self.root_name = ('stage' + \
                               '_' + \
                               self.name).replace(' ', '_').lower()

    def __str__(self):
        return "Stage Table : {}  ".format(self.name)

class StageTableField(Field):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)
    usage = models.CharField(
        max_length=200,
        blank=True,
        default = 'physical',
        choices = (('physical', 'physical'),
                   ('derived', 'derived'),
                   ('augmented', 'augmented')))

    stage_table_primary_key = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text = '''This field represents the primary key of the stage table.  A similar primary key will
                       be created on the augmented table, and then a view will combined fields in the stage table 
                       with fields in the augmented table''' )
    

    def __str__(self):
        return "Stage Table Field : {}.{}  ".format(self.stage_table.name, self.field_name)

   
class HubLoader(models.Model):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

    def __str__(self):
        return "Hub Loader  : From Stage Table  {} to {}  ".format(self.stage_table.name, self.hub.name)

   
class HubLoaderField(models.Model):
    hub_loader = models.ForeignKey(HubLoader, on_delete=models.CASCADE)

    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True)
    purpose  = models.CharField(
        max_length=200,
        blank=True,
        default = 'hub key field',
        choices = (('hub key field', 'Hub Key Field'), ))

    hub_field_name  = models.CharField(
        max_length=200,
        blank=True,
        help_text = '''If left blank, the loader will
                       look for a hub field whose name is the same as this field.  
                       If this field is populated, then the loader will load 
                       data into the field specified here ''' )
    
    def __str__(self):
        return "Hub Loader Field  :  {} {}    ".format(
            self.stage_table_field.field_name,
            self.hub_loader,
            )

   
class HubSateliteLoader(models.Model):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)

    hub_loader = models.ForeignKey(HubLoader,
                                    on_delete=models.CASCADE)
    
class HubSateliteLoaderField(models.Model):
    hub_satelite_loader = models.ForeignKey(HubSateliteLoader,
                                            on_delete=models.CASCADE)
    
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)

    comment = models.CharField(max_length=200, blank=True)
    create_field_like_this_in_satelite = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text = '''If a field with this name does not exist in the satelite, then
                       a field will be created when this record is saved ''' )
    
    satelite_field_name= models.CharField(
        max_length=200,
        blank=True,
        help_text = '''The satelite field that will get populated by load routines ''' )

   

class LinkLoader(models.Model):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)
    hub_loaders = models.ManyToManyField(HubLoader)
   
class LinkLoaderField(models.Model):
    link_loader = models.ForeignKey(LinkLoader, on_delete=models.CASCADE)
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)
   
class LinkSateliteLoader(models.Model):
    stage_table = models.ForeignKey(StageTable,
                                    on_delete=models.CASCADE)

    link_loader = models.ForeignKey(LinkLoader, on_delete=models.CASCADE)

    
class LinkSateliteLoaderField(models.Model):
    link_satelite_loader = models.ForeignKey(LinkSateliteLoader,
                                            on_delete=models.CASCADE)
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)
