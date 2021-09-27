from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from .forms import PersonForm
from .models import Person


@login_required
def persons_list(request):
    nome = request.GET.get('nome', None)
    sobrenome = request.GET.get('sobrenome', None)

    if nome and sobrenome:
        persons = Person.objects.filter(first_name__icontains=nome, last_name__icontains=sobrenome)

    elif nome:
        persons = Person.objects.filter(first_name__icontains=nome)

    elif sobrenome:
        persons = Person.objects.filter(last_name__icontains=sobrenome)

    else:
        persons = Person.objects.all()

    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})


# class PersonList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class PersonList(LoginRequiredMixin, ListView):
    model = Person
    # permission_required = 'polls.add_choice'
    # Or multiple of permissions:
    # permission_required = ('polls.view_choice', 'polls.change_choice')
    # context_object_name = 'name'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        primeiro_acesso = self.request.session.get('primeiro_acesso', False)

        if not primeiro_acesso:
            context['message'] = 'Primeiro acesso hoje, isso aí!'

            # Setar True depois de exibir mensagem
            self.request.session['primeiro_acesso'] = True

        else:
            context['message'] = 'Continue acessando, tudo muda quando você muda'

        return context
