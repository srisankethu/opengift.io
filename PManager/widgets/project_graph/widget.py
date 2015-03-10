# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task

def widget(request, headerValues, ar, qargs):
    current_project = headerValues['CURRENT_PROJECT']
    bPay = request.POST.get('pay', False)
    summ = int(request.POST.get('summ', 0) or 0)

    profile = request.user.get_profile()

    total = profile.account_total or 0

    projectData = {
        'allProjectPrice': total,
        'closedTasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': True, 'active': True})),
        'tasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': False, 'active': True})),
        'bPay': bPay,
        'rate': profile.getBet(current_project),
        'premiumTill': profile.premium_till or '01.04.2014' if request.user.is_staff else ''
    }

    return projectData