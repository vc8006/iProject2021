from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.views import View
from .forms  import *
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from recruiter.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "StudentLanding.html")

class StudentRegistration(CreateView):
    model = User
    form_class = StudentsForm
    template_name = './StudentRegistration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return HttpResponseRedirect(reverse('StudentProfile',kwargs={'pk': user.id}))



class StartUpsRegistration(CreateView):
    model = User
    form_class = StartUpsForm
    template_name = 'recruiter/RecruiterRegistration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'startup'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': user.id}))


def StudentProfile(request,**kwargs):

    user = Students.objects.get(user=request.user)
    registered_internships = InternApplication.objects.filter(Intern__id = user.pk)
    print(registered_internships)
    return render(request, "StudentProfile1.html",{'student':user,'interns':registered_internships})


def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('StudentProfile',kwargs={'pk': user.id}))
                # return redirect('/student/profile',kwargs={'pk': user.id})
            else:
                return redirect('/',{'error':'User is flagged Inactive. Drop mail to internfair@udgam.in to reactivate your account'})
        else:
            return redirect('/', {'error':'Invalid login details given'})
    else:
        return redirect('/')

def startupLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('recruiter:Profile',kwargs={'pk': user.id}))
                return redirect('../recruiter/profile')
            else:
                return redirect('../recruiter',{'error':'User is flagged Inactive. Drop mail to internfair@udgam.in to reactivate your account'})
        else:

            return redirect('../recruiter',{'error':'Invalid login details given'})
    else:
        return redirect('../recruiter')




def AvailableInternships(request):
    if request.method == "POST":
        print(request.POST)
        student = Students.objects.get(user=request.user)
        startup = request.POST["startup"]
        profile = request.POST["profile"]
        id = request.POST['id']
        internship = Intern_form.objects.get(pk=id)
        answers  = request.POST.getlist("answers")
        print(internship.location)
        app = InternApplication.objects.create(Intern=student,Internship = internship, Answers=answers)
        # app = [student.name,startup,profile,internship,answers]
        print(app)
        return redirect('StudentProfile')

    else:
        available_internships = Intern_form.objects.all()

        template = "AvailableInternships.html"
        context = {'interns': available_internships}

        return render(request, template, context)



def EditStudProfile(request, **kwargs):
    current_user = request.user
    student = Students.objects.get(user=current_user)
    if request.method=='POST':
        if request.POST['roll_number']:
            student.roll_number = request.POST['roll_number']
        if request.POST['department']:
            student.department = request.POST['department']
        if request.POST['bio']:
            student.bio = request.POST['bio']
        student.save()
    return HttpResponseRedirect(reverse('StudentProfile',kwargs={'pk': current_user.id}))







# if request.method=='POST':
#         if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
#             product=Product()
#             product.title= request.POST['title']
#             product.body= request.POST['body']

#             if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
#                 product.url= request.POST['url']
#             else:
#                 product.url= 'http://' + request.POST['url']

#             product.icon = request.FILES['icon']
#             product.image = request.FILES['image']
#             product.pub_date= timezone.datetime.now()
#             product.hunter = request.user
#             product.save()
            

#             return redirect('/products/'+str(product.id))
#         else:
#             return render(request, 'products/create.html', {'error':'All fields are required.'})

#     else:
#         return render(request, 'products/create.html')

def logout_view(request):
    logout(request)
    return redirect( 'index')

def search(request):
    query = request.GET['query']
    interns = StartUps.objects.filter(companyName__icontains = query)
    params = {'interns':interns}
    return render(request,search.html,params)