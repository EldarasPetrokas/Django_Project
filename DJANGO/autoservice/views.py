from django.shortcuts import render
from django.http import HttpResponse
from .models import Paslauga, Uzsakymas, Automobilis


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



