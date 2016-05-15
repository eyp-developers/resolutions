from django.contrib import admin

from .models import Session, Committee, Subtopic, Clause, ClauseContent, SubClause, SubClauseContent, FactSheet


#Setting up the inline for the resolutions for the session admin
class CommitteeInline(admin.StackedInline):
    model = Committee
    extra = 0


#Setting up the session admin
class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Session Information', {'fields': ['name', 'full_name', 'email', 'ga_start_date', 'ga_end_date']}),
        ('Session Users', {'fields': ['admin_user', 'resolution_user']})
    ]

    inlines = [CommitteeInline]

    list_display = ('name', 'email', 'ga_start_date', 'ga_end_date')

    list_filter = ['ga_start_date']


class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('session', 'name', 'number')


class SubtopicAdmin(admin.ModelAdmin):
    list_display = ('committee', 'name', 'position')


class ClauseAdmin(admin.ModelAdmin):
    list_display = ('committee', 'clause_type', 'last_edited', 'position')


class ClauseContentAdmin(admin.ModelAdmin):
    list_display = ('clause', 'content')


class SubClauseAdmin(admin.ModelAdmin):
    list_display = ('clause', 'last_edited', 'position')


class SubClauseContentAdmin(admin.ModelAdmin):
    list_display = ('subclause', 'content')


class FactSheetAdmin(admin.ModelAdmin):
    list_display = ('committee', 'content')


admin.site.register(Session, SessionAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Subtopic, SubtopicAdmin)
admin.site.register(Clause, ClauseAdmin)
admin.site.register(ClauseContent, ClauseContentAdmin)
admin.site.register(SubClause, SubClauseAdmin)
admin.site.register(SubClauseContent, SubClauseContentAdmin)
admin.site.register(FactSheet, FactSheetAdmin)
