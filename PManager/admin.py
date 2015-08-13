__author__ = 'Gvammer'
from django.contrib import admin
from PManager.models import Credit, Payment, Specialty, \
    LogData, Agent, PM_File_Category, PM_Milestone, \
    PM_NoticedUsers, PM_Notice, PM_Task_Status, \
    PM_User_PlanTime, PM_Files, PM_Task_Message, \
    PM_Timer, PM_Role, PM_Task, PM_ProjectRoles, \
    PM_Properties, PM_Project, PM_Tracker, PM_User, \
    PM_User_Achievement, PM_Achievement, AccessInterface, \
    PM_Reminder, PM_Project_Achievement

class UserRolesInline(admin.TabularInline):
    fieldsets = (
        (
            None,
            {
                'fields': ('user', 'project', 'role', )
            }
            ),
        )

    model = PM_ProjectRoles
    extra = 0

class CreditInline(admin.ModelAdmin):
    list_display = ['user', 'payer', 'project', 'value', 'type', 'task', 'date']
    list_filter = ['user', 'payer', 'project__name']

class UserRoles(admin.ModelAdmin):
    list_display = ['user', 'project', 'role']
    list_filter = ['user', 'project', 'role__code']

class LogDatas(admin.ModelAdmin):
    list_display = ['code', 'value', 'datetime', 'project_id', 'user']

class Timers(admin.ModelAdmin):
    list_display = ['seconds', 'user', 'dateEnd', 'task']

class PaymentsInline(admin.ModelAdmin):
    list_display = ['user', 'payer', 'project', 'value', 'date']

class Reminder(admin.ModelAdmin):
    list_display = ['user', 'task', 'date']

admin.site.register(PM_Role)
admin.site.register(PM_Task)
admin.site.register(PM_ProjectRoles, UserRoles)
admin.site.register(PM_Properties)
admin.site.register(PM_Project)
admin.site.register(PM_Tracker)
admin.site.register(PM_User)
admin.site.register(PM_Files)
admin.site.register(PM_Task_Message)
admin.site.register(PM_Timer, Timers)
admin.site.register(PM_Achievement)
admin.site.register(PM_User_Achievement)
admin.site.register(PM_Project_Achievement)
admin.site.register(PM_User_PlanTime)
admin.site.register(PM_Task_Status)
admin.site.register(PM_Notice)
admin.site.register(PM_NoticedUsers)
admin.site.register(PM_Milestone)
admin.site.register(PM_File_Category)
admin.site.register(PM_Reminder, Reminder)
admin.site.register(Agent)
admin.site.register(LogData, LogDatas)
admin.site.register(Specialty)
admin.site.register(Payment, PaymentsInline)
admin.site.register(Credit, CreditInline)
admin.site.register(AccessInterface)