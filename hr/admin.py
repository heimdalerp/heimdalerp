from django.contrib import admin

from reversion.admin import VersionAdmin

from hr import models


class EthnicityAdmin(VersionAdmin):
    pass


class SexualOrientationAdmin(VersionAdmin):
    pass


class AptitudeAdmin(VersionAdmin):
    pass


class AchievementAdmin(VersionAdmin):
    pass


class SanctionAdmin(VersionAdmin):
    pass


class EmployeeAdmin(VersionAdmin):
    pass


class LanguageAdmin(VersionAdmin):
    pass


class EmployeeSpeaksLanguageAdmin(VersionAdmin):
    pass


class EmployeeHasSanctionAdmin(VersionAdmin):
    pass


class AcademicInstitutionAdmin(VersionAdmin):
    pass


class DegreeAdmin(VersionAdmin):
    pass


class EmployeeHasDegreeAdmin(VersionAdmin):
    pass


class RoleAdmin(VersionAdmin):
    pass


class AreaAdmin(VersionAdmin):
    pass


class AreaHasEmployeeAdmin(VersionAdmin):
    pass


class EmployeeHasRoleAdmin(VersionAdmin):
    pass


admin.site.register(models.Ethnicity, EthnicityAdmin)
admin.site.register(models.SexualOrientation, SexualOrientationAdmin)
admin.site.register(models.Aptitude, AptitudeAdmin)
admin.site.register(models.Achievement, AchievementAdmin)
admin.site.register(models.Sanction, SanctionAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(
    models.EmployeeSpeaksLanguage,
    EmployeeSpeaksLanguageAdmin
)
admin.site.register(models.EmployeeHasSanction, EmployeeHasSanctionAdmin)
admin.site.register(models.AcademicInstitution, AcademicInstitutionAdmin)
admin.site.register(models.Degree, DegreeAdmin)
admin.site.register(models.EmployeeHasDegree, EmployeeHasDegreeAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.AreaHasEmployee, AreaHasEmployeeAdmin)
admin.site.register(models.EmployeeHasRole, EmployeeHasRoleAdmin)
