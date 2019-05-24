from django.contrib import admin
from django import forms

# Register your models here.

#from admirarchy.toolbox import HierarchicalModelAdmin, AdjacencyList

from .models import Hub, HubKeyField, HubSatelite, HubSateliteField
from .models import Link, LinkHubReference, LinkSatelite
from .models import StageTable, StageTableField, HubLoader, HubLoaderField
from .models import HubSateliteLoader, HubSateliteLoaderField
from .models import LinkLoader, LinkLoaderField, LinkSateliteLoader, LinkSateliteLoaderField, LinkLoaderToHubLoader
from .models import *


class HubKeyFieldInline(admin.TabularInline):
    model = HubKeyField
    extra = 0

    
class HubSateliteInline(admin.TabularInline):
    model = HubSatelite
    show_change_link = True
    extra = 0    
    
class HubAdmin(admin.ModelAdmin):
    readonly_fields = ['schema']
    #hierarchy = AdjacencyList(None)
    inlines = [HubKeyFieldInline, HubSateliteInline]
    
admin.site.register(Hub, HubAdmin)
admin.site.register(HubKeyField)

class HubSateliteFieldInline(admin.TabularInline):
    model = HubSateliteField
    extra = 0

class HubSateliteAdmin(admin.ModelAdmin):
    #hierarchy = AdjacencyList('hub')
    inlines = [HubSateliteFieldInline]

admin.site.register(HubSatelite, HubSateliteAdmin)
admin.site.register(HubSateliteField)


class LinkHubReferenceInline(admin.TabularInline):
    model = LinkHubReference
    extra = 0   

    
class LinkSateliteInline(admin.TabularInline):
    model = LinkSatelite
    show_change_link = True
    extra = 0

class LinkFieldInline(admin.TabularInline):
    model = LinkField
    extra = 0

class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ['schema']
    inlines = [LinkHubReferenceInline, LinkSateliteInline, LinkFieldInline]
    #fields = ['pub_date', 'question_text']

admin.site.register(Link, LinkAdmin)

#
# Logic for stage table and loaders starts
#

#
# Register the HubLoader
#

class HubLoaderFieldForm(forms.ModelForm):
   
    class Meta:
        model = HubLoaderField
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(HubLoaderFieldForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None:
            self.fields['stage_table_field'].queryset = self.parent_object.stage_table.stagetablefield_set.all()
            

class HubLoaderFieldFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs
        
       
class HubLoaderFieldInline(admin.TabularInline):
    model = HubLoaderField
    extra = 0
    form = HubLoaderFieldForm
    formset = HubLoaderFieldFormSet

    
class HubLoaderAdmin(admin.ModelAdmin):
    inlines = [HubLoaderFieldInline]

    
admin.site.register(HubLoader, HubLoaderAdmin)

#
# Create forms with inlines for HubSateliteLoader
#

class HubSateliteLoaderFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class HubSateliteLoaderForm(forms.ModelForm):
   
    class Meta:
        model = HubSateliteLoader
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(HubSateliteLoaderForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None:
            self.fields['hub_loader'].queryset = self.parent_object.hubloader_set.all()

        if hasattr(self.instance, 'hub_loader'):
            self.fields['hub_satelite'].queryset = self.instance.hub_loader.hub.hubsatelite_set.all()
        else:
            self.fields['hub_satelite'].queryset = HubSatelite.objects.none()
            
       
class HubSateliteLoaderInline(admin.TabularInline):
    model = HubSateliteLoader
    extra = 0
    form = HubSateliteLoaderForm
    formset = HubSateliteLoaderFormSet
    show_change_link = True

#
# Deal with Hub Satelite Loader 
#

class HubSateliteLoaderFieldForm(forms.ModelForm):
   
    class Meta:
        model = HubSateliteLoaderField
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(HubSateliteLoaderFieldForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None:
            self.fields['stage_table_field'].queryset = self.parent_object.stage_table.stagetablefield_set.all()
            

class HubSateliteLoaderFieldFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        #print('get form kwargs', index)
        #print('self instance', self.instance)
        kwargs['parent_object'] = self.instance
        return kwargs
       
      
class HubSateliteLoaderFieldInline(admin.TabularInline):
    model = HubSateliteLoaderField
    extra = 0
    form = HubSateliteLoaderFieldForm
    formset = HubSateliteLoaderFieldFormSet

    
class HubSateliteLoaderAdmin(admin.ModelAdmin):
    form = HubSateliteLoaderForm
    inlines = [HubSateliteLoaderFieldInline]

    
admin.site.register(HubSateliteLoader, HubSateliteLoaderAdmin)


#######
#
# Register the LinkLoaderField
#

class LinkLoaderFieldFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class LinkLoaderFieldForm(forms.ModelForm):
   
    class Meta:
        model = LinkLoaderField
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(LinkLoaderFieldForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None and hasattr(self.parent_object, 'stage_table'):
            self.fields['stage_table_field'].queryset = self.parent_object.stage_table.stagetablefield_set.all()


class LinkLoaderFieldInline(admin.TabularInline):
    model = LinkLoaderField
    extra = 0
    form = LinkLoaderFieldForm
    formset = LinkLoaderFieldFormSet

#
# LinkLoaderToHubLoader
#

class LinkLoaderToHubLoaderFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class LinkLoaderToHubLoaderForm(forms.ModelForm):
   
    class Meta:
        model = LinkLoaderToHubLoader
        fields = '__all__'

    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
#        super(LinkLoaderToHubLoaderForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        
        if self.parent_object is not None and hasattr(self.parent_object, 'stage_table'):
            pass
            self.fields['hub_loader'].queryset = self.parent_object.stage_table.hubloader_set.all()
        else:
            self.fields['hub_loader'].queryset = HubLoader.objects.none()


class LinkLoaderToHubLoaderInline(admin.TabularInline):
    model = LinkLoaderToHubLoader
    extra = 0
    form = LinkLoaderToHubLoaderForm
    formset = LinkLoaderToHubLoaderFormSet




    
#
# Link Loader
#
    
class LinkLoaderFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs


class LinkLoaderForm(forms.ModelForm):
   
    class Meta:
        model = LinkLoader
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(LinkLoaderForm, self).__init__(*args, **kwargs)
        print(self.instance.stage_table_id)
        #print(dir(self.instance))
        stage_table = None
        
        print(self.fields)
        if self.parent_object is not None:
            stage_table = self.parent_object
        elif self.instance is not None and hasattr(self.instance, 'stage_table') \
             and self.instance.stage_table_id is not None :
            stage_table = self.instance.stage_table
            

        if stage_table is not None:
            pass
            #self.fields['hub_loaders'].queryset = stage_table.hubloader_set.all()
        else:
            pass
            #self.fields['hub_loaders'].queryset = HubLoader.objects.none()


    
class LinkLoaderAdmin(admin.ModelAdmin):
    form = LinkLoaderForm
    formset = LinkLoaderFormSet
    inlines = [LinkLoaderToHubLoaderInline, LinkLoaderFieldInline]

    
admin.site.register(LinkLoader, LinkLoaderAdmin)



#
# Deal with Link Satelite Loader 
#
class LinkSateliteLoaderFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class LinkSateliteLoaderForm(forms.ModelForm):
   
    class Meta:
        model = LinkSateliteLoader
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(LinkSateliteLoaderForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None:
            self.fields['link_loader'].queryset = self.parent_object.linkloader_set.all()

        if hasattr(self.instance, 'link_loader'):
            pass
            #self.fields['link_satelite'].queryset = self.instance.link_loader.link.linksatelite_set.all()
        else:
            pass
            #self.fields['link_satelite'].queryset = LinkSatelite.objects.none()
            
       
class LinkSateliteLoaderInline(admin.TabularInline):
    model = LinkSateliteLoader
    extra = 0
    form = LinkSateliteLoaderForm
    formset = LinkSateliteLoaderFormSet
    show_change_link = True

class LinkSateliteLoaderFieldForm(forms.ModelForm):
   
    class Meta:
        model = LinkSateliteLoaderField
        fields = '__all__'
       
    def __init__(self,  *args, parent_object=None,  **kwargs):
        self.parent_object = parent_object
        super(LinkSateliteLoaderFieldForm, self).__init__(*args, **kwargs)

        if self.parent_object is not None:
            self.fields['stage_table_field'].queryset = self.parent_object.stage_table.stagetablefield_set.all()
            

class LinkSateliteLoaderFieldFormSet(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        #print('get form kwargs', index)
        #print('self instance', self.instance)
        kwargs['parent_object'] = self.instance
        return kwargs
       
      
class LinkSateliteLoaderFieldInline(admin.TabularInline):
    model = LinkSateliteLoaderField
    extra = 0
    form = LinkSateliteLoaderFieldForm
    formset = LinkSateliteLoaderFieldFormSet

    
class LinkSateliteLoaderAdmin(admin.ModelAdmin):
    form = LinkSateliteLoaderForm
    inlines = [LinkSateliteLoaderFieldInline]

    
admin.site.register(LinkSateliteLoader, LinkSateliteLoaderAdmin)



#######

class StageTableFieldInline(admin.TabularInline):
    model = StageTableField
    classes = ['collapse']
    extra = 0

class StageTableHubLoaderInline(admin.TabularInline):
    model = HubLoader
    #classes = ['collapse']
    show_change_link = True
    extra = 0

class StageTableHubSateliteLoaderInline(admin.TabularInline):
    model = HubSateliteLoader
    #classes = ['collapse']
    show_change_link = True
    extra = 0

    
class StageTableLinkLoaderInline(admin.TabularInline):
    model = LinkLoader
    form = LinkLoaderForm
    formset = LinkLoaderFormSet
    #classes = ['collapse']
    show_change_link = True
    extra = 0

class StageTableAdmin(admin.ModelAdmin):
    inlines = [StageTableFieldInline,
               StageTableHubLoaderInline,
               HubSateliteLoaderInline,
               StageTableLinkLoaderInline,
               LinkSateliteLoaderInline]

   
admin.site.register(StageTable, StageTableAdmin)
