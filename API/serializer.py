import logging
from API.settings.Globals import UUID_ZERO
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from API.models import Company, AuditArea, TemplateIndicator, TemplateCategory, Audit, \
    CustomUser, PersonName, NameType, PhoneNumber, PhoneNumberType, UserProfile, Index, \
    Country, ClinicType, SpecialtyType, Template, Category, Indicator, IndicatorOption, IndicatorType


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

    def get_context_company(self, needle, obj):
        if needle in obj:
            return obj[needle]
        return None

    def get_short_name(self, obj):
        return obj.name if len(obj.short_name) <= 0 else obj.short_name


class TemplateCategorySerializer(ModelSerializer):
    parent = SerializerMethodField(source=id)
    text = ReadOnlyField(source='category.name', )

    class Meta:
        model = TemplateCategory
        read_only_fields = ('id', 'text')
        fields = ('id', 'parent', "uuid", 'text', )

    def get_parent(self, obj):
        return "#" if str(obj.parent) == UUID_ZERO else obj.parent


class TemplateIndicatorSerializer(ModelSerializer):
    parent = SerializerMethodField(source=id)
    text = ReadOnlyField(source='indicator.name', )

    class Meta:
        model = TemplateIndicator
        read_only_fields = ('id', 'text')
        fields = ('id', 'parent', "uuid", 'text', )

    def get_parent(self, obj):
        return "#" if str(obj.parent) == UUID_ZERO else obj.parent


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

    class Meta:
        model = Indicator
        read_only_fields = ('id', )
        fields = ('id', 'name', 'short_name', 'active', 'options', 'type', 'image', )

    def create(self, validated_data):
        company = Company.objects.get(pk=self.get_context_company("company", self.context))
        return Indicator.objects.create(company=company,
                                        **validated_data
                                        )

    def get_context_company(self, needle, obj):
        if needle in obj:
            return obj[needle]
        return None

    def get_short_name(self, obj):
        return obj.name if len(obj.short_name) <= 0 else obj.short_name

    def get_type(self, obj):
        serializer = IndicatorTypeSerializer(IndicatorType.objects.get(indicatorType=obj))
        return serializer.data

    def get_options(self, instance):
        serializer = IndicatorOptionSerializer(instance.options.get_queryset(), many=True)
        return serializer.data


class TemplateSerializer(ModelSerializer):
    categories = TemplateCategorySerializer(source='templateCategoryCategory', many=True, read_only=True, partial=True)

    class Meta:
        model = Template
        read_only_fields = ('id', )
        fields = ('id', 'name', 'categories', 'company', 'active', )

    def create(self, validated_data):
        company = Company.objects.get(pk=validated_data.get("company"))
        categories = Category.objects.filter(company=company, active=True)
        indicators = Indicator.objects.filter(company=company, active=True)
        template = Template.objects.create(company=company,
                                           name=validated_data.get("name")
                                           )
        for category in categories:
            templateCategory = TemplateCategory(category=category, template=template)
            templateCategory.save()
        for indicator in indicators:
            templateIndicator = TemplateIndicator(indicator=indicator, template=template)
            templateIndicator.save()

        return template

    def update(self, instance, validated_data):

        if "categories" in self.initial_data:
            for category in self.initial_data.get("categories"):
                templateCategory = TemplateCategory.objects.get(uuid=category['uuid'])
                templateCategory.parent = category['parent']
                templateCategory.save()

        if "indicators" in self.initial_data:
            for indicator in self.initial_data.get("indicators"):
                templateIndicator= TemplateIndicator.objects.get(uuid=indicator['uuid'])
                templateIndicator.parent = indicator['parent']
                templateIndicator.save()

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

    def get_context_company(self, needle, obj):
        if needle in obj:
            return obj[needle]
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

    def get_director(self, obj):
        serializer = PersonNameSerializer(PersonName.objects.get(auditAreaDirector=obj))
        return serializer.data

    def get_manager(self, obj):
        serializer = PersonNameSerializer(PersonName.objects.get(auditAreaManager=obj))
        return serializer.data

    def get_phone(self, obj):
        serializer = PhoneNumberSerializer(PhoneNumber.objects.get(auditAreaPhoneNumber=obj))
        return serializer.data

    def get_clinic_type(self, obj):
        serializer = ClinicTypeSerializer(ClinicType.objects.get(auditAreaClinicType=obj))
        return serializer.data

    def get_specialty_type(self, obj):
        serializer = SpecialtyTypeSerializer(SpecialtyType.objects.get(auditAreaSpecialtyType=obj))
        return serializer.data

    def get_company(self, obj):
        serializer = CompanySerializer(Company.objects.get(auditAreaCompany=obj))
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
    def getContextItem(needle, obj):
        try:
            return obj[needle]
        except KeyError:
            return None


class AuditSerializer(ModelSerializer):
    template = SerializerMethodField()
    area = SerializerMethodField()
    categories = SerializerMethodField()
    indicators = SerializerMethodField()

    class Meta:
        model = Audit
        read_only_fields = ('id', 'created',)
        fields = ('id', 'area', 'name', 'active', 'template', 'categories', 'created', 'indicators', )

    def get_template(self, obj):
        serializer = TemplateSerializer(Template.objects.get())
        return serializer.data

    def get_area(self, instance):
        serializer = AuditAreaSerializer(AuditArea.objects.get())
        return serializer.data

    def get_categories(self, instance):
        serializer = TemplateCategorySerializer(TemplateCategory.objects.all().order_by("parent", "uuid"), many=True)
        return serializer.data

    def get_indicators(self, instance):
        serializer = TemplateIndicatorSerializer(TemplateIndicator.objects.all().order_by("parent", "uuid"), many=True)
        return serializer.data