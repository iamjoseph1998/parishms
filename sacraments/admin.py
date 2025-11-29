from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import SacramentType, MemberSacrament

@admin.register(SacramentType)
class SacramentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(MemberSacrament)
class MemberSacramentAdmin(SimpleHistoryAdmin):
    list_display = ('member', 'sacrament_type', 'sacrament_date')
    list_filter = ('sacrament_type', 'sacrament_date')
    search_fields = ('member__phone_number',)
    history_list_display = ['sacrament_date', 'notes']
    
    def has_change_permission(self, request, obj=None):
        """
        Allow editing if user is in 'Sacrament Editors' group or is superuser/staff.
        """
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Check if user is in Sacrament Editors group
        return request.user.groups.filter(name='Sacrament Editors').exists()
    
    def has_add_permission(self, request):
        """Same permission logic for adding"""
        return self.has_change_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Same permission logic for deleting"""
        return self.has_change_permission(request)
