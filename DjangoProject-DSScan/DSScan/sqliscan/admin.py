from django.contrib import admin
from .models import SqlInjection

class SqlInjectionAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'target_url', 'scan_data', 'vulnerability', )
    list_filter = ('scan_status', 'vulnerability', )
    search_fields = ('target_url', )
    ordering = ('-vulnerability', 'task_id', )

admin.site.register(SqlInjection, SqlInjectionAdmin)
