from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CustomUser,Property,PropertyImage,Review
from django.contrib.auth.decorators import login_required
from django.views import View 
from .forms import PropertyForm,ReviewForm

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # authenticate uses username by default, so if email is your login field:
        try:
            from .models import CustomUser
            user_obj = CustomUser.objects.get(email=email)
            username = user_obj.username
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name} ({user.user_type})!")

            # Redirect based on user_type
            if user.user_type == 'broker':
                return redirect('broker_dashboard')
            elif user.user_type == 'agent':
                return redirect('agent_dashboard')
            else:  # buyer
                return redirect('buyer_dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')

# REGISTER VIEW
def register_view(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('c_pass')
        user_type = request.POST.get('user_type')  # Get role from dropdown

        # 1️⃣ Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')

        # 2️⃣ Check if email already exists
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'register.html')

        # 3️⃣ Create user
        user = CustomUser.objects.create_user(
            username=email,      # Using email as username
            email=email,
            password=password,
            first_name=name,
            user_type=user_type,  # Save role
            is_verified=False     # Optional: admin verification
        )

        user.save()

        messages.success(request, "Account created successfully! Please wait for verification if you are an Agent or Broker.")
        return redirect('login')

    return render(request, 'register.html')

# -------------------------
# broker Dashboard Views
# -------------------------
class BrokerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'broker_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get ACTIVE agents only
        agents = CustomUser.objects.filter(
            user_type='agent',
            is_active=True
        )

        context['agents'] = agents
        return context

class ManageAgentsView(LoginRequiredMixin, View):
    """
    View for broker to manage all agents.
    Requires user to be logged in.
    """
    def get(self, request, *args, **kwargs):
        # Later: Fetch agents from your database
        context = {
            'title': 'Manage Agents',
            'user_type': request.user.user_type,
        }
        return render(request, 'broker/manage_agents.html', context)


class ManagepropertiesView(LoginRequiredMixin, View):
    """
    View for broker to manage all property listings.
    Requires user to be logged in.
    """
    def get(self, request, *args, **kwargs):
        # Later: Fetch properties from your database
        context = {
            'title': 'Manage Properties',
            'user_type': request.user.user_type,
        }
        return render(request, 'broker/manage_properties.html', context)


@login_required
def agent_dashboard_view(request):
    buyers = CustomUser.objects.filter(user_type="buyer")
    properties = Property.objects.filter(agent=request.user)
    context = {
        "buyers": buyers,
        "properties": properties,
    }
    return render(request, "agent_dashboard.html", context)

@login_required
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.agent = request.user
            property_instance.save()

            # ✅ SAVE MULTIPLE IMAGES
            images = request.FILES.getlist('images')
            for img in images:
                PropertyImage.objects.create(
                    property=property_instance,
                    image=img
                )

            return redirect("agent_dashboard")
        else:
            print(form.errors)
    else:
        form = PropertyForm()

    return render(request, "agent/add_property.html", {"form": form})

@login_required
def edit_property(request, id):
    """
    Allows an agent to edit their own property listing.
    """
    # Make sure property belongs to the logged-in agent
    property_instance = get_object_or_404(Property, id=id, agent=request.user)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()

             # ✅ ADD NEW IMAGES (DOES NOT DELETE OLD ONES)
            images = request.FILES.getlist('images')
            for img in images:
                PropertyImage.objects.create(
                    property=property_instance,
                    image=img
                )
            messages.success(request, "Property updated successfully!")
            return redirect("agent_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, "agent/edit_property.html", {"form": form, "property": property_instance})

@login_required
def delete_property(request, id):
    """
    Allows an agent to delete a property they own.
    """
    # Make sure the property belongs to the logged-in agent
    property_instance = get_object_or_404(Property, id=id, agent=request.user)
    
    if request.method == "POST":
        property_instance.delete()
        return redirect("agent_dashboard")
    
    # Optional: confirm deletion page
    return render(request, "agent/delete_property.html", {"property": property_instance})
# -------------------------
# Agent Dashboard Views
# -------------------------

class AgentDashboardView(LoginRequiredMixin, View):
    """
    Dashboard main page for agents.
    """
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Agent Dashboard',
            'user_type': request.user.user_type,
        }
        return render(request, 'agent/agent_dashboard.html', context)


class ViewBuyersView(LoginRequiredMixin, View):
    """
    Page for agents to view buyer information.
    """
    def get(self, request, *args, **kwargs):
        # Replace this with your actual Buyer model query
        buyers = [
            {'name': 'John Doe', 'email': 'john@example.com', 'phone': '09123456789'},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '09987654321'}
        ]
        context = {
            'title': 'View Buyers',
            'buyers': buyers,
            'user_type': request.user.user_type,
        }
        return render(request, 'agent/view_buyers.html', context)
    
class ListingsPageView(TemplateView):
    template_name = "agent/listings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["properties"] = Property.objects.filter(
            is_available=True
        ).order_by("-created_at")

        return context
    
class BasePageView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["properties"] = Property.objects.filter(
            is_available=True
        ).order_by("-created_at")

        return context

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        message = request.POST.get("message")

        # You can save to DB or send email here
        messages.success(request, "Message sent successfully!")

        return redirect('contact')

    return render(request, 'contact.html')
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('about')  # redirect after submit
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form})

class AgentDashboardView(TemplateView):
    template_name = 'agent_dashboard.html'


class BuyerDashboardView(TemplateView):
    template_name = 'buyer_dashboard.html'



class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.order_by("-created_at")
        return context

class ContactPageView(TemplateView):
    template_name = 'contact.html'

class SearchPageView(TemplateView):
    template_name = 'search.html'

class View_propertyPageView(TemplateView):
    template_name = 'view_property.html'

