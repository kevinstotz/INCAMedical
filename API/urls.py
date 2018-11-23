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
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from API.settings.Base import Base
from API.views.company.views import IndexView, \
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
    TemplateCategoryDetail, TemplateIndicatorDetail, \
    AuditList, AuditCreate, AuditDetail, \
    NoteTypeList, NoteDetail, ImageUpload, AuditImageUpload

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'', IndexView.as_view(), name="indexView"),
    path(r'api/', IndexView.as_view(), name="indexView"),
    path(r'api/v1/', IndexView.as_view(), name="indexView"),

    path(r'api/v1/company/', CompanyList.as_view()),
    path(r'api/v1/company/create/', CompanyCreate.as_view(), name="companyCreate"),
    path(r'api/v1/company/<int:pk>/', CompanyDetail.as_view(), name="companyDetail"),

    path(r'api/v1/indicator-type/', IndicatorTypeList.as_view(), name="indicatorTypeList"),
    path(r'api/v1/indicator-type<int:pk>//', IndicatorTypeDetail.as_view(), name="indicatorTypeDetail"),

    path(r'api/v1/indicator-option/', IndicatorOptionList.as_view(), name="indicatorOptionList"),
    path(r'api/v1/indicator-option/<int:pk>/', IndicatorOptionDetail.as_view(), name="indicatorOptionDetail"),

    path(r'api/v1/clinic-type/', ClinicTypeList.as_view(), name="clinicTypeList"),
    path(r'api/v1/clinic-type/<int:pk>/', ClinicTypeDetail.as_view(), name="clinicTypeDetail"),

    path(r'api/v1/specialty-type/', SpecialtyTypeList.as_view(), name="specialtyTypeList"),
    path(r'api/v1/specialty-type/<int:pk>/', SpecialtyTypeDetail.as_view(), name="specialtyTypeDetail"),

    path(r'api/v1/audit-area/', AuditAreaList.as_view(), name="auditAreaList"),
    path(r'api/v1/audit-area/<int:pk>/', AuditAreaDetail.as_view(), name="auditAreaDetail"),

    path(r'api/v1/template/', TemplateList.as_view()),
    path(r'api/v1/template/create/', TemplateCreate.as_view(), name="templateCreate"),
    path(r'api/v1/template/<int:pk>/', TemplateDetail.as_view(), name="templateDetail"),

    path(r'api/v1/category/', CategoryList.as_view(), name="categoryList"),
    path(r'api/v1/category/<int:pk>/', CategoryDetail.as_view(), name="categoryDetail"),

    path(r'api/v1/note-type/', NoteTypeList.as_view(), name="noteTypeList"),
    path(r'api/v1/note/', NoteDetail.as_view(), name="note"),

    path(r'api/v1/image-upload/', ImageUpload.as_view(), name="imageUpload"),
    path(r'api/v1/audit-image-upload/<int:pk>/', AuditImageUpload.as_view(), name="auditImageUpload"),

    path(r'api/v1/indicator/', IndicatorList.as_view(), name="indicatorList"),
    path(r'api/v1/indicator/<int:pk>/', IndicatorDetail.as_view(), name="indicatorDetail"),

    path(r'api/v1/template-category/', TemplateCategoryList.as_view(), name="templateCategoryList"),
    path(r'api/v1/template-category/<int:pk>/', TemplateCategoryDetail.as_view(), name="templateCategoryDetail"),

    path(r'api/v1/template-indicator/', TemplateIndicatorList.as_view(), name="templateIndicatorList"),
    path(r'api/v1/template-indicator/<int:pk>/', TemplateIndicatorDetail.as_view(), name="templateIndicatorDetail"),

    path(r'api/v1/audit/', AuditList.as_view(), name="auditsAuditList"),
    path(r'api/v1/audit/create/', AuditCreate.as_view(), name="auditsAuditCreate"),
    path(r'api/v1/audit/<int:pk>/', AuditDetail.as_view(), name="auditsAuditDetail"),
 ] + static(Base.MEDIA_URL, document_root=Base.MEDIA_ROOT)
#  static(Base.STATIC_URL, document_root=Base.STATIC_ROOT) +
urlpatterns = format_suffix_patterns(urlpatterns)
