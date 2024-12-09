from django.contrib import admin
from .models import AutomobilioModelis, Automobilis, Paslauga, Uzsakymas, UzsakymoEilute, UzsakymoKomentaras, Profilis


class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 1


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('id', 'automobilis', 'statusas', 'vartotojas', 'grazinimo_terminas', 'is_overdue')
    inlines = [UzsakymoEiluteInline]
    list_filter = ('statusas', 'grazinimo_terminas')
    search_fields = ('automobilis__valstybinis_nr', 'vartotojas__username')


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas', 'nuotrauka')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


class UzsakymoKomentarasAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'user', 'content', 'created_at')


admin.site.register(UzsakymoKomentaras, UzsakymoKomentarasAdmin)
admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Profilis)
