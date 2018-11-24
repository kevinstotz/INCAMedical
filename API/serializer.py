import logging
from API.settings.Globals import UUID_ZERO
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from API.models import Company, AuditArea, TemplateIndicator, TemplateCategory, Audit, Image, Upload, \
    CustomUser, PersonName, NameType, PhoneNumber, PhoneNumberType, UserProfile, Index, Note, NoteType, \
    Country, ClinicType, SpecialtyType, Template, Category, Indicator, IndicatorOption, IndicatorType, UploadType
from django.core.files.storage import FileSystemStorage


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class IndexSerializer(ModelSerializer):

    class Meta:
        model = Index


class CategorySerializer(ModelSerializer):
    short_name = SerializerMethodField()

    class Meta:
        model = Category
        read_only_fields = ('id', )
        fields = ('id', 'name', 'short_name', 'active', )

    def create(self, validated_data):
        company = Company.objects.get(pk=self.get_context_company("company", self.context))
        return Category.objects.create(company=company,
                                       short_name="",
                                       **validated_data
                                       )

    def get_context_company(self, needle, instance):
        if needle in instance:
            return instance[needle]
        return None

    def get_short_name(self, instance):
        return instance.name if len(instance.short_name) <= 0 else instance.short_name


class TemplateCategorySerializer(ModelSerializer):
    parent = SerializerMethodField(source='parent')
    text = ReadOnlyField(source='category.name', )
    category = CategorySerializer()

    class Meta:
        model = TemplateCategory
        read_only_fields = ('id', 'text', )
        fields = ('id', 'parent', "uuid", 'text', 'category', )

    def get_parent(self, instance):
        return "#" if str(instance.parent) == UUID_ZERO else instance.parent


class UploadTypeSerializer(ModelSerializer):

    class Meta:
        model = UploadType
        read_only_fields = ('id', )
        fields = ('id', 'type', )


class UploadSerializer(ModelSerializer):
    type = UploadTypeSerializer()
    file_url = SerializerMethodField(source='name')

    class Meta:
        model = Upload
        read_only_fields = ('id', )
        fields = ('id', 'type', 'name', 'file_url', 'size', )

    def get_file_url(self, instance):
        fs = FileSystemStorage()
        return fs.url(str(instance.name))


class ImageSerializer(ModelSerializer):
    file_url = SerializerMethodField(source='name')

    class Meta:
        model = Image
        read_only_fields = ('id', )
        fields = ('id', 'created', 'name', 'file_url', 'size', )

    def create(self, validated_data):
        file_upload_obj = self.initial_data['fileToUpload']
        fs = FileSystemStorage()
        filename = fs.save(file_upload_obj.name, file_upload_obj)
        return Image.objects.create(name=filename, uploaded_name=file_upload_obj.name, size=file_upload_obj.size)

    def get_file_url(self, instance):
        fs = FileSystemStorage()
        return fs.url(str(instance.name))


class TemplateIndicatorSerializer(ModelSerializer):
    parent = SerializerMethodField(source=id)
    text = ReadOnlyField(source='indicator.name')
    images = ImageSerializer(many=True)
    type = SerializerMethodField(source='indicator.type')
    options = SerializerMethodField(source='indicator.options')
    uploads = UploadSerializer(many=True)

    class Meta:
        model = TemplateIndicator
        read_only_fields = ('id', 'text', )
        fields = ('id', 'parent', "uuid", 'text', 'images', 'type', 'indicator_option', 'options', "uploads", )

    def get_parent(self, instance):
        return "#" if str(instance.parent) == UUID_ZERO else instance.parent

    def get_options(self, instance):
        serializer = IndicatorOptionSerializer(instance.indicator.options, many=True)
        return serializer.data

    def get_type(self, instance):
        serializer = IndicatorTypeSerializer(instance.indicator.type)
        return serializer.data

    def update(self, instance, validate_data):
        pass


class IndicatorOptionSerializer(ModelSerializer):

    class Meta:
        model = IndicatorOption
        read_only_fields = ('id', )
        fields = ('id', 'option', 'active', )


class IndicatorTypeSerializer(ModelSerializer):

    class Meta:
        model = IndicatorType
        read_only_fields = ('id', )
        fields = ('id', 'type', 'active', )


class IndicatorSerializer(ModelSerializer):
    short_name = SerializerMethodField()
    type = SerializerMethodField()
    options = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Indicator
        read_only_fields = ('id', )
        fields = ('id', 'name', 'short_name', 'active', 'options', 'type', 'images', )

    def update(self, instance, validated_data):

        if 'type' in self.initial_data.keys():
            instance.type = IndicatorType.objects.get(pk=self.initial_data['type']['type'])
        if 'active' in self.initial_data.keys():
            instance.active = self.initial_data['active']
        if 'images' in self.initial_data.keys():
            print(self.initial_data['images'])
            instance.images = self.initial_data['images']
        instance.save()
        return instance

    def create(self, validated_data):
        company = Company.objects.get(pk=self.get_context_company("company", self.context))
        return Indicator.objects.create(company=company,
                                        **validated_data
                                        )

    def get_context_company(self, needle, instance):
        if needle in instance:
            return instance[needle]
        return None

    def get_short_name(self, instance):
        return instance.name if len(instance.short_name) <= 0 else instance.short_name

    def get_type(self, instance):
        serializer = IndicatorTypeSerializer(IndicatorType.objects.get(indicatorType=instance),
                                             read_only=False,
                                             partial=True)
        return serializer.data

    def get_options(self, instance):
        serializer = IndicatorOptionSerializer(instance.options.get_queryset(), many=True)
        return serializer.data

    def get_images(self, instance):
        serializer = ImageSerializer(instance.images.get_queryset(), many=True)
        return serializer.data


class TemplateSerializer(ModelSerializer):
    categories = TemplateCategorySerializer(source='templateCategoryCategory',
                                            many=True,
                                            read_only=True,
                                            partial=True)
    indicators = TemplateIndicatorSerializer(source='templateCategoryIndicator',
                                             many=True,
                                             read_only=True,
                                             partial=True)

    class Meta:
        model = Template
        read_only_fields = ('id', )
        fields = ('id', 'name', 'categories', 'indicators', 'company', 'active', )

    def create(self, validated_data):
        company = Company.objects.get(pk=self.get_from_context("company", self.context))
        categories = Category.objects.filter(company=company, active=True)
        indicators = Indicator.objects.filter(company=company, active=True)
        template = Template.objects.create(company=company,
                                           name=validated_data.get("name")
                                           )
        for category in categories:
            template_category = TemplateCategory(category=category, template=template)
            template_category.save()
        for indicator in indicators:
            template_indicator = TemplateIndicator(indicator=indicator, template=template)
            template_indicator.save()

        return template

    def update(self, instance, validated_data):
        if "categories" in self.initial_data:
            for category in self.initial_data.get("categories"):
                template_category = TemplateCategory.objects.get(uuid=category['uuid'])
                template_category.parent = category['parent']
                template_category.save()

        if "indicators" in self.initial_data:
            for indicator in self.initial_data.get("indicators"):
                template_indicator = TemplateIndicator.objects.get(uuid=indicator['uuid'])
                template_indicator.parent = indicator['parent']
                template_indicator.save()

        instance.__dict__.update(**validated_data)
        instance.save()
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
        fields = ('id', 'type', )


class PersonNameSerializer(ModelSerializer):
    type = NameTypeSerializer(many=False, read_only=True)

    class Meta:
        model = PersonName
        fields = ('id', 'name', 'type', )


class CountrySerializer(ModelSerializer):

    class Meta:
        model = Country
        fields = ('sort_name', 'name', 'id', 'phone_code', )

    def create(self, validated_data):
        return Country.objects.create(**validated_data)


class PhoneNumberTypeSerializer(ModelSerializer):

    class Meta:
        model = PhoneNumberType
        fields = ('id', 'type', )


class PhoneNumberSerializer(ModelSerializer):
    type = PhoneNumberTypeSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        depth = 2
        model = PhoneNumber
        fields = ('id', 'phone_number', 'type', 'country', )


class NoteTypeSerializer(ModelSerializer):

    class Meta:
        model = NoteType
        fields = ('id', 'type', )


class NoteSerializer(ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'note', )

    def create(self, validated_data):
        user_profile = 1
        return Note.objects.create(fromUser=CustomUser.objects.get(pk=user_profile), **validated_data)


class ClinicTypeSerializer(ModelSerializer):

    class Meta:
        model = ClinicType
        fields = ('id', 'type', )


class SpecialtyTypeSerializer(ModelSerializer):

    class Meta:
        model = SpecialtyType
        fields = ('id', 'type', )


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'active', )

    def create(self, validated_data):
        user_profile = 1
        return Company.objects.create(user_profile=UserProfile.objects.get(pk=user_profile), **validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AuditAreaSerializer(ModelSerializer):
    director = SerializerMethodField()
    manager = SerializerMethodField()
    phone = SerializerMethodField()
    specialty_type = SerializerMethodField()
    clinic_type = SerializerMethodField()
    company = SerializerMethodField()

    class Meta:
        model = AuditArea
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

    def get_clinic_type(self, instance):
        serializer = ClinicTypeSerializer(ClinicType.objects.get(auditAreaClinicType=instance))
        return serializer.data

    def get_specialty_type(self, instance):
        serializer = SpecialtyTypeSerializer(SpecialtyType.objects.get(auditAreaSpecialtyType=instance))
        return serializer.data

    def get_company(self, instance):
        serializer = CompanySerializer(Company.objects.get(auditAreaCompany=instance))
        return serializer.data

    def create(self, validated_data):
        validated_data["company"] = Company.objects.get(pk=self.getContextItem("company", self.context))
        clinic_type = ClinicType.objects.get(pk=self.getContextItem("clinic_type", self.context))
        specialty_type = SpecialtyType.objects.get(pk=self.getContextItem("specialty_type", self.context))

        director = PersonNameSerializer(data=self.getContextItem("director", self.context))
        manager = PersonNameSerializer(data=self.getContextItem("manager", self.context))
        phone = PhoneNumberSerializer(data={"country": Country.objects.get(pk=232),
                                            "type": self.getContextItem("phone", self.context)['type'],
                                            "phone_number": self.getContextItem("phone", self.context)["phone_number"]
                                            }
                                      )
        if director.is_valid() and manager.is_valid() and phone.is_valid():
            director.save()
            director_obj = PersonName.objects.get(pk=director['id'].value)
            manager.save()
            manager_obj = PersonName.objects.get(pk=manager['id'].value)
            phone.save()
            phone_obj = PhoneNumber.objects.get(pk=phone['id'].value)
            return AuditArea.objects.create(director=director_obj,
                                            manager=manager_obj,
                                            specialty_type=specialty_type,
                                            clinic_type=clinic_type,
                                            phone=phone_obj,
                                            **validated_data
                                            )
        return None

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


class TemplateIndicatorDetailSerializer(ModelSerializer):

    class Meta:
        model = TemplateIndicator
        read_only_fields = ('id', 'created', )
        fields = ('id', 'uuid', 'parent', 'indicator_option', )

    def update(self, instance, validated_data):
        print(validated_data)
        # image = ImageSerializer(data=validated_data['data'])
        return instance


class TemplateCategoryDetailSerializer(ModelSerializer):

    class Meta:
        model = TemplateCategory
        read_only_fields = ('id', 'created',)
        fields = ('id', 'uuid', 'parent', )

    def update(self, instance, validated_data):
        print(validated_data)


class AuditSerializer(ModelSerializer):
    template = SerializerMethodField()
    area = SerializerMethodField()
    categories = SerializerMethodField()
    indicators = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created',)
        fields = ('id', 'area', 'name', 'active', 'template', 'created', 'categories', 'indicators', )

    def get_template(self, instance):
        serializer = TemplateSerializer(instance.template)
        return serializer.data

    def get_area(self, instance):
        serializer = AuditAreaSerializer(instance.area)
        return serializer.data

    def get_categories(self, instance):
        queryset = TemplateCategory.objects.filter(template=instance.template)
        serializer = TemplateCategorySerializer(queryset, source='templateCategoryCategory', many=True)
        return serializer.data

    def get_indicators(self, instance):
        queryset = TemplateIndicator.objects.filter(template=instance.template)
        serializer = TemplateIndicatorSerializer(queryset, source='templateIndicatorIndicator', many=True)
        return serializer.data

    def update(self, instance, validated_data):
        return instance


class AuditListSerializer(ModelSerializer):
    template = SerializerMethodField()
    area = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created', )
        fields = ('id', 'area', 'name', 'active', 'template', 'created', )

    def get_template(self, instance):
        serializer = TemplateSerializer(instance.template)
        return serializer.data

    def get_area(self, instance):
        serializer = AuditAreaSerializer(instance.area)
        return serializer.data

