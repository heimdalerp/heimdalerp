from django.contrib import admin
from hr import models
from reversion.admin import VersionAdmin


@admin.register(models.Ethnicity)
class EthnicityAdmin(VersionAdmin):
    pass


@admin.register(models.SexualOrientation)
class SexualOrientationAdmin(VersionAdmin):
    pass


@admin.register(models.Aptitude)
class AptitudeAdmin(VersionAdmin):
    pass


@admin.register(models.Achievement)
class AchievementAdmin(VersionAdmin):
    pass


@admin.register(models.Sanction)
class SanctionAdmin(VersionAdmin):
    pass


@admin.register(models.Employee)
class EmployeeAdmin(VersionAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(VersionAdmin):
    pass


@admin.register(models.EmployeeSpeaksLanguage)
class EmployeeSpeaksLanguageAdmin(VersionAdmin):
    pass


@admin.register(models.EmployeeHasSanction)
class EmployeeHasSanctionAdmin(VersionAdmin):
    pass


@admin.register(models.AcademicInstitution)
class AcademicInstitutionAdmin(VersionAdmin):
    pass


@admin.register(models.Degree)
class DegreeAdmin(VersionAdmin):
    pass


@admin.register(models.EmployeeHasDegree)
class EmployeeHasDegreeAdmin(VersionAdmin):
    pass


@admin.register(models.Role)
class RoleAdmin(VersionAdmin):
    pass


@admin.register(models.Area)
class AreaAdmin(VersionAdmin):
    pass


@admin.register(models.AreaHasEmployee)
class AreaHasEmployeeAdmin(VersionAdmin):
    pass


@admin.register(models.EmployeeHasRole)
class EmployeeHasRoleAdmin(VersionAdmin):
    pass
