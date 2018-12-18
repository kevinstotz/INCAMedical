import logging
from API.settings.Globals import UUID_ZERO, TEMPLATE_COMPANY
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField, PrimaryKeyRelatedField
from API.models import Company, AuditArea, TemplateIndicator, TemplateCategory, Audit, Image, Upload, \
    CustomUser, PersonName, NameType, PhoneNumber, PhoneNumberType, UserProfile, Index, Note, NoteType, \
    Country, ClinicType, SpecialtyType, Template, Category, Indicator, IndicatorOption, IndicatorType, UploadType, \
    TemplateIndicatorOption, TemplateIndicatorType, AuditIndicatorOption, AuditIndicatorUpload, AuditIndicatorNote
from django.core.files.storage import FileSystemStorage
from django.db.models import Count

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class IndexSerializer(ModelSerializer):

    class Meta:
        model = Index
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    short_name = SerializerMethodField()

    class Meta:
        model = Category
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', 'short_name', 'company', 'active', )

    def create(self, validated_data):
        return Category.objects.create(short_name="", **validated_data)

    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def get_short_name(self, instance):
        return instance.name if len(instance.short_name) <= 0 else instance.short_name


class TemplateCategorySerializer(ModelSerializer):
    parent = SerializerMethodField()

    class Meta:
        model = TemplateCategory
        read_only_fields = ('id', 'text', 'created', )
        fields = ('id', 'parent', 'uuid', 'name', 'level', 'position', )

    def get_parent(self, instance):
        return "#" if str(instance.parent) == UUID_ZERO else instance.parent


class UploadTypeSerializer(ModelSerializer):

    class Meta:
        model = UploadType
        read_only_fields = ('id', 'created',)
        fields = ('id', 'type', )


class UploadSerializer(ModelSerializer):
    type = UploadTypeSerializer()
    file_url = SerializerMethodField(source='name')

    class Meta:
        model = Upload
        read_only_fields = ('id', 'created',)
        fields = ('id', 'type', 'name', 'file_url', 'size', )

    def get_file_url(self, instance):
        fs = FileSystemStorage()
        return fs.url(str(instance.name))


class ImageSerializer(ModelSerializer):
    file_url = SerializerMethodField(source='name')

    class Meta:
        model = Image
        read_only_fields = ('id', 'created',)
        fields = ('id', 'name', 'file_url', 'size', )

    def create(self, validated_data):
        file_upload_obj = self.initial_data['fileToUpload']
        fs = FileSystemStorage()
        filename = fs.save(file_upload_obj.name, file_upload_obj)
        return Image.objects.create(name=filename, uploaded_name=file_upload_obj.name, size=file_upload_obj.size)

    def get_file_url(self, instance):
        fs = FileSystemStorage()
        return fs.url(str(instance.name))


class AuditIndicatorOptionSerializer(ModelSerializer):

    class Meta:
        model = AuditIndicatorOption
        read_only_fields = ('id', 'created', )
        fields = ('id', 'audit', 'indicator', 'option', )

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        return instance


class TemplateIndicatorSerializer(ModelSerializer):
    parent = SerializerMethodField(source=id)
    text = ReadOnlyField(source='indicator_source.name')
    images = SerializerMethodField()
    option = SerializerMethodField(source=id)
    indicator_type = SerializerMethodField(source='indicator.type')
    indicator_options = SerializerMethodField(source='indicator.options')

    class Meta:
        model = TemplateIndicator
        read_only_fields = ('id', 'text', 'created', )
        fields = ('id', 'parent', 'uuid', 'text', 'indicator_type', 'indicator_options', 'indicator_type', 'option', 'images', )

    def get_parent(self, instance):
        return "#" if str(instance.parent) == UUID_ZERO else instance.parent

    def get_images(self, instance):
        serializer = ImageSerializer(instance.images, many=True)
        return serializer.data

    def get_indicator_options(self, instance):
        serializer = IndicatorOptionSerializer(instance.indicator_source.options, many=True)
        return serializer.data

    def get_indicator_type(self, instance):
        serializer = IndicatorTypeSerializer(instance.indicator_source.type)
        return serializer.data

    def get_option(self, instance):
        serializer = AuditIndicatorOptionSerializer(AuditIndicatorOption.objects.get(audit=instance.template.audit,
                                                                                     indicator=instance))
        return serializer.data

    def update(self, instance, validated_data):
        print(validated_data)
        instance.option = validated_data.get('option', instance.option)
        instance.save()
        return instance


class AuditIndicatorNoteSerializer(ModelSerializer):

    class Meta:
        model = AuditIndicatorNote
        read_only_fields = ('id', 'created',)
        fields = ('id', 'audit', 'note', 'indicator', )

    def update(self, instance, validated_data):
        return instance


class AuditIndicatorUploadSerializer(ModelSerializer):

    class Meta:
        model = AuditIndicatorUpload
        read_only_fields = ('id', 'created',)
        fields = ('id', 'audit', 'upload', 'indicator', )

    def update(self, instance, validated_data):
        return instance


class IndicatorOptionSerializer(ModelSerializer):

    class Meta:
        model = IndicatorOption
        read_only_fields = ('id', 'created',)
        fields = ('id', 'option', 'active', 'company', )

    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def create(self, validated_data):
        return IndicatorOption.objects.create(**validated_data)


class IndicatorTypeSerializer(ModelSerializer):

    class Meta:
        model = IndicatorType
        read_only_fields = ('id', 'created',)
        fields = ('id', 'type', )


class NoteTypeSerializer(ModelSerializer):

    class Meta:
        model = NoteType
        read_only_fields = ('id', 'created', )
        fields = ('id', 'type', )


class NoteSerializer(ModelSerializer):
    type = PrimaryKeyRelatedField(queryset=NoteType.objects.all(), many=False, read_only=False)
    fromUser = PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=False, read_only=False)

    class Meta:
        model = Note
        read_only_fields = ('id', 'created', )
        fields = ('id', 'note', 'type', 'fromUser', )

    def create(self, validated_data):
        user_profile = 1
        return Note.objects.create(fromUser=user_profile, **validated_data)


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', )

    def create(self, validated_data):
        user_profile = 1
        company = Company.objects.create(user_profile=UserProfile.objects.get(pk=user_profile), **validated_data)

        for indicator_option in IndicatorOption.objects.filter(company=TEMPLATE_COMPANY, disabled=False):
            IndicatorOption.objects.create(option=indicator_option.option, company=company)

        for indicator_type in IndicatorType.objects.filter(company=TEMPLATE_COMPANY, disabled=False):
            IndicatorType.objects.create(type=indicator_type.type, company=company)

        return company

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class IndicatorCreateSerializer(ModelSerializer):

    class Meta:
        model = Indicator
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', 'short_name', 'company', 'type', )

    def create(self, validated_data):
        indicator = Indicator.objects.create(**validated_data)

        for indicator_option in IndicatorOption.objects.filter(company=TEMPLATE_COMPANY, active=True, disabled=False):
            indicator.options.add(indicator_option)

        indicator.save()

        return indicator


class IndicatorSerializer(ModelSerializer):
    options = SerializerMethodField()
    type = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Indicator
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', 'short_name', 'company', 'type', 'options', 'images', 'active', )

    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.type = validated_data.get('type', instance.type)

        if 'options' in self.validated_data.keys():
            for option in instance.options.all():
                instance.options.remove(option)

            for option in self.validated_data['options']:
                instance.options.add(option)

        if 'images' in self.validated_data.keys():
            instance.images = self.validated_data['images']

        instance.save()
        return instance

    def create(self, validated_data):
        indicator = Indicator.objects.create(**validated_data)

        for indicator_option in IndicatorOption.objects.filter(company=TEMPLATE_COMPANY, active=True, disabled=False):
            indicator.options.add(indicator_option)

        return indicator

    def get_options(self, instance):
        serializer = IndicatorOptionSerializer(instance.options.filter(company=instance.company), many=True)
        return serializer.data

    def get_type(self, instance):
        serializer = IndicatorTypeSerializer(IndicatorType.objects.get(pk=instance.type.pk))
        return serializer.data

    def get_images(self, instance):
        serializer = ImageSerializer(instance.images, many=True)
        return serializer.data


class TemplateCreateSerializer(ModelSerializer):

    class Meta:
        model = Template
        read_only_fields = ('id', 'created',)
        fields = ('id', 'name', 'categories', 'indicators', 'company', )

    def create(self, validated_data):
        categories = Category.objects.filter(company=validated_data.get("company"), active=True)
        indicators = Indicator.objects.filter(company=validated_data.get("company"), active=True)
        template = Template.objects.create(company=validated_data.get("company"), name=validated_data.get("name"))

        for category in categories:
            template_category = TemplateCategory(category_source=category,
                                                 template=template,
                                                 name=category.name)
            template_category.save()

        for indicator in indicators:
            template_indicator_type = TemplateIndicatorType.objects.create(type=indicator.type)
            template_indicator = TemplateIndicator(indicator_source=indicator,
                                                   template=template,
                                                   indicator_type=template_indicator_type,
                                                   name=indicator.name)
            template_indicator.save()
            for indicator_option in indicator.options.all():
                template_indicator_option = TemplateIndicatorOption.objects.create(option=indicator_option.option)
                template_indicator.indicator_options.add(template_indicator_option)

        return template


class TemplateListSerializer(ModelSerializer):

    class Meta:
        model = Template
        read_only_fields = ('id', 'created',)
        fields = ('id', 'name', 'categories', 'indicators', 'company', )


class TemplateDetailSerializer(ModelSerializer):
    categories = SerializerMethodField()
    indicators = SerializerMethodField('get_audit_id')

    class Meta:
        model = Template
        read_only_fields = ('id', 'created',)
        fields = ('id', 'name', 'categories', 'indicators', 'company', )

    def get_categories(self, instance):
        serializer = TemplateCategorySerializer(TemplateCategory.objects.filter(template=instance), many=True)
        return serializer.data

    def get_audit_id(self, instance):
        serializer = TemplateIndicatorDetailSerializer(TemplateIndicator.objects.filter(template=instance),
                                                       many=True,
                                                       context={'audit_id': self.context.get("audit_id")})
        return serializer.data

    def update(self, instance, validated_data):
        if "categories" in self.initial_data:
            for category in self.initial_data.get("categories"):
                template_category = TemplateCategory.objects.get(uuid=category['uuid'])
                template_category.parent = category['parent']
                # template_category.save()

        if "indicators" in self.initial_data:
            for indicator in self.initial_data.get("indicators"):
                template_indicator = TemplateIndicator.objects.get(uuid=indicator['uuid'])
                template_indicator.parent = indicator['parent']
                template_indicator.save()

        instance.__dict__.update(**validated_data)
        # instance.save()
        return instance

    def get_from_context(self, needle, instance):
        if needle in instance:
            return instance[needle]
        return None


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        read_only_fields = ('id', 'email', )
        fields = ('id', 'email', )


class NameTypeSerializer(ModelSerializer):

    class Meta:
        model = NameType
        read_only_fields = ('id', 'created', )
        fields = ('id', 'type', )


class PersonNameSerializer(ModelSerializer):
    type = NameTypeSerializer(many=False, read_only=True)

    class Meta:
        model = PersonName
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', 'type', )


class CountrySerializer(ModelSerializer):

    class Meta:
        model = Country
        read_only_fields = ('id', 'created', )
        fields = ('sort_name', 'name', 'id', 'phone_code', )

    def create(self, validated_data):
        return Country.objects.create(**validated_data)


class PhoneNumberTypeSerializer(ModelSerializer):

    class Meta:
        model = PhoneNumberType
        read_only_fields = ('id', 'created', )
        fields = ('id', 'type', )


class PhoneNumberSerializer(ModelSerializer):
    type = PhoneNumberTypeSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        depth = 2
        model = PhoneNumber
        read_only_fields = ('id', 'created', )
        fields = ('id', 'phone_number', 'type', 'country', )


class ClinicTypeSerializer(ModelSerializer):

    class Meta:
        model = ClinicType
        read_only_fields = ('id', 'created', )
        fields = ('id', 'type', 'active', 'company', )

    def create(self, validated_data):
        clinic_type = ClinicType.objects.create(**validated_data)
        return clinic_type


class SpecialtyTypeSerializer(ModelSerializer):

    class Meta:
        model = SpecialtyType
        read_only_fields = ('id', 'created', )
        fields = ('id', 'type', 'active', 'company', )

    def create(self, validated_data):
        specialty_type = SpecialtyType.objects.create(**validated_data)
        return specialty_type


class AuditAreaSerializer(ModelSerializer):
    director = SerializerMethodField()
    manager = SerializerMethodField()
    phone = SerializerMethodField()

    class Meta:
        model = AuditArea
        read_only_fields = ('id', 'created', )
        fields = ('id', 'name', 'present_on_rounds', 'company', 'director',
                  'manager', 'phone', 'specialty_type', 'clinic_type', )

    def get_director(self, instance):
        serializer = PersonNameSerializer(PersonName.objects.get(auditAreaDirector=instance))
        return serializer.data

    def get_manager(self, instance):
        serializer = PersonNameSerializer(PersonName.objects.get(auditAreaManager=instance))
        return serializer.data

    def get_phone(self, instance):
        serializer = PhoneNumberSerializer(PhoneNumber.objects.get(auditAreaPhoneNumber=instance))
        return serializer.data

    def create(self, validated_data):

        director = PersonNameSerializer(data=self.getContextItem("director", self.context))
        try:
            director.is_valid(raise_exception=True)
            director = director.save()
        except director.ValidationError as error:
            print(error)

        manager = PersonNameSerializer(data=self.getContextItem("manager", self.context))
        try:
            manager.is_valid(raise_exception=True)
            manager = manager.save()
        except director.ValidationError as error:
            print(error)

        phone = self.getContextItem("phone", self.context)
        phone = PhoneNumberSerializer(data={"country": Country.objects.get(pk=232),
                                            "type": phone['type'],
                                            "phone_number": phone["phone_number"]
                                            }
                                      )
        try:
            phone.is_valid(raise_exception=True)
            phone = phone.save()
        except director.ValidationError as error:
            print(error)

        return AuditArea.objects.create(phone=phone, manager=manager, director=director, **validated_data)

    def update(self, instance, validated_data):
        instance.specialty_type = SpecialtyType.objects.get(pk=self.getContextItem("specialty_type", self.context))
        instance.clinic_type = ClinicType.objects.get(pk=self.getContextItem("clinic_type", self.context))
        director = PersonName.objects.get(pk=instance.director.pk)
        director.name = self.getContextItem("director", self.context)['name']
        director.save()
        manager = PersonName.objects.get(pk=instance.manager.pk)
        manager.name = self.getContextItem("manager", self.context)['name']
        manager.save()
        phone = PhoneNumber.objects.get(pk=instance.phone.pk)
        phone.phone_number = self.getContextItem("phone", self.context)['phone_number']
        phone.save()
        instance.name = validated_data.get('name', instance.name)
        instance.present_on_rounds = validated_data.get('present_on_rounds', instance.present_on_rounds)
        instance.save()
        return instance

    @staticmethod
    def getContextItem(needle, instance):
        try:
            return instance[needle]
        except KeyError:
            return None


class TemplateIndicatorOptionSerializer(ModelSerializer):

    class Meta:
        model = TemplateIndicatorOption
        read_only_fields = ('id', 'created', )
        fields = ('id', 'option', )


class TemplateIndicatorDetailSerializer(ModelSerializer):
    indicator_options = SerializerMethodField()
    option = SerializerMethodField()
    images = SerializerMethodField()
    notes = SerializerMethodField()
    uploads = SerializerMethodField()

    class Meta:
        model = TemplateIndicator
        read_only_fields = ('id', 'created', )
        fields = ('id', 'uuid', 'name', 'parent', 'position', 'indicator_options', 'indicator_type', 'option', 'images', 'notes', 'uploads', )

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        return instance

    def get_indicator_options(self, instance):
        serializer = TemplateIndicatorOptionSerializer(instance.indicator_options.all(), many=True)
        return serializer.data

    def get_option(self, instance):
        try:
            audit_indicator_options = AuditIndicatorOption.objects.filter(audit=self.context.get("audit_id"),
                                                                          indicator=instance)
            for audit_indicator_option in audit_indicator_options:
                print(audit_indicator_option)
                serializer = AuditIndicatorOptionSerializer(audit_indicator_option)
            return serializer.data['option']
        except:
            return 1

    def get_images(self, instance):
        indicator_images = []
        indicator = Indicator.objects.get(pk=instance.indicator_source.pk)
        for images in indicator.images.all():
            serializer = ImageSerializer(images)
            indicator_images.append(serializer.data)
        return indicator_images

    def get_uploads(self, instance):
        audit_indicator_upload_list = []
        audit_indicator_uploads = AuditIndicatorUpload.objects.filter(audit=self.context.get("audit_id"), indicator=instance)
        for audit_indicator_upload in audit_indicator_uploads:
            serializer = UploadSerializer(Upload.objects.get(pk=audit_indicator_upload.upload.pk))
            audit_indicator_upload_list.append(serializer.data)
        return audit_indicator_upload_list

    def get_notes(self, instance):
        audit_indicator_notes_list = []
        audit_indicator_notes = AuditIndicatorNote.objects.filter(audit=self.context.get("audit_id"), indicator=instance)
        for audit_indicator_note in audit_indicator_notes:
            serializer = NoteSerializer(Note.objects.get(pk=audit_indicator_note.note.pk))
            audit_indicator_notes_list.append(serializer.data)
        return audit_indicator_notes_list


def get_template_categories(tc, audit_id, include_self=True):
    r = []

    if include_self:
        serializer = TemplateCategorySerializer(tc)
        category_serializer = serializer.data
        category_serializer['indicators'] = []
        for template_indicator in TemplateIndicator.objects.filter(parent=tc.uuid):
            indicator_serializer = TemplateIndicatorDetailSerializer(template_indicator, context={"audit_id": audit_id})
            category_serializer['indicators'] = [indicator_serializer.data]
        r.append(category_serializer)

    for template_category in TemplateCategory.objects.filter(parent=tc.uuid):
        r.append(get_template_categories(template_category, audit_id))

    return r


class TemplateCategoryDetailSerializer(ModelSerializer):
    categories = SerializerMethodField()

    class Meta:
        model = TemplateCategory
        read_only_fields = ('id', 'created', )
        fields = ('id', 'uuid', 'parent', 'position', 'template', 'categories', )

    def update(self, instance, validated_data):
        instance.parent = validated_data.get('parent', instance.parent)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.position = validated_data.get('position', instance.position)
        instance.save()

        return instance

    def get_categories(self, instance):
        request = self.context['request']
        x = get_template_categories(instance, request.query_params['audit'])
        return x


class AuditDetailSerializer(ModelSerializer):
    template = SerializerMethodField()
    area = SerializerMethodField()
    scores = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created',)
        fields = ('id', 'scores', 'area', 'name', 'template', )

    def get_template(self, instance):
        serializer = TemplateDetailSerializer(instance.template, context={'audit_id': instance.id})
        return serializer.data

    def get_scores(self, instance):
        return instance.template.indicators.through.objects.values('indicator_options').order_by('indicator_options').annotate(count=Count('indicator_options'))

    def get_area(self, instance):
        serializer = AuditAreaSerializer(instance.area)
        return serializer.data

    def update(self, instance, validated_data):
        return instance


class AuditListSerializer(ModelSerializer):
    template = SerializerMethodField()
    area = SerializerMethodField()
    scores = SerializerMethodField()
    company = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created', )
        fields = ('id', 'area', 'name', 'scores', 'company', 'template', 'created', )

    def get_company(self, instance):
        return instance.area.company.name

    def get_area(self, instance):
        serializer = AuditAreaSerializer(instance.area)
        return serializer.data

    def get_scores(self, instance):
        return instance.template.indicators.through.objects.values('indicator_options').order_by('indicator_options').annotate(count=Count('indicator_options'))

    def get_template(self, instance):
        serializer = TemplateListSerializer(instance.template)
        return serializer.data


class AuditCreateSerializer(ModelSerializer):
    scores = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created', )
        fields = ('id', 'area', 'name', 'scores', 'company', 'template', 'created', )

    def create(self, validated_data):
        audit = Audit.objects.create(**validated_data)
        return audit

    def get_scores(self, instance):
        return instance.template.indicators.through.objects.values('indicator_options').order_by('indicator_options').annotate(count=Count('indicator_options'))
