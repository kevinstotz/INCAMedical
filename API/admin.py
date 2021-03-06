from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from API.models import CustomUser, Company, Address, AddressType, Audit, AuditArea, TemplateIndicator, Country, Note, \
    TemplateCategory, Category, City, EmailAddress, EmailAddressType, EmailAddressStatus, EmailTemplate, PhoneNumber, \
    EPAIndicator, MailServer, PersonName, NameType, Notification, NotificationType, NotificationStatus, Image, Role, \
    PhoneNumberType, IndicatorType, IndicatorOption, State, UserProfile, UserStatus, ZipCode, UploadType, Upload, \
    AuditIndicatorNote, AuditIndicatorOption, AuditIndicatorUpload, ClinicType, Indicator, NoteType, Permission, \
    SpecialtyType, TemplateIndicatorType, TemplateIndicatorOption


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
# Now register the new UserAdmin...


admin.site.register(CustomUser)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Address)
admin.site.register(AddressType)
admin.site.register(Audit)
admin.site.register(AuditArea)
admin.site.register(AuditIndicatorNote)
admin.site.register(AuditIndicatorOption)
admin.site.register(AuditIndicatorUpload)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(ClinicType)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(EmailAddress)
admin.site.register(EmailAddressStatus)
admin.site.register(EmailAddressType)
admin.site.register(EmailTemplate)
admin.site.register(EPAIndicator)
admin.site.register(Image)
admin.site.register(Indicator)
admin.site.register(IndicatorOption)
admin.site.register(IndicatorType)
admin.site.register(MailServer)
admin.site.register(NameType)
admin.site.register(Note)
admin.site.register(NoteType)
admin.site.register(Notification)
admin.site.register(NotificationStatus)
admin.site.register(NotificationType)
admin.site.register(Permission)
admin.site.register(PersonName)
admin.site.register(PhoneNumber)
admin.site.register(PhoneNumberType)
admin.site.register(Role)
admin.site.register(SpecialtyType)
admin.site.register(State)
admin.site.register(TemplateCategory)
admin.site.register(TemplateIndicator)
admin.site.register(TemplateIndicatorOption)
admin.site.register(TemplateIndicatorType)
admin.site.register(Upload)
admin.site.register(UploadType)
admin.site.register(UserProfile)
admin.site.register(UserStatus)
admin.site.register(ZipCode)
