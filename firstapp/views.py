from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import *
from django.views.generic import View
from firstapp.models import SwapContract, SwapIntermediate, SwapDetails
from .forms import UserLogin, UserRegister, AddSwap, AddSwapContract, LoginForm, NewPassword
from django.http import *
from django.contrib.auth.models import User
from django.template import loader
from django.db.models import Q
from django.contrib.auth import logout as django_logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


def loginview(request):
    # next = request.GET.get('next', '/index/')
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        employee = User.objects.get(username=request.POST.get('username'))
        if user:
            login(request, user)
            return redirect('firstapp:index', employee.id)
    return render(request, 'firstapp/login_new1.html', {'login_form': form})


class UserCreateView(View):
    form_class = UserRegister
    template_name = 'firstapp/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # it won't save to database it's just be saved in the memory for further validation
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('firstapp:login')

        return render(request, self.template_name, {'form': form})


def forgotpasswordview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            validate_user = User.objects.get(username=username)
            if validate_user is not None:
                return redirect('firstapp:newpassword', validate_user.id)
        except User.DoesNotExist:
            error = "Invalid User Name"
            return render(request, 'firstapp/forgotpassword.html', {'error': error})
    error = ""
    return render(request, 'firstapp/forgotpassword.html', {'error': error})


def newpasswordview(request, user_id_new_pass):
    form = NewPassword(request.POST or None)
    if form.is_valid() and request.method == "POST":
        return redirect('firstapp:login')
    user = User.objects.get(id=user_id_new_pass)
    template = loader.get_template('firstapp/newpassword.html')
    context = {'pass_change_user': user}
    return HttpResponse(template.render(context, request))


def index(request, user_id):
    loggedin_user = User.objects.get(pk=user_id)
    template = loader.get_template('firstapp/index.html')
    context = {
        'loggedin_user': loggedin_user,
    }
    return HttpResponse(template.render(context, request))


class UserSwapCreateView(View):
    form_class = AddSwap
    template_name = 'firstapp/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # it won't save to database it's just be saved in the memory for further validation
            # employee = form.save(commit=False)
            name = request.POST.get('swap_name', '')
            swaptype = request.POST.get('swap_type', '')
            marginmoney = request.POST.get('margin_money', '')
            user = User.objects.get(username=request.user)
            swap = SwapContract(user=request.user, swap_name=name, swap_type=swaptype, margin_money=marginmoney)
            swap.save()
            return redirect('firstapp:swapdetails', user.id)

        return render(request, self.template_name, {'form': form})


class AddSwapContractView(View):
    form_class = AddSwapContract
    template_name = 'firstapp/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # it won't save to database it's just be saved in the memory for further validation
            # employee = form.save(commit=False)
            swapname = request.POST.get('swap_name', '')
            swapsector = request.POST.get('swap_sector', '')
            swapmargin = request.POST.get('swap_margin', '')
            swapbasecurr = request.POST.get('swap_base_curr', '')
            swapstartdate = request.POST.get('swap_start_date', '')
            swapenddate = request.POST.get('swap_end_date', '')
            user = User.objects.get(username=request.user)
            swap = SwapDetails(swap_owner=request.user, swap_name=swapname, swap_sector=swapsector, swap_margin=swapmargin, swap_base_curr=swapbasecurr, swap_start_date=swapstartdate, swap_end_date=swapenddate)
            swap.save()
            return redirect('firstapp:swapdetails', user.id)

        return render(request, self.template_name, {'form': form})


def user_swap_details(request, emp_id):
    swap_user_id = 0
    # employee_det = Employee.objects.get(pk=emp_id)
    loggedin_user = User.objects.get(pk=emp_id)
    all_user = User.objects.all()
    try:
        swap_user_pending = SwapDetails.objects.filter(swap_status_request=1)
        #for swaps in swap_user_pending:
         #   print(swaps.user_id, swaps.contract_add_user_id)
    except SwapDetails.DoesNotExist:
        swap_user_pending = None
    open_swap = SwapDetails.objects.filter(~Q(swap_owner=loggedin_user.id))
    template = loader.get_template('firstapp/detail_swap.html')
    context = {
       'loggedin_user': loggedin_user,
       'open_swap': open_swap,
       'swap_user_pending': swap_user_pending,
       'all_user': all_user,
    }
    return HttpResponse(template.render(context, request))


def all_open_swap(request):
    # employee_det = Employee.objects.get(pk=emp_id)
    loggedin_user = User.objects.get(username=request.user)
    open_swap = SwapDetails.objects.filter(~Q(swap_owner=loggedin_user.id))
    template = loader.get_template('firstapp/open_swap.html')
    context = {
        'open_swap': open_swap,
    }
    return HttpResponse(template.render(context, request))


def delete(request, swap_id):
    loggedin_user = User.objects.get(username=request.user)
    swap_det = SwapDetails.objects.get(pk=swap_id, swap_owner=loggedin_user.id)
    swap_det.delete()
    return redirect('firstapp:swapdetails', loggedin_user.id)


def come_in_contract(request, id_swap):
    loggedin_user = User.objects.get(username=request.user)
    swap_det = SwapDetails.objects.get(pk=id_swap)
    swap_det.swap_counter_party = loggedin_user.id
    swap_det.swap_status_request = 1
    swap_det.save()
    return redirect('firstapp:swapdetails', loggedin_user.id)


def accept_contract(request, accept_swap_id):
    get_swap_user_id = SwapDetails.objects.get(pk=accept_swap_id)
    get_swap_user_id.swap_status_accept = 1
    get_swap_user_id.save()
    return redirect('firstapp:swapdetails', get_swap_user_id.swap_owner_id)


def decline_contract(request, decline_swap_id):
    get_swap_user_id = SwapDetails.objects.get(pk=decline_swap_id)
    get_swap_user_id.swap_status_request = 0
    get_swap_user_id.swap_counter_party = 0
    get_swap_user_id.swap_status_accept = 0
    get_swap_user_id.save()
    return redirect('firstapp:swapdetails', get_swap_user_id.swap_owner_id)


def logout(request):
    django_logout(request)
    return redirect('firstapp:login')


def pie_routing(request):
    return render(request, 'firstapp/linechart1.html')


def currency_swap(request):
    return render(request, 'firstapp/linechart2.html')


def commodity_swap(request):
    return render(request, 'firstapp/linechart4.html')


def derivative_swap(request):
    return render(request, 'firstapp/linechart3.html')