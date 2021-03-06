from django.shortcuts import render,redirect,get_object_or_404
from .models import Image,Location,tags, Profile,Review, NewsLetterRecipients,Like,Project
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import NewImageForm, UpdatebioForm, ReviewForm, NewProjectForm
from .email import send_welcome_email
from .forms import NewsLetterForm
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer, ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly


# Create your views here.
  
@login_required(login_url='/accounts/login/')
def home(request):
  
   if request.GET.get('search_term'):
        projects = Project.search_project(request.GET.get('search_term'))

   else:
     projects = Project.objects.all()

   form = NewsLetterForm

   if request.method =='POST':
       form = NewsLetterForm(request.POST or None)

       if form.is_valid():
             name = form.cleaned_data['your_name']
             email = form.cleaned_data['email']

             recipient = NewsLetterRecipients(name=name,email=email)
             recipient.save()

             send_welcome_email(name,email)

             HttpResponseRedirect('home')

   return render(request, 'index.html', {'projects': projects, 'letterForm':form})

def project(request, id):
    
    try:
        project = Project.objects.get(pk = id)
    except DoesNotExit:
         raise Htt404()

    current_user = request.user
    comments = Review.get_comment(Review, id)
    latest_review_list= Review.objects.all()

    if request.method == 'POST':
       form = ReviewForm(request.POST)
       if form.is_valid():
         design_rating = form.cleaned_data['design_rating']
         content_rating = form.cleaned_data['content_rating']
         usability_rating = form.cleaned_data['usability_rating']
         comment = form.cleaned_data['comment']

         review = Review()
         review.project = project
         review.user = current_user
         review.comment = comment
         review.design_rating = design_rating
         review.content_rating = content_rating
         review.save()

    else: 
        form = ReviewForm()

    return render(request,'image.html', {"project": project,'form':form,'comments':comments,'latest_review_list':latest_review_list})
                          

@login_required(login_url='/accounts/login/')
def new_image(request):
   current_user = request.user
   if request.method =='POST':
        form = NewImageForm(request.POST, request.FILES)
        
        if form.is_valid():
             image= form.save(commit=False)
             image.user= current_user
             image.save()
        return redirect('homePage')

   else: 
       form = NewImageForm()

   return render(request,'registration/new_image.html', {"form":form})

@login_required(login_url='/accounts/login')
def new_project(request):
   current_user = request.user
   if request.method == 'POST':
      form = NewProjectForm(request.POST,request.FILES)
      if form.is_valid():
          project = form.save(commit=False)
          project.user = current_user
          project.save()
   
      return redirect('homePage')

   else:
        form = NewProjectForm()

   return render(request, 'registration/new_project.html',{"form":form})


def user_list(request):
    user_list =User.objects.all()
    context ={'user_list': user_list}
    return render(request, 'user_list.html', context)

@login_required(login_url='/accounts/login')
def edit_profile(request):
   current_user = request.user

   if request.method =='POST':
        form = UpdatebioForm(request.POST,request.FILES, instance= current_user.profile)
        print(form.is_valid())
        if form.is_valid():
           image = form.save(commit=False)
           image.user = current_user
           image.save()
        return redirect('homePage')

   else:
       form = UpdatebioForm()
   return render(request, 'registration/edit_profile.html', {"form":form})

@login_required(login_url='accounts/login/')
def individual_profile_page(request,username=None):
   if not username:
        username=request.user.username
   images=Image.objects.filter(user_id=username)
   return render(request,'registration/user_image_list.html',{'images':images,'username':username})

def search_projects(request):

   if 'project' in request.GET and request.GET["project"]:
       search_term = request.GET.get("project")
       search_projects = Project.search_projects(search_term)
       message = f"{search_term}"

       return render(request, 'search.html', {"message": message, "projects": search_projects})
   else:
       message = "You haven't searched for any person"
       return render(request, 'search.html', {"message": message})

def search_image(request):

          if 'image' in request.GET and request.GET["image"]:
             search_term = request.GET.get("image")
             searched_images = Image.search_image(search_term)
             message = f"{search_term}"

             return render(request, 'search.html', {"message":message, "pictures": search_images})

          else:
              message ="you haven't searched for any image"
              return render(request, 'search.html',{"message": message})

@login_required(login_url='/accounts/login/')
def individual_profile_page(request,username):
    print(username)
    if not username:
        username = request.user.username

    images = Image.objects.filter(user_id=username)
    user = request.user
    profile = Profile.objects.get(user=user)
    userf = User.objects.get(pk=username)
    latest_review_list = Review.objects.filter(user_id=username).filter(user_id=username)
    context = {'latest_review_list': latest_review_list}
    if userf:
        print('user found')
        profile = Profile.objects.get(user=userf)

    else:
        print('That user does not exist')
    return render(request, 'registration/user_image_list.html', context, {'images':images,'profile':profile,'user':user,'username':username})

def review_list(request):
    latest_review_list = Review.objects.all()
    context = {'latest_review_list': latest_review_list}
    return render(request,'review_list.html', context)

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review_details.html', {'review': review})

def project_list(request):
    project_list = Profile.objects.order_by('-title')
    context = {'project_list': project_list}
    return render(request, 'project_list.html', context)


def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name= name, email = email)
    recipient.save()
    send_welcome_email(name,email)
    data= {'success': 'You have been successfully added to the newsletter mailing list'}
    return jsonResponse(date)

class ProjectList(APIView):
    def get(self, request, format = None):
       all_projects = Profile.objects.all()
       serializers  = ProfileSerializer(all_projects, many = True)
       return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)

        if serializers.is_valid():
           serializers.save()
           return Response(serializers.data, status= status.HTT_201_CREATED)

        return Response(serializers.errors, status = status.HTT_400_BAD_REQUEST)

class ProjectDescription(APIView):
      permission_classes = (IsAdminOrReadOnly,)
      def get_project(self, pk):
          try:

             return Project.objects.get(pk=pk)
          except Project.DoesNotExit:
               return Http404

      def get(self, request, pk, format=None):
          project = self.get_project(pk)
          serializers = ProfileSerializer(project)
          return Response(serializers.data)
      
      def put(self, request, pk, format = None):
          project = self.get_project(pk)
          serializers = ProfileSerializer(project,request.data)
          if serializers.is_valid():
               serializers.save()
               return Response(serializers.data)

          else:
              return Response(serializers.errors,status = status.HTT_400_BAD_REQUEST)

      def delete(self, request, pk, format=None):
          project= self.get_project(pk)
          project.delete()
          return Response(status=status.HTT_204_NO_CONTENT)

class ProjectList(APIView):
     def get(self, request, format = None):
         all_projects = Profile.objects.all()
         serializers = ProfileSerializer(all_profiles, many = True)
         return Response(serializers.data)

     def post(self, request, format=None):
          serializers = ProfileSerializer(data=request.data)
          permission_classes = (IsAdminOrReadOnly,)

          if serializers.is_valid():
               serializers.save()
               return Response(serializers.data, status= status.HTT_201_CREATED)

          return Response(serializers.errors, status = status.HTT_400_BAD_REQUEST)

class ProfileDescription(APIView):
      permission_classes = (IsAdminOrReadOnly,)
      def get_profile(self, pk):
          try:
              return Profile.objects.get(pk=pk)
          except Profile.DoesNotExit:
              return Htt404

      def get(self, request, pk, format= None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
           serializers.save()
           return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTT_400_BAD_REQUEST)

      def delete(self,request,pk, format=None):
          profile = self.get_profile(pk)
          profile.delete()
          return Response(status=status.HTT_204_NO_CONTENT)
