# tasks/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import Task, DailyCompletion
from django.contrib.admin import display

class DailyCompletionInline(admin.TabularInline):
    model = DailyCompletion
    extra = 0
    fields = ('date', 'completed')
    readonly_fields = ('date',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_description_short', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    inlines = [DailyCompletionInline]

    @display(description='Description')
    def get_description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return ""
    get_description_short.admin_order_field = 'description'  # Allows sorting by description

@admin.register(DailyCompletion)
class DailyCompletionAdmin(admin.ModelAdmin):
    list_display = ('task', 'date', 'completed')
    list_filter = ('date', 'completed')
    search_fields = ('task__name',)
    list_editable = ('completed',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show today's completions by default
        if not request.GET:
            qs = qs.filter(date=timezone.localdate())
        return qs