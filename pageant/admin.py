from django.contrib import admin
from pageant.models import Pageant, CriteriaCategory, Criteria, ParticipantGroup, PageantParticipant, Judge, PageantParticipantRating

class JudgeInline(admin.TabularInline):
    model = Judge

class Participants(admin.TabularInline):
    model = PageantParticipant

class ParticipantGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'pageant']
    inlines = [Participants, ]

class CriteriaInline(admin.TabularInline):
    model = Criteria

class CriteriaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pageant', 'weight']
    inlines = [CriteriaInline,]

class PageantAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_closed']
    inlines = [JudgeInline, ]

# Register your models here.
admin.site.register(Pageant, PageantAdmin)
admin.site.register(CriteriaCategory, CriteriaCategoryAdmin)
admin.site.register(ParticipantGroup, ParticipantGroupAdmin)
# admin.site.register(PageantParticipantRating)