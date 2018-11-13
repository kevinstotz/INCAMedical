"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from API.views.company.views  import \
    CompanyList, CompanyDetail, CompanyCreate, \
    SpecialtyTypeList, SpecialtyTypeDetail, \
    AuditAreaList, AuditAreaDetail, \
    ClinicTypeList, ClinicTypeDetail, \
    TemplateList, TemplateDetail, TemplateCreate, \
    CategoryList, CategoryDetail, \
    IndicatorList, IndicatorDetail, \
    IndicatorTypeList, IndicatorTypeDetail, \
    IndicatorOptionList, IndicatorOptionDetail, \
    TemplateCategoryList, TemplateIndicatorList, \
    AuditList, AuditCreate, AuditDetail

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'api/v1/company/', CompanyList.as_view({'get': 'list'})),
    path(r'api/v1/company/create/', CompanyCreate.as_view(), name="companyCreate"),
    path(r'api/v1/company/<int:pk>/', CompanyDetail.as_view(), name="companyDetail"),

    path(r'api/v1/indicator-type/', IndicatorTypeList.as_view({'get': 'list'}), name="indicatorTypeList"),
    path(r'api/v1/indicator-type<int:pk>//', IndicatorTypeDetail.as_view(), name="indicatorTypeDetail"),

    path(r'api/v1/indicator-option/', IndicatorOptionList.as_view({'get': 'list'}), name="indicatorOptionList"),
    path(r'api/v1/indicator-option/<int:pk>/', IndicatorOptionDetail.as_view(), name="indicatorOptionDetail"),

    path(r'api/v1/clinic-type/', ClinicTypeList.as_view(), name="clinicTypeList"),
    path(r'api/v1/clinic-type/<int:pk>/', ClinicTypeDetail.as_view(), name="clinicTypeDetail"),

    path(r'api/v1/specialty-type/', SpecialtyTypeList.as_view(), name="specialtyTypeList"),
    path(r'api/v1/specialty-type/<int:pk>/', SpecialtyTypeDetail.as_view(), name="specialtyTypeDetail"),

    path(r'api/v1/audit-area/', AuditAreaList.as_view(), name="auditAreaList"),
    path(r'api/v1/audit-area/<int:pk>/', AuditAreaDetail.as_view(), name="auditAreaDetail"),

    path(r'api/v1/template/', TemplateList.as_view({'get': 'list'})),
    path(r'api/v1/template/create/', TemplateCreate.as_view(), name="templateCreate"),
    path(r'api/v1/template/<int:pk>/', TemplateDetail.as_view(), name="templateDetail"),

    path(r'api/v1/category/', CategoryList.as_view(), name="categoryList"),
    path(r'api/v1/category/<int:pk>/', CategoryDetail.as_view(), name="categoryDetail"),

    path(r'api/v1/indicator/', IndicatorList.as_view(), name="indicatorList"),
    path(r'api/v1/indicator/<int:pk>/', IndicatorDetail.as_view(), name="indicatorDetail"),

    path(r'api/v1/template-category/', TemplateCategoryList.as_view({'get': 'list'}), name="templateCategoryList"),
    path(r'api/v1/template-indicator/', TemplateIndicatorList.as_view({'get': 'list'}), name="templateIndicatorList"),

    path(r'api/v1/audit/', AuditList.as_view({'get': 'list'}), name="auditsAuditList"),
    path(r'api/v1/audit/create/', AuditCreate.as_view(), name="auditsAuditCreate"),
    path(r'api/v1/audit/<int:pk>/', AuditDetail.as_view(), name="auditsAuditDetail"),
 ]

urlpatterns = format_suffix_patterns(urlpatterns)
