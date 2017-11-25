__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_User
from django.template import loader, RequestContext
from PManager.services.docker import blockchain_project_status_request, blockchain_donate_request, blockchain_token_move_request, blockchain_pay_request, blockchain_project_getbalance_request, blockchain_user_newproject_request, blockchain_user_register_request, blockchain_user_getkey_request, blockchain_user_getbalance_request

def blockchainMain(request):
    c = RequestContext(request, {})

    return HttpResponse(loader.get_template('blockchain/index.html').render(c))

def blockchainAjax(request):
    action = request.POST.get('action')
    result = ''
    if action == 'register':
        result = blockchain_user_register_request(request.user.username)
        if result.find('Error') == -1:
            res = result.split("\n\n")
            profile = request.user.get_profile()
            profile.blockchain_key = res[0]
            profile.blockchain_cert = res[1]
            profile.save()
    elif action == 'getKey':
        import re
        regex = re.compile('[^a-zA-Z0-9]')
        profile = request.user.get_profile()

        if profile.blockchain_wallet:
            result = profile.blockchain_wallet
        else:
            result = blockchain_user_getkey_request(request.user.username)

            profile.blockchain_wallet = regex.sub('', result)
            profile.save()

    elif action == 'getBalance':
        profile = request.user.get_profile()
        wallet = profile.blockchain_wallet
        result = blockchain_user_getbalance_request(request.user.username, wallet)

    elif action == 'addProject':
        # profile = request.user.get_profile()
        project = request.POST.get('pName')
        result = blockchain_user_newproject_request(request.user.username, project)

    elif action == 'pay':
        # profile = request.user.get_profile()
        wallet = request.POST.get('wallet')
        sum = request.POST.get('sum')
        result = blockchain_pay_request(request.user.username, wallet, sum)

    elif action == 'move':
        # profile = request.user.get_profile()
        project = request.POST.get('project')
        qty = request.POST.get('qty')
        wallet = request.POST.get('wallet')
        result = blockchain_token_move_request(request.user.username, project, wallet, qty)

    elif action == 'donate':
        # profile = request.user.get_profile()
        project = request.POST.get('project')
        qty = request.POST.get('qty')
        result = blockchain_donate_request(request.user.username, project, qty)

    elif action == 'getProjectVals':
        # profile = request.user.get_profile()
        project = request.POST.get('pName')
        result = blockchain_project_getbalance_request(request.user.username, project)

    elif action == 'getProjectStatus':
        # profile = request.user.get_profile()
        project = request.POST.get('pName')
        result = blockchain_project_status_request(request.user.username, project)

    return HttpResponse(result)