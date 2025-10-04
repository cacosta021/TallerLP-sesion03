import uuid
from django.db import models
from pos_project_acosta.choices import EstadoEntidades

# Create your models here.
class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_grupo = models.CharField(max_length=5, null=False)
    nombre_grupo = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "grupos_articulos"
        ordering = ["codigo_grupo"]

    def __str__(self):
        return self.nombre_grupo

class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "lineas_articulo"
        ordering = ["codigo_linea"]

    def __str__(self):
        return self.nombre_linea

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_articulo = models.CharField(max_length=30, unique=True)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=200, null=False)
    presentacion = models.CharField(max_length=100, null=True, blank=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=True, blank=True)
    linea = models.ForeignKey(LineaArticulo, on_delete=models.RESTRICT, null=True, blank=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "articulos"
        ordering = ["descripcion"]

    def __str__(self):
        return f"{self.codigo_articulo} - {self.descripcion}"
    
class ListaPrecio(models.Model):
    lista_precio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='precios')
    precio_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_4 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = "listas_precios"
        ordering = ["-lista_precio_id"]

    def __str__(self):
        return f"{self.articulo.descripcion} - P1: {self.precio_1}"