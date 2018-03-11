from app02 import models
from CURDService.CURDCore import core_func

core_func.site.register(models.School, core_func.BaseCurdAdmin)
