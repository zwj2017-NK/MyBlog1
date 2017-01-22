from django.contrib import admin
from .models import SqlInjection, UrlList, ScanConfig

class SqlInjectionAdmin(admin.ModelAdmin):
    list_display = ('target_url', 'task_id', 'scan_data', 'vulnerability','scan_log', )
    list_filter = ('scan_status', 'vulnerability', )
    search_fields = ('target_url', )
    ordering = ('-vulnerability', 'task_id', )

class UrlListAdmin(admin.ModelAdmin):
    list_display = ('target_urls', )

class ScanConfigAdmin(admin.ModelAdmin):
    list_display = ('thread_num', )

admin.site.register(SqlInjection, SqlInjectionAdmin)
admin.site.register(UrlList, UrlListAdmin)
admin.site.register(ScanConfig, ScanConfigAdmin)
