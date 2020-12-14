from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import user_activation_token
from django.core.mail import EmailMessage

from django.views import generic

from pathlib import Path

from .models import Profile, Firm, AppUser
from .forms import AppUserCreationForm, ProfileUpdateForm


#TODO: Fix permissions issues 


def index(request):
    context = {}
    return render(request, 'CVtq/home.html', context)



def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(username + ' is logged in')
            
            return redirect('CVtq:index')
        
        else:
            print(username, password)
            messages.info(request, 'Invalid username or password')

    context = {}
    return render(request, 'CVtq/login.html', context)

def logoutPage(request):
    logout(request)
    context = {}

    return render(request, 'CVtq/home.html', context)



def registerPage(request):

    form = AppUserCreationForm()

    if request.method == 'POST':
        form = AppUserCreationForm(request.POST)
        

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('CVtq/user_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Please Confirm your email to complete registration.')
            
            return redirect('CVtq:login')
        
        else:
            errors = form.errors
            
            messages.info(request, errors.get('username'))
            messages.info(request, errors.get('email'))
            messages.info(request, errors.get('password'))
            messages.info(request, errors.get('password2'))
            
    
    context = {'form': form}
    return render(request, 'CVtq/register.html', context)



def activate_user(request, uidb64, token):
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = AppUser.objects.get(pk=uid)
    
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'CVtq/index.html', {})
    else:
        return HttpResponse('Activation link is invalid!')



def cvView(request, pk, profile_id):
    
    user = request.user

    print(request, pk, profile_id)
    profile = Profile.objects.get(id=profile_id)

    if profile:
        cv = profile.cv_file
        base_path = Path().cwd()
        print("Resolving path:  ", base_path / cv.path)
        path = base_path / cv.path
        return FileResponse(open(path, 'rb'), filename=cv.name ,content_type='application/pdf')
    
    else:
        return HttpResponseNotFound()




class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):

    login_url = '/login/'
    template_name = 'CVtq/account.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        print(user.id)
    
        profile = Profile.objects.filter(user_id=self.kwargs['pk'])
        
        # print(user.username, profile[0].user.username)
        return get_object_or_404(profile)
         

    def test_func(self):
        return True
        # is_profile_self = (self.kwargs['pk'] == self.request.user.id)
        # return ((self.request.user.is_firm and self.request.user.is_active) 
        #         or 
        #         (self.request.user.is_staff and self.request.user.is_active)
        #         or
        #         (self.request.user.is_profile and self.request.user.is_active and is_profile_self))
    



class ProfileDetailEditView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):

    login_url = '/login/'

    template_name = 'CVtq/account_edit.html'
    context_object_name = 'profile'

    fields = [
         'first_name',
         'last_name',
         'date_of_birth',
         'profile_domain',
         'is_available',
         'profile_text',
         'cv_file',
        ]
    
    def get_success_url(self):
        redirect_to = '/account/' + str(self.request.user.id) + '/'
        return redirect_to
        
    
    def get_object(self, get_queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
    
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


    def test_func(self):
        return True
        # print(self.request.user)
        # return (self.request.user.is_profile and self.request.user.is_active)


class ProfilesListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):

    login_url = '/login/'

    model = Profile
    template_name = 'CVtq/profiles.html'
    context_object_name = 'profiles_list'
    paginate_by = 20

    def test_func(self):
        return True
        # return ((self.request.user.is_firm and self.request.user.is_active) 
        #         or 
        #         (self.request.user.is_staff and self.request.user.is_active))


    def get_queryset(self):
        """Return all profiles"""

        return Profile.objects.all()



class FirmsView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):

    login_url = '/login/'

    model = Firm
    template_name = 'CVtq/firms.html'
    context_object_name = 'firms_list'
    paginate_by = 20


    def test_func(self):
        return self.request.user.is_staff


    def get_queryset(self):
        """Return all firms"""

        return Firm.objects.all()