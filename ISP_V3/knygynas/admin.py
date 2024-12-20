from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import (
    Knyga
)


@admin.action(description="Toggle 'Užšaldyta' status")
def toggle_uzsaldyta(modeladmin, request, queryset):
    # Iterate through selected books
    for book in queryset:
        book.uzsaldyta = not book.uzsaldyta
        book.save()
    # Add a success message
    messages.success(request, "Užšaldyta status successfully toggled for selected books.")




class KnygaForm(ModelForm):
    class Meta:
        model = Knyga
        fields = '__all__'

    def clean_akcija(self):
        akcija = self.cleaned_data.get('akcija')
        if akcija is not None:
            if akcija < 0 or akcija > 100:
                raise ValidationError('Akcija (discount) must be between 0 and 100.')
        return akcija



class KnygaAdmin(admin.ModelAdmin):
    form = KnygaForm
    list_display = (
        'pavadinimas', 
        'kaina', 
        'likutis', 
        'akcija', 
        'autorius', 
        'leidykla', 
        'uzsaldyta_status', 
        'apply_discount_button'
    )
    list_filter = ('fk_Leidykla', 'fk_Autorius', 'uzsaldyta')
    search_fields = ('pavadinimas', 'fk_Autorius__vardas', 'fk_Leidykla__pavadinimas')
    actions = [toggle_uzsaldyta]

    def uzsaldyta_status(self, obj):
        return obj.uzsaldyta

    uzsaldyta_status.boolean = True
    uzsaldyta_status.short_description = "Užšaldyta"

    def apply_discount_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Apply Discount</a>',
            reverse('admin:apply_discount', args=[obj.pk])
        )

    apply_discount_button.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/apply-discount/',
                self.admin_site.admin_view(self.apply_discount_view),
                name='apply_discount',
            ),
        ]
        return custom_urls + urls

    def apply_discount_view(self, request, pk):
        knyga = get_object_or_404(Knyga, pk=pk)

        if request.method == 'POST':
            akcija = request.POST.get('akcija')
            akcijos_galiojimas = request.POST.get('akcijos_galiojimas')

            if akcija and akcijos_galiojimas:
                try:
                    akcija = float(akcija)
                    akcijos_galiojimas = timezone.datetime.strptime(akcijos_galiojimas, '%Y-%m-%d').date()

                    if akcija < 0 or akcija > 100:
                        messages.error(request, 'Akcija (discount) must be between 0 and 100.')
                    else:
                        knyga.akcija = akcija
                        knyga.akcijos_galiojimas = akcijos_galiojimas
                        knyga.save()
                        messages.success(request, f'Discount of {akcija}% applied to "{knyga.pavadinimas}" until {akcijos_galiojimas}.')
                        return redirect('admin:knygynas_knyga_changelist')

                except ValueError:
                    messages.error(request, 'Invalid input. Please ensure all fields are correctly filled.')

        return render(request, 'admin/akcijos_forma.html', {
            'knyga': knyga,
        })


admin.site.register(Knyga, KnygaAdmin)

# Register your models here.
