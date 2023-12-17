from django.contrib import admin
from . import models as m

admin.site.register(m.Categoria)
admin.site.register(m.Contribuidor)
admin.site.register(m.Produto)