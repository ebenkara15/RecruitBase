from django.contrib import admin
from .models import Profile, Firm, AppUser

#############################################################
# Defining proper and covenient models to be set in 
# adminstration site in order to filter and search on fields
#############################################################

class AppUserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identité',    {'fields': ['username', 'email', 'first_name', 'last_name']}),
        ('Status',      {'fields': ['is_active', 'is_profile', 'is_firm', 'is_staff']}),
    ]

    list_display = ('username', 'email', 'is_active', 'is_profile', 'is_firm', 'is_staff')
    list_filter = ('is_active', 'is_profile', 'is_firm', 'is_staff')
    search_fields = ('username', 'email')


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identité',        {'fields': ['user', 'first_name', 'last_name', 'email_profile', 'date_of_birth' ]}),
        ('Professionnel',   {'fields': ['profile_domain', 'is_available', 'profile_text', 'cv_file']}),
    ]

    list_display = ('email_profile', 'first_name', 'last_name', 'is_available', 'profile_domain')
    list_filter = ('is_available',)
    search_fields = ('email_profile', 'first_name', 'last_name', 'profile_domain')


class FirmAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identité',    {'fields': ['user', 'email_firm', 'firm_name']}),
        ('Domain',      {'fields': ['firm_domain']}),
    ]

    list_display = ('firm_name', 'email_firm', 'firm_domain')
    list_filter = ('firm_name', 'firm_domain')
    search_fields = ('firm_name', 'firm_domain')




#############################################################
# Registring models in admin site and customize interface
#############################################################

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Firm, FirmAdmin)

admin.site.site_header = 'Administration de la CVthèque'
admin.site.site_title = 'CVtq | Admin'
admin.site.index_title = "Application en cours d'utilisation"