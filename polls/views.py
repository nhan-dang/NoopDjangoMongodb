# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from polls.forms import CommentForm, UserForm, UserProfileForm


class PostDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


def register(request):
    # Get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST.
    if request.method == 'POST':
        # Grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash the password with the set_password method.
            # Update the user object.
            user.set_password(user.password)
            user.save()

            # Sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'D:\Sublime\Mission\mysite\website\templates\register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def user_login(request):
    # Get the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST['username']
        password = request.POST['password']

        # Django's machinery to attempt to see if the username/password combination is valid.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no user with matching credentials was found.
        if user:
            # Is the account active?
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                login(request, user)
                return HttpResponseRedirect('D:\Sublime\Mission\mysite\website\templates')
            else:
                # An inactive account was used
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST
    else:
        # No context variables to pass to the template system
        return render_to_response('D:\Sublime\Mission\mysite\website\templates\login.html', {}, context)

#No need for RequestContext() cause we don't need to get request's context from Django's backend for simple logout
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('D:\Sublime\Mission\mysite\website\templates')
