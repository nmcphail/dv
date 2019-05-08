from django.contrib import admin
from django import forms

# Register your models here.


from .models import Hub, HubKeyField, HubHashField, HubSatelite
from .models import Link, LinkHubReference, LinkSatelite
from .models import StageTable, StageTableField, HubLoader, HubLoaderField


class HubKeyFieldInline(admin.TabularInline):
    model = HubKeyField
    extra = 0

    
class HubHashFieldInline(admin.TabularInline):
    model = HubHashField
    extra = 0    

class HubSateliteInline(admin.TabularInline):
    model = HubSatelite
    show_change_link = True
    extra = 0    
    
class HubAdmin(admin.ModelAdmin):
    readonly_fields = ['schema']
    inlines = [HubKeyFieldInline, HubSateliteInline, HubHashFieldInline]

    
admin.site.register(Hub, HubAdmin)
admin.site.register(HubSatelite)

admin.site.register(HubKeyField)

class LinkHubReferenceInline(admin.TabularInline):
    model = LinkHubReference
    extra = 0   

    
class LinkSateliteInline(admin.TabularInline):
    model = LinkSatelite
    show_change_link = True
    extra = 0


class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ['schema']
    inlines = [LinkHubReferenceInline, LinkSateliteInline]
    #fields = ['pub_date', 'question_text']

admin.site.register(Link, LinkAdmin)


class HubLoaderFieldForm(forms.ModelForm):
    #stage_table_field = forms.ModelChoiceField(queryset=Hub.objects.all() )
    #stage_table_field = forms.EmailField()

   
    class Meta:
        model = HubLoaderField
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        super(HubLoaderFieldForm, self).__init__(*args, **kwargs)
        #self.fields['stage_table_field'].queryset = self.instance.hub_loader.stage_table.foo_bar.all()
        #self.initial['comment'] = self.instance.hub_loader.id
       
       
class HubLoaderFieldInline(admin.TabularInline):
    model = HubLoaderField
    extra = 0
    form = HubLoaderFieldForm

    
class HubLoaderAdmin(admin.ModelAdmin):
    inlines = [HubLoaderFieldInline]

    
admin.site.register(HubLoader, HubLoaderAdmin)


class StageTableFieldInline(admin.TabularInline):
    model = StageTableField
    classes = ['collapse']
    extra = 0

class StageTableHubLoaderInline(admin.TabularInline):
    model = HubLoader
    classes = ['collapse']
    show_change_link = True
    extra = 0

class StageTableAdmin(admin.ModelAdmin):
    inlines = [StageTableFieldInline, StageTableHubLoaderInline]

   
admin.site.register(StageTable, StageTableAdmin)
