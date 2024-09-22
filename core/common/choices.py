from django.db import models
from django.utils.translation import gettext_lazy as _


class SkillLevel(models.IntegerChoices):
    BEGINNER = 1, _("Beginner")  # BEGINNER: 0-1 years
    INTERMEDIATE = 2, _("Intermediate")  # INTERMEDIATE: 1-3 years
    ADVANCED = 3, _("Advanced")  # ADVANCED: 3-5 years
    EXPERT = 4, _("Expert")  # EXPERT: 5-10 years
    MASTER = 5, _("Master")  # MASTER: 10+ years


class LanguageProficiencyLevel(models.IntegerChoices):
    BEGINNER = 1, _("Beginner")  # BEGINNER: Basic understanding
    ELEMENTARY = 2, _("Elementary")  # ELEMENTARY: Limited working proficiency
    INTERMEDIATE = 3, _(
        "Intermediate"
    )  # INTERMEDIATE: Professional working proficiency
    ADVANCED = 4, _("Advanced")  # ADVANCED: Full professional proficiency
    NATIVE = 5, _("Native")  # NATIVE: Native or bilingual proficiency
