from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as _noop

from persons.models import PersonProfile, GENRE_TYPES


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
    member_since = models.DateField(
        _('member since'),
        blank=True,
        null=True
    )
    ethnicities = models.ManyToManyField(
        Ethnicity,
        blank=True,
        verbose_name=_('ethnicities'),
        related_name='ethnicities',
        help_text=_('Relevant for countries where one must comply quotas')
    )
    sexual_orientation = models.ForeignKey(
        SexualOrientation,
        blank=True,
        null=True,
        verbose_name=_('sexual orientation'),
        help_text=_('Relevant for countries where one must comply quotas')
    )
    aptitudes = models.ManyToManyField(
        Aptitude,
        verbose_name=_('aptitudes'),
        related_name='aptitudes',
        blank=True
    )
    achievements = models.ManyToManyField(
        Achievement,
        verbose_name=_('achievements'),
        related_name='achievements',
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
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
        verbose_name=_('employee')
    )
    language = models.ForeignKey(
        Language,
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
        verbose_name=_('employee')
    )
    sanction = models.ForeignKey(
        Sanction,
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
        related_name='implicated',
        verbose_name=_('others implicated'),
        blank=True
    )
    victims = models.ManyToManyField(
        Employee,
        related_name='victims',
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


class EmployeeHasDegree(models.Model):
    """
    An employee has a certain degree from an academic institution.
    """
    employee = models.ForeignKey(
        Employee,
        verbose_name=_('employee')
    )
    degree = models.ForeignKey(
        Degree,
        verbose_name=_('degree')
    )
    academic_institution = models.ForeignKey(
        AcademicInstitution,
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

