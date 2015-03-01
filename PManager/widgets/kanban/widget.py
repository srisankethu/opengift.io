# -*- coding:utf-8 -*-
__author__ = 'Tonakai'

from django.http import Http404
from django.template.loader_tags import register
from PManager.models.users import PM_User, PM_ProjectRoles, PM_Role
from PManager.models.tasks import PM_Project, PM_Task, PM_Task_Status
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.widgets.tasklist.widget import get_task_tag_rel_array, get_user_tag_sums
import datetime


@register.simple_tag()
def multiply(position, width, *args, **kwargs):
    return position * width


@register.inclusion_tag('kanban/templates/task.html')
def show_micro_task(task):
    return {
        'id': task.id,
        'name': task.name,
        'status': task.status.code,
        'executor': task.resp.get_profile().avatar_rel if task.resp else '',
        'executor_id': task.resp.id if task.resp else '',
        'deadline': task.deadline
    }

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    user = request.user
    current_project = headerValues['CURRENT_PROJECT'] if headerValues['CURRENT_PROJECT'] else None

    statuses = PM_Task_Status.objects.all().order_by('-id')
    tasks = PM_Task.getForUser(user, current_project, {'closed': False , 'onPlanning': False, 'status__in': statuses})
    projects_data = {}
    recommended_user = None
    for task in tasks['tasks']:
        idx = str(task.project.id)
        if idx not in projects_data:
            print 'not have attribute'
            projects_data[idx] = {
                'project': task.project,
                'date_init': task.project.dateCreate,
                'user_source': task.project.getUsers(),
                'tasks': []
            }
        recommended_user, tags = get_user_tag_sums(get_task_tag_rel_array(task), recommended_user)
        task_data = {'task': task, 'responsibleList': tags}
        projects_data[idx]['tasks'].append(task_data)
    prd_array = []
    for pd in projects_data:
        prd_array.append(projects_data[pd])
    widget_manager = TaskWidgetManager()
    users = widget_manager.getResponsibleList(request.user, headerValues['CURRENT_PROJECT'])
    return {
        'projects_data': prd_array,
        'statuses': statuses,
        'status_width': 100 / statuses.count() if statuses.count() != 0 else 100,
        'status_width_remains': 100 % statuses.count() if statuses.count() != 0 else 0,
        'users': users
    }