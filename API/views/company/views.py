import logging
from rest_framework import serializers
from API.models import Company, AuditArea, ClinicType, SpecialtyType, Template, Category, Indicator, TemplateCategory, \
    IndicatorType, IndicatorOption, TemplateIndicator, Audit, Index, NoteType, Note, Image, Upload
from API.classes.utils import ReturnResponse
from API.filters.filters import TemplateListFilter, TemplateCategoryListFilter, CompanyListFilter, CategoryListFilter, \
    IndicatorOptionListFilter, IndicatorListFilter, IndicatorTypeListFilter, SpecialtyTypeListFilter, AuditListFilter, \
    TemplateIndicatorListFilter, AuditAreaListFilter
from API.serializer import CompanySerializer, AuditAreaSerializer, ClinicTypeSerializer, SpecialtyTypeSerializer, \
    TemplateSerializer, CategorySerializer, IndicatorSerializer, TemplateCategorySerializer, IndicatorTypeSerializer, \
    IndicatorOptionSerializer, TemplateIndicatorSerializer, AuditSerializer, IndexSerializer, AuditListSerializer, \
    NoteTypeSerializer, NoteSerializer, ImageSerializer, TemplateIndicatorDetailSerializer, \
    TemplateCategoryDetailSerializer
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from rest_framework_json_api import renderers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser
from rest_framework import generics, status
import json


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
logger = logging.getLogger(__name__)


class ImageUpload(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser, )
    queryset = Image.objects.all()
    model = Image

    def post(self, request, *args, **kwargs):
        image = ImageSerializer(data=request.data)

        try:
            image.is_valid(raise_exception=ValueError)
            image.save()
        except Exception as e:
            print('{0}'.format(e))
            return Response(ReturnResponse.Response(1, __name__, 'Image failed to create', "failed").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        indicator = Indicator.objects.get(pk=self.request.data['id'])
        indicator.images.add(image.instance)
        indicator.save()

        res = image.data
        res['indicator'] = indicator.id
        return Response(ReturnResponse.Response(0, __name__, json.dumps(res), "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditImageUpload(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TemplateIndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser, FormParser, )
    queryset = Upload.objects.all()
    model = Upload

    def post(self, request, *args, **kwargs):
        file_upload_obj = request.data['fileToUpload']
        fs = FileSystemStorage()
        upload = ""
        try:
            filename = fs.save(file_upload_obj.name, file_upload_obj)
            upload = Upload.objects.create(name=filename, uploaded_name=file_upload_obj.name, size=file_upload_obj.size)
            template_indicator = TemplateIndicator.objects.get(pk=self.kwargs['pk'])
            template_indicator.uploads.add(upload)
            upload = Upload.objects.filter(pk=upload.id)
        except Exception as e:
            print(e)

        data = serializers.serialize('json', upload)
        return Response(ReturnResponse.Response(0, __name__, data, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndexView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = IndexSerializer
    parser_classes = (JSONParser, )
    queryset = Index.objects.all()
    model = Index


class IndicatorTypeList(generics.ListAPIView):
    model = IndicatorType
    serializer_class = IndicatorTypeSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorType.objects.all().order_by('type')
    filter_class = IndicatorTypeListFilter


class IndicatorTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = IndicatorType
    serializer_class = IndicatorTypeSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorType.objects.all()


class IndicatorOptionList(generics.ListAPIView):
    model = IndicatorOption
    serializer_class = IndicatorOptionSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorOption.objects.all().order_by('option')
    filter_class = IndicatorOptionListFilter


class IndicatorOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    model = IndicatorOption
    serializer_class = IndicatorOptionSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorOption.objects.all()


class TemplateIndicatorList(generics.ListAPIView):
    model = TemplateIndicator
    serializer_class = TemplateIndicatorSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = TemplateIndicator.objects.all()
    filter_class = TemplateIndicatorListFilter


class TemplateCategoryList(generics.ListAPIView):
    model = TemplateCategory
    serializer_class = TemplateCategorySerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = TemplateCategory.objects.all().order_by('category__name')
    filter_class = TemplateCategoryListFilter


class IndicatorList(generics.ListCreateAPIView):
    model = Indicator
    queryset = Indicator.objects.all().order_by('name')
    serializer_class = IndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)
    filter_class = IndicatorListFilter

    def put(self, request):
        data = request.data
        company = data.pop("company")
        indicator = IndicatorSerializer(data=request.data, context={"company": company})

        try:
            indicator.is_valid(raise_exception=True)
            indicator = indicator.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(indicator.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, indicator.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndicatorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Indicator
    serializer_class = IndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, FileUploadParser, )
    permission_classes = (AllowAny, )
    queryset = Indicator.objects.all()


class CategoryList(generics.ListCreateAPIView):
    model = Category
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)
    filter_class = CategoryListFilter

    def put(self, request):
        data = request.data
        company = data.pop("company")
        category = CategorySerializer(data=request.data, context={"company": company})
        try:
            category.is_valid(raise_exception=True)
            category = category.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(category.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Category Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, category.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = CategorySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()


class TemplateCreate(generics.CreateAPIView):
    model = Template
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)

    def put(self, request):
        data = request.data
        company = data.pop("company")
        template = TemplateSerializer(data=request.data, context=company)

        try:
            template.is_valid(raise_exception=True)
            template = template.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(template.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Template Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class NoteDetail(generics.ListCreateAPIView):
    model = Note
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)

    def put(self, request):
        data = request.data
        print(data)
        company = data.pop("company")
        note = NoteSerializer(data=request.data, context=company)

        try:
            note.is_valid(raise_exception=True)
            note = note.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(note.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Note Failed', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, note.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class TemplateList(generics.ListAPIView):
    model = Template
    queryset = Template.objects.all().order_by('name')
    serializer_class = TemplateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = TemplateListFilter

    def put(self, request):
        data = request.data
        company = data.pop("company")
        template = TemplateSerializer(data=request.data, context={"company": company})

        try:
            template.is_valid(raise_exception=True)
            template = template.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(template.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Template Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Template
    serializer_class = TemplateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = Template.objects.filter(active=True)


class SpecialtyTypeList(generics.ListCreateAPIView):
    model = SpecialtyType
    queryset = SpecialtyType.objects.all().order_by('type')
    serializer_class = SpecialtyTypeSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = SpecialtyTypeListFilter


class SpecialtyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = SpecialtyType
    queryset = SpecialtyType.objects.all()
    serializer_class = SpecialtyTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class AuditList(generics.ListAPIView):
    model = Audit
    queryset = Audit.objects.all().order_by('created')
    serializer_class = AuditListSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditListFilter


class AuditCreate(generics.CreateAPIView):
    model = Audit
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class AuditDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Audit
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class TemplateIndicatorDetail(generics.RetrieveUpdateAPIView):
    model = TemplateIndicator
    queryset = TemplateIndicator.objects.all()
    serializer_class = TemplateIndicatorDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser, FormParser, )
    permission_classes = (AllowAny, )


class TemplateCategoryDetail(generics.RetrieveUpdateAPIView):
    model = TemplateCategory
    queryset = TemplateCategory.objects.all()
    serializer_class = TemplateCategoryDetailSerializer
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)


class ClinicTypeList(generics.ListCreateAPIView):
    model = ClinicType
    queryset = ClinicType.objects.all().order_by('type')
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class NoteTypeList(generics.ListAPIView):
    model = NoteType
    queryset = NoteType.objects.all().order_by('type')
    serializer_class = NoteTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class ClinicTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = ClinicType
    queryset = ClinicType.objects.all()
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class AuditAreaList(generics.ListCreateAPIView):
    model = AuditArea
    queryset = AuditArea.objects.all().order_by('name')
    serializer_class = AuditAreaSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditAreaListFilter

    def put(self, request):
        context = request.data
        company_id = context.pop("companyId")
        director = context.pop("director")
        manager = context.pop("manager")
        clinic_type_id = context.pop("clinicTypeId")
        specialty_type_id = context.pop("specialtyTypeId")
        phone = context.pop("phone")
        audit_area = AuditAreaSerializer(data=request.data, context={"company": company_id,
                                                                     "director": director,
                                                                     "manager": manager,
                                                                     "phone": phone,
                                                                     "clinic_type": clinic_type_id,
                                                                     "specialty_type": specialty_type_id,
                                                                     })

        try:
            audit_area.is_valid(raise_exception=True)
            audit_area = audit_area.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(audit_area.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, audit_area.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditAreaDetail(generics.RetrieveUpdateDestroyAPIView):
    model = AuditArea
    queryset = AuditArea.objects.all()
    serializer_class = AuditAreaSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        audit_area = AuditArea.objects.get(pk=self.kwargs['pk'])
        context = request.data
        serializer = AuditAreaSerializer(audit_area, data=request.data, partial=True, context=context)
        try:
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Audit Area Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)

    def post(self, request):
        pass


class CompanyList(generics.ListAPIView):
    model = Company
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = CompanyListFilter

    def get_serializer_context(self):
        return {'user_profile': 2}


class CompanyCreate(generics.CreateAPIView):
    model = Company
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def put(self, request):
        company = CompanySerializer(data=request.data)
        try:
            company.is_valid(raise_exception=True)
            company = company.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(company.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, company.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        company = Company.objects.get(pk=self.kwargs['pk'])
        serializer = CompanySerializer(company, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(company.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)
