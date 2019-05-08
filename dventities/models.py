from django.db import models

# Create your models here.


class DVEntity(models.Model):
    name = models.CharField(max_length=200)
    #last_mod_date = models.DateTimeField('last modified date', blank=True)
    vault = models.CharField(max_length=200,
                             blank=True,
                             choices=(('Raw', 'Raw'), ('Bus', 'Business')),
                             default='raw')

    schema = models.CharField(
        max_length=200,
        blank=True,
    )
    table_name = models.CharField(max_length=200, blank=True)
    table_alias = models.CharField(max_length=200, blank=True)

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
    field_type = models.CharField(max_length=200, blank=True)
    field_precision = models.IntegerField(blank=True)
    field_scale = models.IntegerField(blank=True)
    field_desciption = models.CharField(max_length=200, blank=True)
    column_name = models.CharField(max_length=200, blank=True)

    class Meta():
        abstract = True


class Satelite(DVEntity):
    source = models.CharField(max_length=200, blank=True)
    rate_of_change = models.CharField(max_length=200, blank=True)

    class Meta():
        abstract = True


class Hub(RootEntity):
    def clean(self):
        self.schema = self.vault
        if self.root_name is None or self.root_name == '':
            self.root_name = (
                'hub' + \
                '_' + \
                self.name
            ).replace(' ', '_').lower()

        if not hasattr(self, 'hubhashfield'):
            f = HubHashField(
                field_name='Hub Hash Field',
                field_type='char',
                field_precision=1,
            )

            self.hubhashfield = f


class HubHashField(Field):
    hub = models.OneToOneField(
        Hub,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class HubKeyField(Field):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)


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


class Link(RootEntity):
    def clean(self):
        self.schema = self.vault
        if self.root_name is None or self.root_name == '':
            self.root_name = ('link' + \
                               '_' + \
                               self.name).replace(' ', '_').lower()


class LinkField(Field):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)


class LinkDifferenceField(Field):
    link = models.OneToOneField(
        Link,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class LinkHubReference(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    hub_alias = models.CharField(max_length=200, blank=True)


class LinkSatelite(Satelite):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)


class StageTable(RootEntity):
    pass

    def __str__(self):
        return "Stage Table : {}  ".format(self.name)

class StageTableField(Field):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE, related_name='foo_bar')
    usage = models.CharField(
        max_length=200,
        blank=True,
        default = 'physical',
        choices = (('physical', 'physical'),
                   ('derived', 'derived'),
                   ('augmented', 'augmented')))
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

#    def __str__(self):
#        return "Hub Loader Field  :  {}    ".format(
#            self.fie,
#            self.stage_table_field.field_name,
#            self.hub_loader,
#            )

   
class HubSateliteLoader(models.Model):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)
   
class HubSateliteLoaderField(models.Model):
    hub_satelite_loader = models.ForeignKey(HubSateliteLoader,
                                            on_delete=models.CASCADE)
    
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)

   
class LinkLoader(models.Model):
    stage_table = models.ForeignKey(StageTable, on_delete=models.CASCADE)
   
class LinkLoaderField(models.Model):
    hub_loader = models.ForeignKey(LinkLoader, on_delete=models.CASCADE)
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)
   
class LinkSateliteLoader(models.Model):
    stage_table = models.ForeignKey(StageTable,
                                    on_delete=models.CASCADE)
   
class LinkSateliteLoaderField(models.Model):
    hub_satelite_loader = models.ForeignKey(LinkSateliteLoader,
                                            on_delete=models.CASCADE)
    stage_table_field = models.ForeignKey(StageTableField,
                                          on_delete=models.CASCADE)
