from django.contrib import admin
from django.contrib import messages
from django import forms
from accounts.models import AccountUser
from .models import Family

class ChangeFamilyHeadForm(forms.Form):
    new_head = forms.ModelChoiceField(
        queryset=AccountUser.objects.none(),
        label="Select New Family Head",
        help_text="Choose a family member to promote as the new head"
    )
    
    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)
        if family:
            # Only show members of this family
            self.fields['new_head'].queryset = family.members.all()

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_head')
    search_fields = ('name', 'family_head__phone_number')
    
    def change_family_head(self, request, queryset):
        """
        Admin action to change family head.
        Uses Django's intermediate page without custom template.
        """
        if queryset.count() != 1:
            self.message_user(
                request, 
                "Please select exactly one family.", 
                level=messages.WARNING
            )
            return
        
        family = queryset.first()
        
        if 'apply' in request.POST:
            form = ChangeFamilyHeadForm(request.POST, family=family)
            if form.is_valid():
                new_head = form.cleaned_data['new_head']
                family.handle_head_death(new_head)
                self.message_user(
                    request,
                    f"Successfully changed family head to {new_head}",
                    level=messages.SUCCESS
                )
                return None
        else:
            form = ChangeFamilyHeadForm(family=family)
        
        context = {
            'title': f'Change Family Head for {family.name}',
            'form': form,
            'family': family,
            'opts': self.model._meta,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        }
        
        return admin.helpers.action_form(
            request,
            queryset,
            form,
            'Change Family Head'
        )
    
    change_family_head.short_description = "Change Family Head (Succession)"
    
    actions = ['change_family_head']
