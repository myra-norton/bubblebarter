from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q
from .models import Item, Proposal, Report
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.http import JsonResponse
from cloudinary import api
from django.contrib.auth.decorators import login_required, user_passes_test
from django_cas_ng import views as cas_views
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect


import uuid
# Create your views here.
def welcome(request):
    return HttpResponse('<h1>Welcome to Barter in the Bubble<h1>')

def cas_required(function=None):
    """
    Decorator that requires the user to be authenticated with CAS.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                login_url = reverse('cas_ng_login')
                next_url = request.get_full_path()
                redirect_url = f'{login_url}?next={next_url}'
                return redirect(redirect_url)
        return wrapper
    if function:
        return decorator(function)
    return decorator

def cas_login(request):
    """
    View that redirects the user to the CAS login page.
    """
    return cas_views.login(request, next=reverse('home'))

# Generate home search page
@cas_required
def index(request):
    query = request.GET.get('q')
    if not query:
        query = ''
    category_filter = Q()
    selected_categories = request.GET.get('categories')
    if not selected_categories:
        orig_cats = ''
        selected_categories = []
    else:
        orig_cats = str(selected_categories)
        selected_categories = selected_categories.split(',')
        selected_categories = [x.lower()+'_tag' for x in selected_categories]
    for category in selected_categories:
        category_filter |= Q(**{category: True})
    if not selected_categories:
        results = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    active_filter = Q(isactive=True)
    results = Item.objects.filter((Q(title__icontains=query) | Q(description__icontains=query)) & category_filter & active_filter)
    authenticated = request.user.is_authenticated
    results = list(results)
    results = sorted(results, key=lambda x: x.dateposted, reverse=True)
    owned_items = Item.objects.filter(owner = request.user.username, isactive = True)
    selected_no_dups = list(set(orig_cats.split(',')))
    selected_no_dups= ', '.join(str(i) for i in selected_no_dups)

    tags = ['Art', 'Food', 'Clothing', 'Transport','Fun', 'Weird', 'Event', 'Ticket', 'Misc', 'Free', 'Room', 'Help']
    context = {'search_results': results, 'authenticated': authenticated,'user': request.user, 'categories': tags,
               'prev_search': query, 'selected_categories': orig_cats, 'owned_items': owned_items,  'sel_no_dups':selected_no_dups}
    response = render(request, 'index.html', context)
    response.set_cookie('prev_inspect_url', request.get_full_path())
    return response

def get_results(request):
    query = request.GET.get('search_term')
    print(query)
    if not query:
        query = ''
    category_filter = Q()
    selected_categories = request.GET.get('categories')
    print(selected_categories)
    if not selected_categories:
        selected_categories = []
    else:
        selected_categories = selected_categories.split(',')
        selected_categories = [x.lower()+'_tag' for x in selected_categories]
    for category in selected_categories:
        category_filter |= Q(**{category: True})
    if not selected_categories:
        results = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results = Item.objects.filter((Q(title__icontains=query) | Q(description__icontains=query)) & category_filter)
    authenticated = request.user.is_authenticated
    tags = ['Art', 'Food', 'Clothing', 'Transport','Fun', 'Weird', 'Event', 'Ticket', 'Misc', 'Free', 'Room', 'Help']
    context = {'search_results': results, 'categories': tags}
    response = HttpResponse(render(request, 'searchresults.html', context))
    response.set_cookie('prev_search', query)
    return response

@cas_required
def account(request):
    if request.user.is_authenticated:
        username = request.user.username
        authenticated = request.user.is_authenticated
    else:
        #request = HttpResponse("User is not authenticated.")
        #return render(request, "account.html")
        username = 'test_user'
    # Get list of user's items
    items = Item.objects.filter(owner = username)
    items = list(items)
    items.sort(key=lambda x: x.dateposted, reverse=True)
    items = sorted(items, key=lambda item: (not item.isactive, -item.dateposted.timestamp()))
    proposals = Proposal.objects.filter(proposedto = username, status = 'Pending')
    incoming_proposals = []
    for proposal in proposals:
        owned_item = Item.objects.get(itemid = proposal.itemid)
        trade_item = Item.objects.get(itemid = proposal.itembid)
        incoming_proposals.append({'proposal': proposal, 'owned_item': owned_item, 'trade_item': trade_item, 'status': proposal.status})
    incoming_proposals.sort(key=lambda x: x['proposal'].dateoffered, reverse=True)
    # Get list of outgoing active proposals
    outgoing_proposals = Proposal.objects.filter(proposer = username, status = 'Pending')
    # Get info for outgoing proposals
    outgoing_proposals_info = []
    for proposal in outgoing_proposals:
        owned_item = Item.objects.get(itemid = proposal.itemid)
        trade_item = Item.objects.get(itemid = proposal.itembid)
        outgoing_proposals_info.append({'proposal': proposal, 'owned_item': owned_item, 'trade_item': trade_item, 'status': proposal.status})
    outgoing_proposals_info.sort(key=lambda x:  x['proposal'].dateoffered, reverse=True)
    # Get list of past proposals
    past_props = Proposal.objects.filter(~Q(status ='Pending') & (Q(proposedto=username) | Q(proposer=username)))
    # Get info for past proposals
    proposal_history = []
    for proposal in past_props:
        if username == proposal.proposer:
            owned_item = Item.objects.get(itemid = proposal.itemid)
            trade_item = Item.objects.get(itemid = proposal.itembid)
        else:
            owned_item = Item.objects.get(itemid = proposal.itembid)
            trade_item = Item.objects.get(itemid = proposal.itemid)
        proposal_history.append({'proposal': proposal, 'owned_item': owned_item, 'trade_item': trade_item, 'status': proposal.status})
    proposal_history.sort(key=lambda x:  x['proposal'].dateupdated, reverse=True)
    tags = ['Art', 'Food', 'Clothing', 'Transport','Fun', 'Weird', 'Event', 'Ticket', 'Misc', 'Free', 'Room', 'Help']
    accountdetails = {'user':  request.user, 'proposals': proposals, 'proposal_history': proposal_history, 'outgoing_proposals': outgoing_proposals_info,
                      'incoming_proposals': incoming_proposals, 'authenticated': authenticated, 'items': items, 'categories': tags}
    response = render(request, "account.html", accountdetails)
    response.set_cookie('prev_inspect_url', request.get_full_path())
    return response

@cas_required
def inspectitem(request):
    itemid = request.GET.get('itemid')
    # still need to check if uuid
    if not itemid or not Item.objects.filter(itemid = itemid).exists():
        return HttpResponse("Item does not exist.")
    item = Item.objects.get(itemid = itemid)
    if request.user.username:
        netid = request.user.username
    else:
        netid = 'test_user'
    if item.owner == netid:
        can_edit = True
    else:
        can_edit = False
    if item.image_url:
        resized_image_url = cloudinary.CloudinaryImage(item.image_url).build_url(transformation=[    {'width': '50%'}])
        has_image = True
    else:
        has_image = False
        resized_image_url = ''
    owned_items = Item.objects.filter(owner = netid, isactive = True)
    tags = ['Art', 'Food', 'Clothing', 'Transport','Fun', 'Weird', 'Event', 'Ticket', 'Misc', 'Free', 'Room', 'Help']
    active_tags = item.get_active_tags()
    itemdetails = {'item':item, 'image_url':resized_image_url, 'is_owner': can_edit,'has_image':has_image, 
                   'owned_items': owned_items, 'categories':tags, 'active_categories':active_tags, 'last_url': request.COOKIES.get('prev_inspect_url')}
    return render(request, "inspectitem.html", itemdetails)

def areusure(request):
    return render(request, "message-areusure.html")

# When user clicks post item, saves the item info to the database and
# Redirect to confirmation page
@cas_required
def itemposted(request: WSGIRequest):
    title = request.POST.get('title')
    description = request.POST.get('description')
    wants = request.POST.get('wants')
    if request.user.username:
        netid = request.user.username
    else:
        netid = 'test_user' # temp netid before cas approval
    item = Item(title=title, description=description, wants=wants, itemid = str(uuid.uuid4()), owner = netid)
    # Tag data
    if request.POST.get('fun'):
        item.fun_tag = True
    if request.POST.get('weird'):
        item.weird_tag = True
    if request.POST.get('event'):
        item.event_tag = True
    if request.POST.get('ticket'):
        item.ticket_tag = True
    if request.POST.get('misc'):
        item.misc_tag = True
    if request.POST.get('free'):
        item.free_tag = True
    if request.POST.get('room'):
        item.room_tag = True
    if request.POST.get('help'):
        item.help_tag = True
    if request.POST.get('art'):
        item.art_tag = True
    if request.POST.get('food'):
        item.food_tag = True
    if request.POST.get('clothing'):
        item.clothing_tag = True
    if request.POST.get('transport'):
        item.transport_tag = True

    if request.FILES:
        image_file = request.FILES['myPhoto']
        result = cloudinary.uploader.upload(image_file, folder="bbapp_images")
        item.image_url = result['url']
        item.image_public_id = result['public_id']
    #print('art: ', item.art_tag, 'food: ', item.food_tag, 'clothing: ', item.clothing_tag, 'transport: ', item.transport_tag, 'fun: ', item.fun_tag, 'weird: ', item.weird_tag, 'event: ', item.event_tag, 'ticket: ', item.ticket_tag, 'misc: ', item.misc_tag, 'free: ', item.free_tag, 'room: ', item.room_tag, 'help: ', item.help_tag)
    item.save()
    return redirect('index')#render(request, "message-itemposted.html") #maybe instead we should redirect to its item page

@cas_required
def itemreported(request: WSGIRequest):
    print(request.POST);
    if request.user.username:
        netid = request.user.username
    else:
        netid = 'test_user' # temp netid before cas approval
    reporteduser = request.POST.get('reporteduser')
    reporteditemid = request.POST.get('reporteditemid')
    reportedproposalid = request.POST.get('reportedproposalid')
    reporttext = request.POST.get('reporttext')
    reportid = str(uuid.uuid4())
    # print(reporteduser, reporteditemid, reportedproposalid, reporttext, reportid)
    report = Report(
        reportid = reportid,
        reporter = netid,
        reporteduser = reporteduser,
        reporteditemid = reporteditemid,
        reportedproposalid = reportedproposalid,
        reporttext = reporttext
    )
    report.save()
    return redirect('index') #render(request, "message-itemreported.html")

@cas_required
def processproposal(request, itemid):
    print('here')
    to_item = request.POST.get('chosen-item')
    message = request.POST.get('message')
    proposal = Proposal(proposaltext = message, status = 'Pending', itembid = itemid,
                        itemid = to_item, proposalid = str(uuid.uuid4()))
    from_item = Item.objects.get(itemid = proposal.itemid)
    to_item = Item.objects.get(itemid = proposal.itembid)
    proposal.proposer = from_item.owner
    proposal.proposedto = Item.objects.get(itemid = itemid).owner
    proposal.save()
    proposer = User.objects.get(username = proposal.proposer)
    proposedto = User.objects.get(username = proposal.proposedto)
    response_data = {
        'success': True,
        'message': 'Proposal sent successfully',
        'current_item_url': '/current-item',
        'home_page_url': '/',
    }
    if request.method == 'POST' and request.user.is_authenticated:
        subject = f"New proposal on {to_item.title}"
        message = f'''
                    Hi {proposedto.email},
                    
                    You have a new proposal on {to_item.title}, you are being offered:
                    {from_item.itemid}

                    Proposer {proposer.email} said:
                    
                    {proposal.proposaltext}

                    Accept or reject this proposal at https://bubblebarter.herokuapp.com/account/.
                    
                    This is a cos333 project, email lshannon@princeton.edu for help.'''
        html_message = f'''
                        <html>
                            <body style="font-family: Arial, sans-serif; font-size: 14px;">
                                <p>Hi {proposedto.email},</p><br>
                                <p>You have a new proposal on {to_item.title}, you are being offered:</p>
                                <p>{from_item.title}</p>
                                <p>Proposer {proposer.email} said:</p>
                                <p>{proposal.proposaltext}</p>
                                <p>Accept or reject this proposal on <a href="https://bubblebarter.herokuapp.com/account/">your account page.</a></p>
                                <br>
                                <br>
                                <p>*This is a cos333 project, email <a href="mailto:lshannon@princeton.edu">luke</a> for help.</p>
                            </body>
                        </html>
                    '''
        recipient_list = [proposedto.email]
        msg = EmailMultiAlternatives(subject, message, 'bubblebarter@gmail.com', recipient_list)
        msg.attach_alternative(html_message, "text/html")

        if msg.send(fail_silently=False):
            print("Email sent successfully")
        else:
            print("Email failed to send")
    return JsonResponse(response_data)

    '''to_item = request.POST.get('param1') #itemid of the item being proposed to
    to_user = Item.objects.get(itemid = to_item).owner #netid of the item being proposed to
    from_item = request.POST.get('param2') #itemid of the item being proposed from
    from_item = Item.objects.get(itemid = from_item)
    from_user = from_item.owner
    proposal = Proposal(proposer = from_user, proposedto = to_user, itembid = to_item, itemid = from_item.itemid, proposalid = str(uuid.uuid4()), status = 'Pending')
    if request.POST.get('message'):
        proposal.message = request.POST.get('message')
    print(proposal)
    proposal.save()
    return redirect(proposalsent)'''

def proposalsent(request):
    # *** change to post
    return render(request, "message-proposalsent.html")

@cas_required
def proposal(request):
    proposalid = request.GET.get('proposalid')
    proposal = Proposal.objects.get(proposalid = proposalid)
    itemowned = Item.objects.get(itemid = proposal.itembid)
    itemproposed = Item.objects.get(itemid = proposal.itemid)
    if request.user.username==itemowned.owner:
        can_accept = True
    else:
        can_accept = False
    if itemowned.image_url:
        owned_image_url = cloudinary.CloudinaryImage(itemowned.image_url).build_url(transformation=[    {'width': '50%'}])
        ownedhas_image = True
    else:
        ownedhas_image = False
        owned_image_url = ''
    if itemproposed.image_url:
        proposed_image_url = cloudinary.CloudinaryImage(itemproposed.image_url).build_url(transformation=[    {'width': '50%'}])
        proposedhas_image = True
    else:
        proposedhas_image = False
        proposed_image_url = ''
    proposaldetails = {'proposal': proposal, 'itemowned': itemowned, 
        'itemproposed': itemproposed, 'proposedhas_image' : proposedhas_image, 
        'proposed_image_url': proposed_image_url, 'ownedhas_image': ownedhas_image,
        'owned_image_url': owned_image_url, 'can_accept': can_accept}
    return render(request, "proposal.html", proposaldetails)

@cas_required
def proposalacceptance(request, proposalid):
    #proposalid = request.POST.get('param1')
    print('here')
    print(proposalid)
    proposal = Proposal.objects.get(proposalid = proposalid)
    proposal.status = 'Accepted'
    proposal.save()
    item1 = Item.objects.get(itemid = proposal.itembid)
    item2 = Item.objects.get(itemid = proposal.itemid)
    item1.isactive = False
    item2.isactive = False
    item1.save()
    item2.save()

    proposer = User.objects.get(username = proposal.proposer)
    proposedto = User.objects.get(username = proposal.proposedto)

    subject = f"Successful swap!"
    message = f'''
                Hi {item1.owner} and {item2.owner},
                
                You have made a successful trade on BubbleBarter!
                {item1.owner}'s {item1.title} for {item2.owner}'s {item2.title}.

                You can view the details of this trade on your account: https://bubblebarter.herokuapp.com/account/
                BubbleBarter has connected you both on this trade, so you can arrange a time and place to meet up and exchange your items.

                Thank you for swapping!
                '''
    html_message = f'''
                <html>
                <body style="font-family: Arial, sans-serif; font-size: 14px;">
                <p>Hi {item1.owner} and {item2.owner},</p>
                <br>
                <p>You have made a successful trade on BubbleBarter!</p>
                <p>{item1.owner}'s {item1.title} for {item2.owner}'s {item2.title}.</p>
                <br>
                <p>You can view the details of this trade on <a href="https://bubblebarter.herokuapp.com/account/">your account page.</a></p>
                <p>BubbleBarter has connected you both on this trade, so you can arrange a time and place to meet up and exchange your items.</p>
                <br>
                <p>Thank you for swapping!</p>
                </html>
                '''
    recipient_list = [proposer.email, proposedto.email]
    msg = EmailMultiAlternatives(subject, message, 'bubblebarter@gmail.com', recipient_list)
    msg.attach_alternative(html_message, "text/html")

    if msg.send(fail_silently=False):
        print("Email sent successfully")
    else:
        print("Email failed to send")


    # remove all proposals the items are involved in
    proposals = Proposal.objects.filter(itembid = proposal.itemid, status = 'Pending')
    for old_proposal in proposals:
        old_proposal.status = 'Rejected'
        old_proposal.dateupdated = timezone.now()
        old_proposal.save()
    proposals = Proposal.objects.filter(itembid = proposal.itembid, status = 'Pending')
    for old_proposal in proposals:
        old_proposal.status = 'Rejected'
        old_proposal.dateupdated = timezone.now()
        old_proposal.save()
    proposals = Proposal.objects.filter(itemid = proposal.itemid, status = 'Pending')
    for old_proposal in proposals:
        old_proposal.status = 'Rescinded'
        old_proposal.dateupdated = timezone.now()
        old_proposal.save()
    proposals = Proposal.objects.filter(itemid = proposal.itembid, status = 'Pending')
    for old_proposal in proposals:
        old_proposal.status = 'Rescinded'
        old_proposal.dateupdated = timezone.now()
        old_proposal.save()
    proposal.dateupdated = timezone.now()
    proposal.save()
    url = request.build_absolute_uri('/proposal/?proposalid=' + str(proposalid))
    #return redirect(request.META.get('HTTP_REFERER'))
    return redirect(account)

@cas_required
def proposalrejection(request):
    print('here')
    proposalid = request.POST.get('param1')
    proposal = Proposal.objects.get(proposalid = proposalid)
    proposal.status = 'Rejected'
    proposal.dateupdated = timezone.now()
    proposal.save()
    return redirect(account)

def swaprejected(request):
    return render(request, "message-swaprejected.html")

def swapsuccessful(request):
    return render(request, "message-swapsuccessful.html")

@cas_required
def postitem(request):
    tags = ['art', 'food', 'clothing', 'transport','fun', 'weird', 'event', 'ticket', 'misc', 'free', 'room', 'help']
    if request.user.email:
        has_email = True
    else:
        has_email = False
    context = {'categories': tags, 'has_email':has_email}
    return render(request, "postitem.html", context)

@cas_required
def edit_item(request, itemid):
    item = get_object_or_404(Item, itemid=itemid)
    print(item.get_active_tags())
    if request.user.username:
        netid = request.user.username
    else:
        netid = 'test_user'
    if item.owner == netid:
        can_edit = True
    else:
        can_edit = False
    if not can_edit or request.method != 'POST':
        return HttpResponseForbidden('<h1>Invalid access of edit item</h1>')
    if request.method == 'POST':
        item.title = request.POST.get('name')
        item.description = request.POST.get('description')
        item.wants = request.POST.get('wants')
        if request.FILES:
            image_file = request.FILES['myPhoto']
            result = cloudinary.uploader.upload(image_file, folder="bbapp_images")
            prev_id = item.image_public_id
            if prev_id:
                api.delete_resources([prev_id])
            item.image_url = result['url']
            item.image_public_id = result['public_id']
        if request.POST.get('edit-Fun'):
            item.fun_tag = True
        else:
            item.fun_tag = False
        if request.POST.get('edit-Weird'):
            item.weird_tag = True
        else:
            item.weird_tag = False
        if request.POST.get('edit-Event'):
            item.event_tag = True
        else:
            item.event_tag = False
        if request.POST.get('edit-Ticket'):
            item.ticket_tag = True
        else:
            item.ticket_tag = False
        if request.POST.get('edit-Misc'):
            item.misc_tag = True
        else: 
            item.misc_tag = False
        if request.POST.get('edit-Free'):
            item.free_tag = True
        else:
            item.free_tag = False
        if request.POST.get('edit-Room'):
            item.room_tag = True
        else:
            item.room_tag = False
        if request.POST.get('edit-Help'):
            item.help_tag = True
        else:
            item.help_tag = False
        if request.POST.get('edit-Art'):
            item.art_tag = True
        else:
            item.art_tag = False
        if request.POST.get('edit-Food'):
            item.food_tag = True
        else:
            item.food_tag = False
        if request.POST.get('edit-Clothing'):
            item.clothing_tag = True
        else:
            item.clothing_tag = False
        if request.POST.get('edit-Transport'):
            item.transport_tag = True
        else:
            item.transport_tag = False
        item.save()
        if request.POST.get('origin'):
            url = request.build_absolute_uri('/account/?tab=items')
        else:
            url = request.build_absolute_uri('/')
    return redirect(url)
    #return render('<h1>Invalid access of edit item</h1>')

@cas_required
def propose(request):
    id = request.GET.get('itemid')
    target_item = Item.objects.get(itemid = id) # Item being proposed to
    if target_item.owner:
        target_netid = target_item.owner #netid of the owner of the item being proposed to
    else:
        target_netid = 'test_user'
    if request.user.username:
        proposer_netid = request.user.username
    else:
        proposer_netid = 'test_user' # temp netid before cas approval
    owned_items = Item.objects.filter(owner = proposer_netid)
    context = {'to_item':target_item, 'owned_items':owned_items, 'proposer_netid':proposer_netid, 'target_netid':target_netid}
    return render(request, "propose.html",context)

def report(request, itemid):
    reporteduser = request.GET.get('reporteduser') or ''
    reporteditemid = request.GET.get('reporteditemid') or itemid or ''
    reporteditem = Item.objects.get(itemid = reporteditemid)
    reportedproposalid = request.GET.get('reportedproposalid') or ''
    context = {'reporteduser':reporteduser, 'reporteditemid':reporteditemid, 'reportedproposalid':reportedproposalid, 'reporteditemtitle': reporteditem.title}
    return render(request, "report.html", context)

def account_status(request):
    if request.user.is_authenticated:
        username = request.user.username
        account_status_message = f"Username: {username}"
    else:
        account_status_message = "User is not authenticated."

    if request.method == 'POST' and request.user.is_authenticated:
        subject = "Account Status"
        message = f"Hi {username},\n\nYour account status is active. This is a test of a cos333 project, email lshannon@princeton.edu for help."
        recipient_list = [request.user.email]
        if send_mail(
            subject,
            message,
            'bubblebarter@gmail.com',
            recipient_list,
            fail_silently=False,
        ):
            print("Email sent successfully")
        else:
            print("Email failed to send")

    context = {'account_status_message': account_status_message}
    return render(request, 'account_status.html', context)

def get_item_data(request, item_id):
    item = Item.objects.get(itemid=item_id)
    data = {'title': item.title, 'description': item.description, 'wants': item.wants}
    return JsonResponse(data)

@cas_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        user.email = email
        user.phonenumber = phonenumber
        user.save()
        print(user)
        return(redirect('/account'))

@cas_required
def rescind_proposal(request, proposalid):
    # Assure that current user is the proposer *******
    proposal = Proposal.objects.get(proposalid = proposalid)
    proposal.status = 'Rescinded'
    proposal.dateupdated = timezone.now()
    proposal.save()
    return redirect(account)

@cas_required
def delete_item(request, itemid):
    item = Item.objects.get(itemid = itemid)
    proposals_sent = Proposal.objects.filter(itemid = itemid)
    proposals_rec = Proposal.objects.filter(itembid = itemid)
    if item.image_public_id:
        api.delete_resources([item.image_public_id])
    item.delete()
    for proposal in proposals_sent:
        proposal.delete()
    for proposal in proposals_rec:
        proposal.delete()
    # response = redirect('/')
    previous_page_url = request.META.get('HTTP_REFERER', '/')
    print(previous_page_url)
    # Redirect the user to the previous page or default URL /
    return redirect(previous_page_url)

@cas_required
def help(request):
    return render(request, 'help.html')

def item_not_found(request):
    return render(request, 'item_not_found.html')