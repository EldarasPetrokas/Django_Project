from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from .forms import CommentForm, UserUpdateForm, ProfilisUpdateForm


def index(request):
    paslaugu_kiekis = Paslauga.objects.all().count()
    atliktu_uzsakymu_kiekis = Uzsakymas.objects.filter(statusas__exact='uzbaigtas').count()
    automobiliu_kiekis = Automobilis.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


def automobiliu_sarasas(request):
    automobiliai = Automobilis.objects.all()
    paginator = Paginator(automobiliai, 10)  # 10 įrašų per puslapį
    page_number = request.GET.get('page')
    automobiliu_puslapis = paginator.get_page(page_number)
    return render(request, 'automobiliai.html', {'automobiliai': automobiliu_puslapis})


def automobilis(request, automobilis_id):
    vienas_automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', {'automobilis': vienas_automobilis})


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 10
    template_name = 'uzsakymas_list.html'
    context_object_name = 'uzsakymai'


class UzsakymasDetails(FormMixin, DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.uzsakymas = self.object
            comment.user = self.request.user
            comment.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


def search(request):
    """
    Paprasta paieška. Naudojame `query` iš paieškos laukelio,
    kad filtruotume automobilius pagal pavadinimą, modelį, klientą ir VIN kodą.
    """
    query = request.GET.get('query', '')  # Gaukite užklausą arba naudokite tuščią string
    search_results = Automobilis.objects.filter(
        Q(valstybinis_nr__icontains=query) |
        Q(automobilio_modelis__marke__icontains=query) |
        Q(automobilio_modelis__modelis__icontains=query) |
        Q(vin_kodas__icontains=query) |
        Q(klientas__icontains=query)
    ) if query else Automobilis.objects.none()  # Grąžinkite tuščią rezultatą, jei nėra užklausos

    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


class UserUzsakymaiView(LoginRequiredMixin, ListView):
    model = Uzsakymas
    template_name = 'user_uzsakymai.html'
    context_object_name = 'uzsakymai'

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).order_by('grazinimo_terminas')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)

