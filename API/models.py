from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from API.settings.Globals import EMAIL_LENGTH, PASSWORD_LENGTH, AUDIT_AREA_NAME_LENGTH, UUID_ZERO, USER_STATUS, \
    ADDRESS_LENGTH, FIRST_NAME_LENGTH, EMAIL_TEMPLATE_DIR, COMPANY_NAME_LENGTH, SITE_ID_LENGTH, DEFAULT_USER, \
    NAME_TYPE


def validate_uuid(value):
    return value


class Index(models.Model):
    objects = models.Manager()

    def __str__(self):
        return '%s' % "HI"

    class Meta:
        ordering = ()


class ZipCode(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.CharField(max_length=5, default="00000", blank=False)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.zipcode

    class Meta:
        ordering = ('zipcode', )


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    sort_name = models.CharField(max_length=3, verbose_name="2 letter name", blank=False, default="XX")
    name = models.CharField(max_length=50, verbose_name="Country Name", blank=False, default="XXX")
    phone_code = models.IntegerField(default=0, blank=False)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.sort_name

    class Meta:
        ordering = ('sort_name', )


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, verbose_name="State Name", blank=False, default="XX")
    code = models.CharField(max_length=2, verbose_name="State Code", blank=False, default="XX")
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                default=1,
                                verbose_name="State Country",
                                related_name='stateCountry')
    zip_codes = models.ManyToManyField(ZipCode,
                                       default=1,
                                       related_name="statesZipCodes",
                                       verbose_name="State Zip Code", )

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name', )


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="City Name", blank=False)
    state = models.ForeignKey(State,
                              on_delete=models.PROTECT,
                              default=1,
                              verbose_name="State City",
                              related_name='cityState', )
    zip_codes = models.ManyToManyField(ZipCode,
                                       default=1,
                                       related_name="cityStates",
                                       verbose_name="City State", )

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name', )


class AddressType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Address Type Type", blank=False, default="1")
    active = models.BooleanField(default=True, verbose_name="Address Type Active")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    disabled = models.BooleanField(default=False, verbose_name="Address Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=255, verbose_name="Address 1", default="")
    address2 = models.CharField(max_length=255, verbose_name="Address 2", default="")
    address3 = models.CharField(max_length=255, verbose_name="Address 3", default="")
    unit = models.CharField(max_length=20, verbose_name="Unit", default="")
    type = models.ForeignKey(AddressType,
                             on_delete=models.CASCADE,
                             default=1,
                             related_name="addressType",
                             verbose_name="Address Type")
    zipcode = models.ForeignKey(ZipCode,
                                on_delete=models.PROTECT,
                                default=1,
                                related_name='addressZipcode',
                                verbose_name="Address Zip Code")
    city = models.ForeignKey(City,
                             on_delete=models.PROTECT,
                             default=1,
                             related_name='addressCity',
                             verbose_name="Address City")
    state = models.ForeignKey(State,
                              on_delete=models.PROTECT,
                              default=1,
                              related_name='addressState',
                              verbose_name="Address State")
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                default=1,
                                related_name='addressCountry',
                                verbose_name="Address Country")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Address Active")
    disabled = models.BooleanField(default=False, verbose_name="Address Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class NameType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Type of Name")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Name Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Name Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class PersonName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Person Name Name")
    type = models.ForeignKey(NameType,
                             on_delete=models.PROTECT,
                             verbose_name="Person Name Type",
                             default=1,
                             related_name='nameType')
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Person Name Active")
    disabled = models.BooleanField(default=False, verbose_name="Person Name Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', )


class NotificationType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Notification Type")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Notification Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Notification Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class NotificationStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Notification Status Status")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Notification Status Active")
    disabled = models.BooleanField(default=False, verbose_name="Notification Status Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id', )


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50, default="None", blank=False, unique=True, verbose_name="Role Type")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Role Active")
    disabled = models.BooleanField(default=False, verbose_name="Role Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Role Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Role Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, default="None", blank=False, unique=True, verbose_name="Permission Type")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Permission Active")
    disabled = models.BooleanField(default=False, verbose_name="Permission Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Permission Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Permission Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class EPAIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.CharField(max_length=255, blank=False, unique=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="EPA Indicator Active")
    disabled = models.BooleanField(default=False, verbose_name="EPA Indicator Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class PhoneNumberType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Phone Number Type Type", blank=False, default="1")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Phone Number Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Phone Number Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class PhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=16, default="0000000000", verbose_name="Phone Number")
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                verbose_name="Phone Number Country",
                                related_name='phoneNumberCountry',
                                default=1, )
    type = models.ForeignKey(PhoneNumberType,
                             verbose_name="Phone Number Country",
                             on_delete=models.PROTECT,
                             related_name='phoneNumberType',
                             default=1, )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Phone Number Active")
    disabled = models.BooleanField(default=False, verbose_name="Phone Number Active Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.phone_number

    class Meta:
        ordering = ('id', 'phone_number', 'country', )


class UserProfile(models.Model):
    first_name = models.ForeignKey(PersonName,
                                   on_delete=models.CASCADE,
                                   default=1,
                                   related_name="userProfileFirstName",
                                   verbose_name="User Profile First Name",
                                   )
    last_name = models.ForeignKey(PersonName,
                                  on_delete=models.CASCADE,
                                  default=1,
                                  related_name="userProfileLastName",
                                  verbose_name="User Profile Last Name",
                                  )
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="userProfileAddress",
                                verbose_name="User Profile Address",
                                )
    date_of_birth = models.CharField(max_length=50,
                                     blank=True,
                                     verbose_name="User Profile Date of Birth",
                                     unique=False,
                                     default="1970/01/01",
                                     )
    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             default=1,
                             related_name="userProfileRole",
                             verbose_name="User Profile Role")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="User Profile created")
    disabled = models.BooleanField(default=False, verbose_name="User Profile Disabled")

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.pk

    class Meta:
        ordering = ('id', )


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    site_id = models.CharField(max_length=SITE_ID_LENGTH, blank=True, verbose_name="Site ID Company")
    name = models.CharField(max_length=COMPANY_NAME_LENGTH, verbose_name="Name of Company")
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.CASCADE,
                                     default=1,
                                     verbose_name="Company User Profile",
                                     related_name="companyUserProfile", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Company Active")
    disabled = models.BooleanField(default=False, verbose_name="Company Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class NoteType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Note Type")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Note Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Note Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class IndicatorOption(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="indicatorOptionCompany",
                                verbose_name="Indicator Option Company", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Indicator Option created")
    active = models.BooleanField(default=True, verbose_name="Indicator Option Active")
    disabled = models.BooleanField(default=False, verbose_name="Indicator Option Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("company", "option")


class IndicatorType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="indicatorTypeCompany",
                                verbose_name="Indicator Type Company", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Indicator Type created")
    active = models.BooleanField(default=True, verbose_name="Indicator Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Indicator Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("company", "type")


class SpecialtyType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, verbose_name="Specialty Type of Company", blank=False, default="1")
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="specialtyType",
                                verbose_name="SpecialtyType Company", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Specialty Type created")
    active = models.BooleanField(default=True, verbose_name="Specialty Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Specialty Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="categoryCompany",
                                verbose_name="Category Company", )
    name = models.CharField(max_length=255, unique=True, blank=False)
    active = models.BooleanField(default=True, verbose_name="Category Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    disabled = models.BooleanField(default=False, verbose_name="Category Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name', )


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="", blank=True)
    uploaded_name = models.CharField(max_length=255, default="", blank=True)
    file = models.FileField(upload_to='images/', verbose_name="Image path", name="imagePath")
    size = models.IntegerField(default=0)
    active = models.BooleanField(default=True, verbose_name="Image Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    disabled = models.BooleanField(default=False, verbose_name="Image Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', )


class Indicators(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.CharField(max_length=255, default="None", blank=False)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 default=1,
                                 verbose_name="Indicator Category",
                                 related_name='indicatorCategory')
    subcategory = models.ForeignKey(Category,
                                    on_delete=models.PROTECT,
                                    default=1,
                                    verbose_name="Indicator Subcategory",
                                    related_name='indicatorSubcategory')
    active = models.BooleanField(default=True, verbose_name="Indicators Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    disabled = models.BooleanField(default=False, verbose_name="Indicators Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.indicator

    class Meta:
        ordering = ('id', )


class Indicator(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=50, default="None", blank=True)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="indicatorCompany",
                                verbose_name="Indicator Company", )
    type = models.ForeignKey(IndicatorType,
                             on_delete=models.CASCADE,
                             related_name="indicatorType",
                             default=1,
                             verbose_name="Indicator Type", )
    options = models.ManyToManyField(IndicatorOption, related_name='indicatorOptions')
    images = models.ManyToManyField(Image, related_name='indicatorImages')
    name = models.TextField(max_length=2000)
    active = models.BooleanField(default=True, verbose_name="Indicator Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    disabled = models.BooleanField(default=False, verbose_name="Indicator Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', )


class ClinicType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, verbose_name="Type of Clinic", blank=False, default="1")
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="clinicTypeCompany",
                                verbose_name="Clinic Type Company", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Clinic Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Clinic Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class AuditArea(models.Model):
    id = models.AutoField(primary_key=True),
    name = models.CharField(max_length=AUDIT_AREA_NAME_LENGTH, verbose_name="Name of Area", blank=False)
    clinic_type = models.ForeignKey(ClinicType,
                                    on_delete=models.CASCADE,
                                    default=1,
                                    related_name="auditAreaClinicType",
                                    verbose_name="Audit Area Clinic Type", )
    specialty_type = models.ForeignKey(SpecialtyType,
                                       on_delete=models.CASCADE,
                                       default=1,
                                       related_name="auditAreaSpecialtyType",
                                       verbose_name="Audit Area Specialty Type", )
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="auditAreaCompany",
                                verbose_name="Audit Area Company", )
    director = models.ForeignKey(PersonName,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="auditAreaDirector",
                                 verbose_name="Audit Area Director", )
    manager = models.ForeignKey(PersonName,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="auditAreaManager",
                                verbose_name="Audit Company Manager", )
    phone = models.ForeignKey(PhoneNumber,
                              on_delete=models.CASCADE,
                              default=1,
                              related_name="auditAreaPhoneNumber",
                              verbose_name="Audit Area Phone Number", )
    present_on_rounds = models.CharField(max_length=100, blank=True, unique=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Audit Area Active")
    disabled = models.BooleanField(default=False, verbose_name="Audit Area Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        unique_together = ("company", "name")
        ordering = ('id', )


class MailServer(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=255, blank=False, verbose_name="vendor name", default="No Name")
    username = models.CharField(max_length=EMAIL_LENGTH, blank=False, verbose_name="username", default="No Name")
    password = models.CharField(max_length=PASSWORD_LENGTH, blank=False, verbose_name="password", default="No Name")
    server = models.CharField(max_length=255, blank=False, verbose_name="server name", default="No Name")
    port = models.IntegerField(blank=False, default=465)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=False, verbose_name="Active Mail Server")
    disabled = models.BooleanField(default=False, verbose_name="Mail Server Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.vendor

    class Meta:
        ordering = ('vendor', )


class UserStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=ADDRESS_LENGTH, verbose_name="Status of User")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="User Status Active")
    disabled = models.BooleanField(default=False, verbose_name="User Status Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id', )


class CustomUserManager(BaseUserManager):

    def create_user(self, email, status=USER_STATUS['ACTIVE'], password=None, firstname="", lastname=""):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email)
        )
        first_name = PersonName(name=firstname, type=NameType.objects.get(pk=NAME_TYPE['FIRST']))
        first_name.save()
        last_name = PersonName(name=lastname, type=NameType.objects.get(pk=NAME_TYPE['LAST']))
        last_name.save()
        user_profile = UserProfile(first_name=first_name, last_name=last_name)
        user_profile.save()
        user.user_profile = user_profile
        user.status = UserStatus.objects.get(pk=status)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, status=USER_STATUS['ACTIVE'], password=None, firstname="", lastname=""):

        user = self.create_user(
            email,
            password=password,
            status=status,
            firstname=firstname,
            lastname=lastname
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class EmailAddressStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Status of Email Address")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Email Address Status Active")
    disabled = models.BooleanField(default=False, verbose_name="Email Address Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id', )


class EmailTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=60, verbose_name="Subject of Email Template")
    from_address = models.CharField(max_length=50, verbose_name="Email Template From Address")
    html = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                            max_length=100,
                            blank=True,
                            null=True,
                            verbose_name="Email Template HTML Filename")
    text = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                            max_length=100,
                            blank=True,
                            null=True,
                            verbose_name="Email Template Text Filename")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Email Template Active")
    disabled = models.BooleanField(default=False, verbose_name="Email Template Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Email Template Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Email Template Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.subject

    class Meta:
        ordering = ('id', )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              verbose_name="Login of user",
                              unique=True, )
    username = models.CharField(max_length=EMAIL_LENGTH,
                                blank=False,
                                verbose_name="username of user",
                                unique=True,
                                default="Username", )

    status = models.ForeignKey(UserStatus,
                               on_delete=models.CASCADE,
                               default=1,
                               verbose_name="Customer User Status",
                               related_name="customUserStatus", )
    user_profile = models.OneToOneField(UserProfile,
                                        on_delete=models.CASCADE,
                                        default=1,
                                        verbose_name="Custom User User Profile",
                                        related_name="customUserUserProfile", )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    is_active = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '%s' % self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    @staticmethod
    def get_full_name(self):
        self.full_name = '%s %s' % ("first", "last")
        return self.full_name.strip()

    @staticmethod
    def get_short_name():
        return "first"


class EmailAddressType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Email Address Type", blank=False, default="1")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Email Address Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Email Sddress Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class EmailAddress(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email Address of Register")
    type = models.ForeignKey(EmailAddressType, on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,
                                        on_delete=models.CASCADE,
                                        default=1,
                                        verbose_name="Email Address Custom User Profile",
                                        related_name="emailAddressCustomUserProfile", )
    status = models.ForeignKey(EmailAddressStatus, on_delete=models.PROTECT, default=1)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Email Address Active")
    disabled = models.BooleanField(default=False, verbose_name="Email Address Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.email

    class Meta:
        ordering = ('id', )


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="templateCompany",
                                verbose_name="Template Company", )
    indicators = models.ManyToManyField(Indicator, through='TemplateIndicator', related_name='templateIndicators')
    categories = models.ManyToManyField(Category, through='TemplateCategory', related_name='templateCategories')
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Template Active")
    disabled = models.BooleanField(default=False, verbose_name="Template Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("company", "name", )


class TemplateIndicatorType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Template Indicator Type created")
    active = models.BooleanField(default=True, verbose_name="Template Indicator Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Template Indicator Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note = models.TextField(max_length=2000)
    fromUser = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="noteFromUser",
                                 verbose_name="Note From User", )
    type = models.ForeignKey(NoteType,
                             on_delete=models.SET_DEFAULT,
                             default=1,
                             related_name="noteType",
                             verbose_name="Note Type", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Note Type")
    disabled = models.BooleanField(default=False, verbose_name="Note Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class UploadType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Upload Type", blank=False, default="1")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Upload Type Active")
    disabled = models.BooleanField(default=False, verbose_name="Upload Type Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', )


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="", blank=True)
    uploaded_name = models.CharField(max_length=255, default="", blank=True)
    file = models.FileField(upload_to='images/', verbose_name="Upload path", name="uploadPath")
    size = models.IntegerField(default=0, verbose_name="Upload Size")
    fromUser = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="uploadFromUser",
                                 verbose_name="Upload From User", )
    type = models.ForeignKey(UploadType,
                             on_delete=models.SET_DEFAULT,
                             default=1,
                             related_name="uploadType",
                             verbose_name="Upload Type")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Upload Active")
    disabled = models.BooleanField(default=False, verbose_name="Upload Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class TemplateIndicatorOption(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=50, blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Template Indicator Option created")
    active = models.BooleanField(default=True, verbose_name="Template Indicator Option Active")
    disabled = models.BooleanField(default=False, verbose_name="Template Indicator Option Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class TemplateIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(primary_key=False,
                            default=uuid.uuid4,
                            unique=True,
                            editable=True)
    level = models.IntegerField(default=0, blank=False)
    position = models.IntegerField(default=0, blank=False)
    parent = models.UUIDField(primary_key=False,
                              default=UUID_ZERO,
                              unique=False,
                              editable=True)
    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="templateIndicatorTemplate",
                                 verbose_name="Template Indicator Template")
    indicator_source = models.ForeignKey(Indicator,
                                         on_delete=models.CASCADE,
                                         related_name="templateIndicatorIndicatorSource",
                                         default=1,
                                         verbose_name="Template Indicator Indicator Source")
    name = models.TextField(max_length=2000)
    indicator_type = models.ForeignKey(TemplateIndicatorType,
                                       on_delete=models.CASCADE,
                                       default=1,
                                       related_name="templateIndicatorType",
                                       verbose_name="Template Indicator Type")
    indicator_options = models.ManyToManyField(TemplateIndicatorOption,
                                               verbose_name="Template Indicator Options",
                                               related_name='templateIndicatorOptions')
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Template Indicator Active")
    disabled = models.BooleanField(default=False, verbose_name="Template Indicator Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class TemplateCategory(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
                            primary_key=False,
                            default=uuid.uuid4,
                            unique=True,
                            editable=True)
    level = models.IntegerField(default=0, blank=False)
    position = models.IntegerField(default=0, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    parent = models.UUIDField(
                              primary_key=False,
                              default=UUID_ZERO,
                              unique=False,
                              editable=True)
    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="templateCategoryTemplate",
                                 verbose_name="Template Category Template", )
    category_source = models.ForeignKey(Category,
                                        on_delete=models.CASCADE,
                                        related_name="templateCategoryCategorySource",
                                        default=1,
                                        verbose_name="Template Category Category Source", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Template Category Active")
    disabled = models.BooleanField(default=False, verbose_name="Template Category Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )


class Audit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="", blank=True)
    area = models.ForeignKey(AuditArea,
                             on_delete=models.CASCADE,
                             default=1,
                             related_name="auditArea",
                             verbose_name="Audit Area", )
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                default=1,
                                related_name="auditCompany",
                                verbose_name="Audit Company", )
    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="auditTemplate",
                                 verbose_name="Audit Template", )

    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Audit Active")
    disabled = models.BooleanField(default=False, verbose_name="Audit Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', )


class AuditIndicatorUpload(models.Model):
    id = models.AutoField(primary_key=True)
    audit = models.ForeignKey(Audit,
                              on_delete=models.CASCADE,
                              default=1,
                              related_name="auditIndicatorUploadAudit",
                              verbose_name="Audit Indicator Upload Audit")
    indicator = models.ForeignKey(TemplateIndicator,
                                  on_delete=models.CASCADE,
                                  default=1,
                                  related_name="auditIndicatorUploadIndicator",
                                  verbose_name="Audit Indicator Upload Indicator")
    upload = models.ForeignKey(Upload,
                               on_delete=models.CASCADE,
                               default=1,
                               related_name="auditIndicatorUploadOption",
                               verbose_name="Audit Indicator Upload Option")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Audit Indicator Upload created")
    active = models.BooleanField(default=True, verbose_name="Audit Indicator Upload Active")
    disabled = models.BooleanField(default=False, verbose_name="Audit Indicator Upload Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("indicator", "audit", "upload", )


class AuditIndicatorNote(models.Model):
    id = models.AutoField(primary_key=True)
    audit = models.ForeignKey(Audit,
                              on_delete=models.CASCADE,
                              default=1,
                              related_name="auditIndicatoNoteAudit",
                              verbose_name="Audit Indicator Note Audit")
    indicator = models.ForeignKey(TemplateIndicator,
                                  on_delete=models.CASCADE,
                                  default=1,
                                  related_name="auditIndicatorNoteIndicator",
                                  verbose_name="Audit Indicator Note Indicator")
    note = models.ForeignKey(Note,
                             on_delete=models.CASCADE,
                             default=1,
                             related_name="auditIndicatorNoteNote",
                             verbose_name="Audit Indicator Note Note")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Audit Indicator Note created")
    active = models.BooleanField(default=True, verbose_name="Audit Indicator Note Active")
    disabled = models.BooleanField(default=False, verbose_name="Audit Indicator Note Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("indicator", "audit", "note", )


class AuditIndicatorOption(models.Model):
    id = models.AutoField(primary_key=True)
    audit = models.ForeignKey(Audit,
                              on_delete=models.CASCADE,
                              default=1,
                              related_name="auditIndicatorOptionAudit",
                              verbose_name="Audit Indicator Option Audit")
    indicator = models.ForeignKey(TemplateIndicator,
                                  on_delete=models.CASCADE,
                                  default=1,
                                  related_name="auditIndicatorOptionIndicator",
                                  verbose_name="Audit Indicator Option Indicator")
    option = models.ForeignKey(TemplateIndicatorOption,
                               on_delete=models.CASCADE,
                               default=1,
                               related_name="auditIndicatorOptionOption",
                               verbose_name="Audit Indicator Option Option")
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Audit Indicator Option created")
    active = models.BooleanField(default=True, verbose_name="Audit Indicator Option Active")
    disabled = models.BooleanField(default=False, verbose_name="Audit Indicator Option Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
        unique_together = ("indicator", "audit")


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(NotificationType,
                             on_delete=models.SET_DEFAULT,
                             default=1,
                             related_name="notificationType",
                             verbose_name="Notification Type",
                             )
    fromUser = models.ForeignKey(CustomUser,
                                 on_delete=models.SET_DEFAULT,
                                 default=1,
                                 related_name="notificationFromUser",
                                 verbose_name="Notification From User", )
    toUser = models.IntegerField(default=0)
    status = models.ForeignKey(NotificationStatus,
                               on_delete=models.SET_DEFAULT,
                               default=1,
                               related_name="notificationStatus",
                               verbose_name="Notification Status", )
    updated = models.DateTimeField(auto_now=True, verbose_name="Time Updated")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time created")
    active = models.BooleanField(default=True, verbose_name="Notification Active")
    disabled = models.BooleanField(default=False, verbose_name="Notification Disabled")
    creator = models.IntegerField(default=DEFAULT_USER,
                                  verbose_name="Address Type Creator",
                                  blank=False)
    owner = models.IntegerField(default=DEFAULT_USER,
                                verbose_name="Address Type Owner",
                                blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id', )
