from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic


# Sukurti puslapį (ne admin), kuriame būtų matoma statistika: paslaugų kiekis, atliktų užsakymų kiekis, automobilių kiekis

def index(request):
    paslaugu_kiekis = Paslauga.objects.all().count()
    atliktu_uzsakymu_kiekis = Uzsakymas.objects.filter(statusas__exact='uzbaigtas').count()
    automobiliu_kiekis = Automobilis.objects.all().count()

    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis
    }

    return render(request, 'index.html', context=context)


def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)


def automobilis(request, automobilis_id):
    vienas_automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', {'automobilis': vienas_automobilis})


class UzsakymasView(generic.ListView):
    model = Uzsakymas
    template_name = 'uzsakymas_list.html'

class UzsakymasDetails(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
