from django.db import models
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

# Create your models here.

# class TodoItem(models.Model):
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(default=False)
    
#     class Meta:
#         db_table = "todos"

class Autorius(models.Model):
    id_Autorius = models.AutoField(primary_key=True)  # Explicitly define the primary key
    vardas = models.CharField(max_length=255)
    pavarde = models.CharField(max_length=255)
    gimimo_metai = models.DateField()

    class Meta:
        db_table = 'autoriai'  # Maps to the existing SQL table

    def __str__(self):
        return f"{self.vardas} {self.pavarde}"

class Kurjeris(models.Model):
    id_Kurjeris = models.AutoField(primary_key=True)  # Explicitly define the primary key
    pavadinimas = models.CharField(max_length=255)
    tel_numeris = models.CharField(max_length=255)
    el_pastas = models.CharField(max_length=255)
    transporto_priemones_tipas = models.CharField(max_length=255, blank=True, null=True)
    paslaugu_teikimo_teritorija = models.CharField(max_length=255)
    reitingas = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'kurjeriai'  # Maps to the existing SQL table

    def __str__(self):
        return self.pavadinimas

class Leidykla(models.Model):
    id_Leidykla = models.AutoField(primary_key=True)  # Explicitly define the primary key
    pavadinimas = models.CharField(max_length=255)
    adresas = models.CharField(max_length=255)
    ikurimo_data = models.DateField()

    class Meta:
        db_table = 'leidyklos'  # Maps to the existing SQL table

    def __str__(self):
        return self.pavadinimas
    
    
class PrekiuUzsakymas(models.Model):
    id_Prekiu_uzsakymas = models.AutoField(primary_key=True)  # Explicitly define the primary key
    knygu_kiekis = models.IntegerField()
    uzsakymo_data = models.DateField()
    issiuntimo_data = models.DateField()
    atvykimo_data = models.DateField()
    prekiu_busena = models.CharField(
        max_length=9,
        choices=[
            ('užsakyta', 'Užsakyta'),
            ('atvyksta', 'Atvyksta'),
            ('įvykdyta', 'Įvykdyta'),
            ('atšaukta', 'Atšaukta'),
            ('grąžinama', 'Grąžinama'),
        ]
    )

    class Meta:
        db_table = 'prekiu_uzsakymai'  # Maps to the existing SQL table

    def __str__(self):
        return f"Užsakymas #{self.id_Prekiu_uzsakymas} ({self.prekiu_busena})"
    
    
class Sandelis(models.Model):
    id_Sandelis = models.AutoField(primary_key=True)  # Explicitly define the primary key
    adresas = models.CharField(max_length=255)
    inventorius = models.IntegerField()
    talpa = models.IntegerField()

    class Meta:
        db_table = 'sandeliai'  # Maps to the existing SQL table

    def __str__(self):
        return f"Sandelis #{self.id_Sandelis} ({self.adresas})"
    

class Vartotojas(models.Model):
    id_Vartotojas = models.AutoField(primary_key=True)  # Explicitly define the primary key
    vardas = models.CharField(max_length=255)
    pavarde = models.CharField(max_length=255)
    gimimo_data = models.CharField(max_length=255)  # This should ideally be a DateField if the data format is a date
    miestas = models.CharField(max_length=255)
    el_pastas = models.CharField(max_length=255)
    pasto_kodas = models.CharField(max_length=255)
    adresas = models.CharField(max_length=255)
    slaptazodis = models.CharField(max_length=255)
    slapyvardis = models.CharField(max_length=255)
    role = models.CharField(
        max_length=14,
        choices=[
            ('admin', 'Admin'),
            ('registruotas', 'Registruotas'),
            ('neregistruotas', 'Neregistruotas'),
        ]
    )

    class Meta:
        db_table = 'vartotojai'  # Maps to the existing SQL table

    def __str__(self):
        return f"{self.vardas} {self.pavarde} ({self.role})"
    
    
class Knyga(models.Model):
    id_Knyga = models.AutoField(primary_key=True)  # Explicitly define the primary key
    kaina = models.FloatField()
    original_kaina = models.FloatField(blank=True, null=True)  # To store the original price
    leidimo_metai = models.DateField()
    aprasymas = models.CharField(max_length=255, blank=True, null=True)
    likutis = models.IntegerField()
    pavadinimas = models.CharField(max_length=255)
    akcija = models.FloatField(blank=True, null=True)
    akcijos_galiojimas = models.DateField(blank=True, null=True)
    uzsaldyta = models.BooleanField()
    virselio_tipas = models.CharField(
        max_length=8,
        choices=[
            ('kietas', 'Kietas'),
            ('minkštas', 'Minkštas'),
        ]
    )
    fk_Leidykla = models.ForeignKey('Leidykla', on_delete=models.CASCADE, db_column='fk_Leidykla')
    fk_Autorius = models.ForeignKey('Autorius', on_delete=models.CASCADE, db_column='fk_Autorius')

    class Meta:
        db_table = 'knygos'  
        verbose_name = 'Knyga'
        verbose_name_plural = 'Knygos'
        
    def autorius(self):
        return f"{self.fk_Autorius}"
    
    def leidykla(self):
        return f"{self.fk_Leidykla}"
    
    def __str__(self):
        return self.pavadinimas  

    # Views admine
    autorius.short_description = 'Autorius'
    leidykla.short_description = 'Leidykla'  
   
   
   # skaiciavimo dalykai
   
    def clean(self):
            # Validate that discount is between 0 and 100
            if self.akcija is not None:
                if self.akcija < 0 or self.akcija > 100:
                    raise ValidationError({'akcija': 'Akcija (discount) must be between 0 and 100.'})
                
                
    # Update the price when a discount is applied
    # Check expiration and update price accordingly
    def save(self, *args, **kwargs):
        # Check if the original price is set
        if not self.original_kaina:
            self.original_kaina = self.kaina

        # Check if akcijos_galiojimas is set and has expired
        if self.akcijos_galiojimas and self.akcijos_galiojimas < timezone.now().date():
            # Remove the discount and reset the price
            self.akcija = None
            self.akcijos_galiojimas = None
            self.kaina = self.original_kaina
        else:
            # Apply discount if it's valid
            if self.akcija is not None and self.akcija > 0:
                self.kaina = round(self.original_kaina * (1 - self.akcija / 100), 2)
            else:
                # If no discount, reset the price to the original
                self.kaina = self.original_kaina

        super().save(*args, **kwargs)
    
    
    
class Krepselis(models.Model):
    id_Krepselis = models.AutoField(primary_key=True)  # Explicitly define the primary key
    bendra_kaina = models.FloatField()
    kiekis = models.IntegerField()
    PVM = models.FloatField()
    uzsakymo_data = models.DateField()
    planuojama_pristatymo_data = models.DateField()
    uzsakymo_busena = models.CharField(max_length=255)
    sekimo_numeris = models.CharField(max_length=255)
    gavejo_adresas = models.CharField(max_length=255)
    issiuntimo_data = models.DateField()
    gavimo_data = models.DateField()
    valiuta = models.CharField(
        max_length=7,
        choices=[
            ('euras', 'Euras'),
            ('doleris', 'Doleris'),
            ('svaras', 'Svaras'),
        ]
    )
    fk_Vartotojas = models.ForeignKey('Vartotojas', on_delete=models.CASCADE, db_column='fk_Vartotojas')
    fk_Kurjeris = models.ForeignKey('Kurjeris', on_delete=models.CASCADE, db_column='fk_Kurjeris')

    class Meta:
        db_table = 'krepseliai'  # Maps to the existing SQL table

    def __str__(self):
        return f"Krepšelis #{self.id_Krepselis} ({self.valiuta})"





class Kurjerio_Knygos(models.Model):
    fk_Kurjeris = models.ForeignKey('Kurjeris', on_delete=models.CASCADE, db_column='fk_Kurjeris')
    fk_Sandelis = models.ForeignKey('Sandelis', on_delete=models.CASCADE, db_column='fk_Sandelis')

    class Meta:
        db_table = 'kurjerio_knygos'  # Maps to the existing SQL table
        constraints = [
            models.UniqueConstraint(fields=['fk_Kurjeris', 'fk_Sandelis'], name='unique_kurjeris_sandelis')
        ]

    def __str__(self):
        return f"Kurjeris ID: {self.fk_Kurjeris_id}, Sandelis ID: {self.fk_Sandelis_id}"




class Saskaita(models.Model):
    id_Saskaita = models.AutoField(primary_key=True)  # Explicitly define the primary key
    laikas = models.DateField()
    stadija = models.CharField(
        max_length=12,
        choices=[
            ('patvirtintas', 'Patvirtintas'),
            ('atšauktas', 'Atšauktas'),
            ('grąžintas', 'Grąžintas'),
            ('laukiama', 'Laukiama'),
        ]
    )
    fk_Krepselis = models.OneToOneField('Krepselis', on_delete=models.CASCADE, db_column='fk_Krepselis')

    class Meta:
        db_table = 'saskaitos'  # Maps to the existing SQL table

    def __str__(self):
        return f"Saskaita #{self.id_Saskaita} ({self.stadija})"
    
    
    
    
class KrepselioKnyga(models.Model):
    fk_Krepselis = models.ForeignKey('Krepselis', on_delete=models.CASCADE, db_column='fk_Krepselis')
    fk_Knyga = models.ForeignKey('Knyga', on_delete=models.CASCADE, db_column='fk_Knyga')

    class Meta:
        db_table = 'krepselio_knyga'  # Maps to the existing SQL table
        constraints = [
            models.UniqueConstraint(fields=['fk_Krepselis', 'fk_Knyga'], name='unique_krepselis_knyga')
        ]

    def __str__(self):
        return f"Krepšelis ID: {self.fk_Krepselis_id}, Knyga ID: {self.fk_Knyga_id}"
    
    
    
    

class SandelioKnygos(models.Model):
    fk_Sandelis = models.ForeignKey('Sandelis', on_delete=models.CASCADE, db_column='fk_Sandelis')
    fk_Knyga = models.ForeignKey('Knyga', on_delete=models.CASCADE, db_column='fk_Knyga')

    class Meta:
        db_table = 'sandelio_knygos'  # Maps to the existing SQL table
        constraints = [
            models.UniqueConstraint(fields=['fk_Sandelis', 'fk_Knyga'], name='unique_sandelis_knyga')
        ]

    def __str__(self):
        return f"Sandelis ID: {self.fk_Sandelis_id}, Knyga ID: {self.fk_Knyga_id}"
    
      
      
      
      
class UzsakymoKnygos(models.Model):
    fk_Knyga = models.ForeignKey('Knyga', on_delete=models.CASCADE, db_column='fk_Knyga')
    fk_Prekiu_uzsakymas = models.ForeignKey('PrekiuUzsakymas', on_delete=models.CASCADE, db_column='fk_Prekiu_uzsakymas')

    class Meta:
        db_table = 'uzsakymo_knygos'  # Maps to the existing SQL table
        constraints = [
            models.UniqueConstraint(fields=['fk_Knyga', 'fk_Prekiu_uzsakymas'], name='unique_knyga_uzsakymas')
        ]

    def __str__(self):
        return f"Knyga ID: {self.fk_Knyga_id}, Užsakymas ID: {self.fk_Prekiu_uzsakymas_id}"
    

    