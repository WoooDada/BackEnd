from django.contrib import admin
from .models import Study_analysis, Daily_1m_content, One_week_study_data, today_date


admin.site.register(Study_analysis)
admin.site.register(Daily_1m_content)
admin.site.register(One_week_study_data)
admin.site.register(today_date)