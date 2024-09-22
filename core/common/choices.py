from django.db import models
from django.utils.translation import gettext_lazy as _


class SkillLevel(models.IntegerChoices):
    BEGINNER = 1, _("Beginner")  # BEGINNER: 0-1 years
    INTERMEDIATE = 2, _("Intermediate")  # INTERMEDIATE: 1-3 years
    ADVANCED = 3, _("Advanced")  # ADVANCED: 3-5 years
    EXPERT = 4, _("Expert")  # EXPERT: 5-10 years
    MASTER = 5, _("Master")  # MASTER: 10+ years
