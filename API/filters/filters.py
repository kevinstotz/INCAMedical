from rest_framework_filters import FilterSet, filters
from API.models import Template, TemplateCategory, Company, IndicatorOption, IndicatorType, Indicator, Category, \
    SpecialtyType, AuditArea, TemplateIndicator, Audit


class TemplateListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        model = Template
        fields = ['id', 'active', 'company', ]


class TemplateIndicatorListFilter(FilterSet):
    template = filters.RelatedFilter(TemplateListFilter, field_name="template__id", queryset=Template.objects.all())
    active = filters.BooleanFilter()
    company = filters.NumberFilter()
    parent = filters.CharFilter()

    class Meta:
        Model = TemplateIndicator
        fields = ['active', 'company', 'template', 'parent', ]


class TemplateCategoryListFilter(FilterSet):
    template = filters.RelatedFilter(TemplateListFilter, field_name="template__id", queryset=Template.objects.all())
    active = filters.BooleanFilter()
    company = filters.NumberFilter()
    parent = filters.CharFilter()

    class Meta:
        Model = TemplateCategory
        fields = ['active', 'company', 'template', 'parent', ]


class CompanyListFilter(FilterSet):
    active = filters.BooleanFilter()

    class Meta:
        Model = Company
        fields = ['active', ]


class IndicatorTypeListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = IndicatorType
        fields = ['active', 'company', ]


class IndicatorOptionListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = IndicatorOption
        fields = ['active', 'company', ]


class IndicatorListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = Indicator
        fields = ['active', 'company', ]


class CategoryListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = Category
        fields = ['active', 'company', ]


class SpecialtyTypeListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = SpecialtyType
        fields = ['active', 'company', ]


class AuditAreaListFilter(FilterSet):
    active = filters.BooleanFilter()
    company = filters.NumberFilter()

    class Meta:
        Model = AuditArea
        fields = ['active', 'company', ]


class AuditListFilter(FilterSet):
    company = filters.RelatedFilter(TemplateListFilter,
                                    field_name="template__company__id",
                                    queryset=Template.objects.all())
    active = filters.BooleanFilter()
    template = filters.NumberFilter()

    class Meta:
        Model = Audit
        fields = ['active', 'company', 'template', ]