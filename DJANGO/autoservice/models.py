from datetime import date
from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth.models import User
import uuid
from PIL import Image


class AutomobilioModelis(models.Model):
    id = models.AutoField(primary_key=True)
    marke = models.CharField('Markė', max_length=100)
    modelis = models.CharField('Modelis', max_length=100)

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobiliu modeliai"


class Automobilis(models.Model):
    id = models.AutoField(primary_key=True)
    valstybinis_nr = models.CharField('Valstybinis numeris', max_length=8)
    automobilio_modelis = models.ForeignKey(AutomobilioModelis, on_delete=models.CASCADE)
    vin_kodas = models.CharField('VIN kodas', max_length=17)
    klientas = models.CharField('Klientas', max_length=255)
    nuotrauka = models.ImageField('Nuotrauka', upload_to='automobiliai/', null=True, blank=True)
    aprasymas = HTMLField('Aprašymas', null=True, blank=True)

    def __str__(self):
        return f"{self.valstybinis_nr} ({self.klientas})"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Paslauga(models.Model):
    id = models.AutoField(primary_key=True)
    pavadinimas = models.CharField('Pavadinimas', max_length=255)
    kaina = models.DecimalField('Kaina', max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.pavadinimas} - {self.kaina} €"

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class Uzsakymas(models.Model):
    STATUSO_BUSENA = [
        ('nepradetas', 'Nepradėtas'),
        ('vykdomas', 'Vykdomas'),
        ('uzbaigtas', 'Užbaigtas'),
        ('atsauktas', 'Atšauktas')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    data = models.DateField('Data', auto_now_add=True)
    automobilis = models.ForeignKey(Automobilis, on_delete=models.CASCADE)
    statusas = models.CharField(max_length=20, choices=STATUSO_BUSENA, default='nepradetas')
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_terminas = models.DateField('Gražinimo terminas', null=True, blank=True)

    @property
    def is_overdue(self):
        if self.grazinimo_terminas and date.today() > self.grazinimo_terminas:
            return True
        return False

    def __str__(self):
        return f"Užsakymas {self.id} ({self.data}) - {self.statusas}"

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"


class UzsakymoEilute(models.Model):
    id = models.AutoField(primary_key=True)
    paslauga = models.ForeignKey(Paslauga, on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE)
    kiekis = models.PositiveIntegerField('Kiekis')

    def __str__(self):
        return f"{self.paslauga.pavadinimas} x {self.kiekis} ({self.uzsakymas.id})"

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"


class UzsakymoKomentaras(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, related_name='komentaras')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.uzsakymas}'


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
