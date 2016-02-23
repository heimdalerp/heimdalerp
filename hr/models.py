from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as _noop

from persons.models import PersonProfile, GENRE_TYPES, Company


class Ethnicity(models.Model):
    """
    Ethnicity types. Relevant for countries were one must comply with a 
    minimum quota of diversity.
    """
    name = models.CharField(
        _('name'),
        max_length=30,
        help_text=_("i.e. Italic, Hispanic, Black, Arabic, White, Latin"),
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    
    def __str__(self):
        return _noop('%(name)s') % {'name': self.name}

    class Meta:
        verbose_name = _('ethnicity')
        verbose_name_plural = _('ethnicities')
        default_permissions = ('view', 'add', 'change', 'delete')


class SexualOrientation(models.Model):
    """
    Sexual orientation types. Relevant for countries were one must comply 
    with a minimum quota of social inclusion.
    """
    name = models.CharField(
        _('name'),
        max_length=30,
        help_text=_("i.e. Straight, Homosexual, Pansexual, Transexual"),
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop('%(name)s') % {'name': self.name}

    class Meta:
        verbose_name = _('sexual orientation')
        verbose_name_plural = _('sexual orientations')
        default_permissions = ('view', 'add', 'change', 'delete')


class Aptitude(models.Model):
    """
    An aptitude, contrary to an achievement is an ability, skill, knowledge
    experience and or capacity that an employee has. These are generic. 
    For example, Steve has knowledge and experience with project management.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    description = models.CharField(
        _('description'),
        max_length=150,
        default=""
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop('%(name)s') % {'name': self.name}

    class Meta:
        verbose_name = _('aptitude')
        verbose_name_plural = _('aptitudes')
        default_permissions = ('view', 'add', 'change', 'delete')


class Achievement(models.Model):
    """
    An achievement is a one-time accomplished task, shouldn't be something 
    generic.
    For example, John's design got awarded at Current Year Design Awards.
    Or, Jessica finished her project 3 months earlier than expected.
    """
    description = models.TextField(
        _('description'),
        help_text=_("A single-time achievement; "
                    "i.e. Jessica finished her project 3 months earlier")
    )
    when_it_happened = models.DateField(
        _('when it happened'),
        help_text=_("Not necessarily the current date."),
        blank=True,
        null=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop('%(description)s') % {'description': self.description}

    class Meta:
        verbose_name = _('achievement')
        verbose_name_plural = _('achievements')
        default_permissions = ('view', 'add', 'change', 'delete')


class Sanction(models.Model):
    """
    A sanction is a type of misbehaviour that isn't allowed in employees. 
    For example: sexual harassment, verbal violence, physical violence, etc.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    description = models.CharField(
        _('description'),
        max_length=250,
        help_text=_("A brief explanation of what consists of."),
        default=""
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text=_("Enter points greater than zero here, but they'll be "
                    "sustracted rather than added from the total.")
    )

    def __str__(self):
        return _noop('%(description)s') % {'description': self.description}

    class Meta:
        verbose_name = _('sanction type')
        verbose_name_plural = _('sanction types')
        default_permissions = ('view', 'add', 'change', 'delete')


class Degree(models.Model):
    """
    Degrees. Highschool degrees, college degrees, etc.
    Examples: Computer Science, Civil Engineer, Lawyer.
    """
    name = models.CharField(
        _('name'),
        max_length=30,
        help_text=_("i.e. Lawyer, Accountant, Civil Engineer"),
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
   
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('degree')
        verbose_name_plural = _('degrees')
        default_permissions = ('view', 'add', 'change', 'delete')


class Language(models.Model):
    """
    Languages that employees can speak.
    """
    name = models.CharField(
        _('name'),
        max_length=30,
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop('%(name)s') % {'name': self.name}

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        default_permissions = ('view', 'add', 'change', 'delete')


class Employee(PersonProfile):
    """
    All Employees must have a User, whereas they'll use the system or not.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user')
    )
    genre = models.CharField(
        _('genre'),
        max_length=1,
        choices=GENRE_TYPES,
    )
    ethnicities = models.ManyToManyField(
        Ethnicity,
        blank=True,
        verbose_name=_('ethnicities'),
        related_name='ethnicities',
        related_query_name='ethnicity',
        help_text=_('Relevant for countries where one must comply quotas')
    )
    sexual_orientation = models.ForeignKey(
        SexualOrientation,
        blank=True,
        null=True,
        related_name='sexual_orientations',
        related_query_name='sexual_orientation',
        verbose_name=_('sexual orientation'),
        help_text=_('Relevant for countries where one must comply quotas')
    )
    aptitudes = models.ManyToManyField(
        Aptitude,
        verbose_name=_('aptitudes'),
        related_name='aptitudes',
        related_query_name='aptitude',
        blank=True
    )
    achievements = models.ManyToManyField(
        Achievement,
        verbose_name=_('achievements'),
        related_name='achievements',
        related_query_name='achievement',
        blank=True
    )
    sanctions = models.ManyToManyField(
        Sanction,
        verbose_name=_('sanctions'),
        related_name='sanctions',
        related_query_name='sanction',
        through='EmployeeHasSanction',
        through_fields=('employee', 'sanction'),
        blank=True
    )
    degree = models.ManyToManyField(
        Degree,
        verbose_name=_('degrees'),
        related_name='degrees',
        related_query_name='degree',
        through='EmployeeHasDegree',
        through_fields=('employee', 'degree'),
        blank=True
    )
    languages = models.ManyToManyField(
        Language,
        verbose_name=_('languages'),
        related_name='languages',
        related_query_name='language',
        through='EmployeeSpeaksLanguage',
        through_fields=('employee', 'language'),
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        default_permissions = ('view', 'add', 'change', 'delete')


LANGUAGE_SPOKENLEVEL_BASIC = 'B'
LANGUAGE_SPOKENLEVEL_MEDIUM = 'M'
LANGUAGE_SPOKENLEVEL_ADVANCED = 'A'
LANGUAGE_SPOKENLEVEL_NATIVE = 'N'
LANGUAGE_SPOKEN_LEVELS = (
    (LANGUAGE_SPOKENLEVEL_BASIC, _('Basic')),
    (LANGUAGE_SPOKENLEVEL_MEDIUM, _('Medium')),
    (LANGUAGE_SPOKENLEVEL_ADVANCED, _('Advanced')),
    (LANGUAGE_SPOKENLEVEL_NATIVE, _('Native'))
)

class EmployeeSpeaksLanguage(models.Model):
    """
    Employee speaks a language with a certain level.
    """
    employee = models.ForeignKey(
        Employee,
        related_name='employees',
        related_query_name='employee',
        verbose_name=_('employee')
    )
    language = models.ForeignKey(
        Language,
        related_name='languages',
        related_query_name='language',
        verbose_name=_('language')
    )
    level = models.CharField(
        _('level'),
        max_length=1,
        choices=LANGUAGE_SPOKEN_LEVELS,
        default=""
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text=_("Points should be proportional to the level spoken.")
    )

    def __str__(self):
        r = _noop(
            '%(employee)s speaks %(language)s'
        ) % {'employee': self.employee, 'language': self.language}
        return r 

    class Meta:
        verbose_name = _('employee speaks language')
        verbose_name_plural = _('employee speaks languages')
        default_permissions = ('view', 'add', 'change', 'delete')


class EmployeeHasSanction(models.Model):
    """
    An employee has been sanctioned for misbehaviour.
    """
    employee = models.ForeignKey(
        Employee,
        related_name='employees',
        related_query_name='employee',
        verbose_name=_('employee')
    )
    sanction = models.ForeignKey(
        Sanction,
        related_name='sanctions',
        related_query_name='sanction',
        verbose_name=_('sanction')
    )
    what_happened = models.TextField(
        _('what happened'),
        default=""
    )
    when_it_happened = models.DateTimeField(
        _('when it happened'),
        help_text=_("Not necessarily the current date")
    )
    others_implicated = models.ManyToManyField(
        Employee,
        related_name='others_implicated',
        related_query_name='other_implicated',
        verbose_name=_('others implicated'),
        blank=True
    )
    victims = models.ManyToManyField(
        Employee,
        related_name='victims',
        related_query_name='victim',
        verbose_name=_('victims'),
        blank=True
    )

    def __str__(self):
        r = _noop(
            '%(degree)s at %(academia)s'
        ) % {'degree': self.degree, 'academia': self.academic_institution}
        return r 

    class Meta:
        verbose_name = _('employee has degree')
        verbose_name_plural = _('employees have degrees')
        default_permissions = ('view', 'add', 'change', 'delete')


class AcademicInstitution(models.Model):
    """
    Academic Institution for later use in combination with Degree.
    """
    name = models.CharField(
        _('academic institution'),
        max_length=150,
        help_text=_("i.e. Cambridge University"),
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('academic institution')
        verbose_name_plural = _('academic institutions')
        default_permissions = ('view', 'add', 'change', 'delete')


class EmployeeHasDegree(models.Model):
    """
    An employee has a certain degree from an academic institution.
    """
    employee = models.ForeignKey(
        Employee,
        related_name='employees',
        related_query_name='employee',
        verbose_name=_('employee')
    )
    degree = models.ForeignKey(
        Degree,
        related_name='degrees',
        related_query_name='degree',
        verbose_name=_('degree')
    )
    academic_institution = models.ForeignKey(
        AcademicInstitution,
        related_name='academic_institutions',
        related_query_name='academic_institution',
        verbose_name=_('academic institution')
    )
    ingress_year = models.PositiveSmallIntegerField(
        _('ingress year'),
        blank=True,
        null=True
    )
    egress_year = models.PositiveSmallIntegerField(
        _('egress year'),
        blank=True,
        null=True
    )

    def __str__(self):
        r = _noop(
            '%(degree)s at %(academia)s'
        ) % {'degree': self.degree, 'academia': self.academic_institution}
        return r 

    class Meta:
        verbose_name = _('employee has degree')
        verbose_name_plural = _('employees have degrees')
        default_permissions = ('view', 'add', 'change', 'delete')


class Role(models.Model):
    """
    An employee has one or more roles in one or more companies.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop("%(name)s") % {'name': self.name}

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        default_permissions = ('view', 'add', 'change', 'delete')


class Area(models.Model):
    """
    A company has one o more areas where employees have roles.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    points = models.DecimalField(
        _('points'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return _noop("%(name)s") % {'name': self.name}


class CompanyHasEmployee(models.Model):
    """
    Employees are employed in one or more companies.
    """
    company = models.ForeignKey(
        Company,
        related_name='companies',
        related_query_name='company',
        verbose_name=_('company')
    )
    employee = models.ForeignKey(
        Employee,
        related_name='employees',
        related_query_name='employee',
        verbose_name=_('employee')
    )
    areas = models.ManyToManyField(
        Area,
        related_name='areas',
        related_query_name='area',
        verbose_name=_('areas'),
        through='AreaHasEmployee',
        through_fields=('area', 'employee'),
        blank=True
    )
    date_since = models.DateField(
        _('date since'),
        blank=True,
        null=True
    )

    def __str__(self):
        return "%(employee)s @ %(company)s" % {
            'employee': self.employee,
            'company': self.company
        }

    class Meta:
        unique_together = (('company', 'employee'),)
        verbose_name = _('company has employee')
        verbose_name_plural = _('company has employees')
        default_permissions = ('view', 'add', 'change', 'delete')


class AreaHasEmployee(models.Model):
    """
    Employees perform roles in areas of the company.
    """
    area = models.ForeignKey(
        Area,
        verbose_name=_('area'),
        related_name='areas',
        related_query_name='area'
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name=_('employee'),
        related_name='employees',
        related_query_name='employee'
    )
    date_since = models.DateField(
        _('date since'),
        blank=True,
        null=True
    )
    roles = models.ManyToManyField(
        Role,
        related_name='roles',
        related_query_name='role',
        verbose_name=_('roles'),
        through='EmployeeHasRole',
        through_fields=('employee', 'role'),
        blank=True
    )

    def __str__(self):
        return "%(employee)s @ %(area)s" % {
            'employee': self.employee,
            'area': self.area
    }

    class Meta:
        verbose_name = _('area has employee')
        verbose_name_plural = _('area has employees')
        default_permissions = ('view', 'add', 'change', 'delete')


class EmployeeHasRole(models.Model):
    """
    Employees perform roles in areas of the company.
    """
    role = models.ForeignKey(
        Role,
        related_name='roles',
        related_query_name='role',
        verbose_name=_('roles'),
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name=_('employee'),
        related_name='employees',
        related_query_name='employee'
    )
    date_since = models.DateField(
        _('date since'),
        blank=True,
        null=True
    )

    def __str__(self):
        return "%(employee)s is %(role)s" % {
            'employee': self.employee,
            'role': self.role
        }

    class Meta:
        verbose_name = _('employee has role')
        verbose_name_plural = _('employee has roles')
        default_permissions = ('view', 'add', 'change', 'delete')

