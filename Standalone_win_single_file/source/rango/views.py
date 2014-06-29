from django.shortcuts import render_to_response
from django.template import RequestContext
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    category_view_list = Category.objects.order_by('-views')[:5]
    all_categories = Category.objects.order_by('name')
    context_dict = {'categories': category_list, 'view_count': category_view_list, 'all_categories': all_categories}

    for category in category_list:
        category.url = encode_url(category.name)

    for views in category_view_list:
        views.url = encode_url(views.name)

    for item in all_categories:
        item.url = encode_url(item.name)

    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

    try:
        category = Category.objects.get(name=category_name)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)

@login_required
def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:
            print form.errors
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    category_clean = category_name_url.replace('/add_page', '')

    category_clean_final = decode_url(category_clean)


    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():

            page = form.save(commit=False)


            try:
                cat = Category.objects.get(name=category_clean_final)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/index.html', {'category_clean_final': category_clean_final}, context)

            page.views = 0


            page.save()

            return category(request, category_clean)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',
        {'category_name_url': category_name_url,
         'category_name': category_name,
         'category_clean': category_clean,
         'form': form},
        context)

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context
    )

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponseRedirect("Your Rango account is disabled.")

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('rango/log_in.html', {}, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')