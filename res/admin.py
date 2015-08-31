from django.contrib import admin

from .models import Session, Resolution, Clause, ClauseContent, Person, FactSheet

#Setting up the inline for the resolutions for the session admin
class ResolutionInline(admin.StackedInline):
    model = Resolution
    extra = 2

class PersonInline(admin.StackedInline):
    model = Person
    extra = 2

#Setting up the session admin
class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Session Information', {'fields': ['name', 'description', 'email', 'ga_start_date', 'ga_end_date', 'country']}),
        ('Session Users', {'fields': ['admin_user', 'resolution_user']})
    ]

    inlines = [ResolutionInline]

    list_display = ('name', 'email', 'ga_start_date', 'ga_end_date', 'country')

    list_filter = ['ga_start_date']

class ResolutionAdmin(admin.ModelAdmin):
    inlines = [PersonInline]

    list_display = ('session', 'name', 'number')

class ClauseAdmin(admin.ModelAdmin):
    list_display = ('session', 'resolution', 'clause_type', 'edited_last', 'position')

class ClauseContentAdmin(admin.ModelAdmin):
    list_display = ('session', 'resolution', 'clause', 'create_time')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('session', 'resolution', 'country', 'role', 'name')

class FactSheetAdmin(admin.ModelAdmin):
    list_display = ('session', 'resolution')

admin.site.register(Session, SessionAdmin)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(Clause, ClauseAdmin)
admin.site.register(ClauseContent, ClauseContentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(FactSheet, FactSheetAdmin)
