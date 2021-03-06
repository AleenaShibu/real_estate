from django.shortcuts import render
from django.views.generic import ListView,DetailView 
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .models import Realtor

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.conf import settings

class PropertyListView(ListView):
	model = Realtor
	template_name ='home.html'

class PropertyDetailView( LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	model = Realtor
	template_name ='detail.html'
	login_url = 'login'
	permission_required = 'realtors.special_access' 

class AddPropertyView(CreateView):
	model = Realtor
	template_name ='addproperty.html'
	fields = ['owner_name','description','email','photo','phone','district','owner']
		
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)
						
	

class DeletePropertyView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Realtor
	template_name = 'delete.html'
	success_url = reverse_lazy('home')
	login_url = 'login'

	def test_func(self):
		obj = self.get_object()
		return obj.owner == self.request.user

    
class EditPropertyView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Realtor
	template_name = 'edit.html'
	fields = ['owner_name','description','email','photo','phone','district','owner']


	def test_func(self):
		obj = self.get_object()
		return obj.owner == self.request.user

	
	
class SearchPropertyView(ListView):
	model = Realtor
	template_name = 'search.html'

	def ger_Queryset(self):
		query =self.request.GET['q']
		return Realtor.objects.filter(name__icontains=query)
	

