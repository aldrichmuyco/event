from django.contrib import admin
from events.models import Event, Criteria, Judge, Participant, ParticipantRating

# class CriteriaInline(admin.TabularInline):
# 	model = Criteria

# class JudgeInline(admin.TabularInline):
# 	model = Judge

# class ParticipantInline(admin.TabularInline):
# 	model = Participant

# class EventAdmin(admin.ModelAdmin):
# 	list_display=('title','is_closed',)
# 	inlines = [CriteriaInline, JudgeInline, ParticipantInline]
# admin.site.register(Event, EventAdmin)
# admin.site.register(ParticipantRating)