import logging
from rest_framework import mixins
from API.models import Company, AuditArea, ClinicType, SpecialtyType, Template, Category, Indicator, TemplateCategory, \
    IndicatorType, IndicatorOption, TemplateIndicator, Audit, Index, NoteType, Note, Image, Upload, UploadType, \
    AuditIndicatorOption, AuditIndicatorUpload, AuditIndicatorNote
from API.classes.utils import ReturnResponse
from API.filters.filters import TemplateListFilter, TemplateCategoryListFilter, CompanyListFilter, CategoryListFilter, \
    IndicatorOptionListFilter, IndicatorListFilter, IndicatorTypeListFilter, SpecialtyTypeListFilter, AuditListFilter, \
    TemplateIndicatorListFilter, AuditAreaListFilter, AuditDetailFilter
from API.serializer import CompanySerializer, AuditAreaSerializer, ClinicTypeSerializer, SpecialtyTypeSerializer, \
    TemplateListSerializer, CategorySerializer, IndicatorSerializer, TemplateCategorySerializer, ImageSerializer, \
    IndicatorOptionSerializer, TemplateIndicatorSerializer, AuditDetailSerializer, IndexSerializer, \
    NoteTypeSerializer, NoteSerializer, AuditListSerializer, TemplateIndicatorDetailSerializer, AuditCreateSerializer, \
    TemplateCategoryDetailSerializer, UploadSerializer, TemplateDetailSerializer, IndicatorTypeSerializer, \
    IndicatorCreateSerializer, TemplateCreateSerializer, AuditIndicatorOptionSerializer, AuditIndicatorUploadSerializer, \
    AuditIndicatorNoteSerializer
from API.settings.Globals import DEFAULT_USER, PROJECT_DIR
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from rest_framework_json_api import renderers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import generics, status
import json
from os.path import join


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
logger = logging.getLogger(__name__)


class IndicatorImageUpload(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = IndicatorSerializer
    parser_classes = (MultiPartParser, FormParser, )
    queryset = Indicator.objects.all()
    model = Indicator

    def post(self, request, pk):
        image = ImageSerializer(data=request.data)

        try:
            image.is_valid(raise_exception=ValueError)
            image.save()
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            return Response(ReturnResponse.Response(1, __name__, 'Image failed to create', "failed").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        indicator = self.get_object()
        indicator.images.add(image.instance)
        indicator.save()

        res = image.data
        res['indicator'] = indicator.id
        return Response(ReturnResponse.Response(0, __name__, json.dumps(res), "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditIndicatorNoteDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TemplateIndicatorDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    queryset = TemplateIndicator.objects.all()
    model = TemplateIndicator

    def update(self, request, *args, **kwargs):

        notes = request.data.pop("notes")
        note = Note.objects.create(note=notes['note'],
                                   type=NoteType.objects.get(pk=notes['type']),
                                   creator=DEFAULT_USER)

        audit_indicator_note = AuditIndicatorNote.objects.create(audit=Audit.objects.get(pk=request.data['audit']),
                                                                 note=note,
                                                                 indicator=self.get_object())

        return Response(ReturnResponse.Response(0, __name__, audit_indicator_note.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditIndicatorImageUpload(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser, FormParser, )
    queryset = TemplateIndicator.objects.all()
    model = TemplateIndicator

    def post(self, request, pk, audit):

        file_upload_obj = request.data['fileToUpload']
        file_upload_type = ""
        upload = ""

        for upload_type in UploadType.objects.all():
            file_upload_type = upload_type
            if upload_type.type == file_upload_obj.name.split(".")[-1].lower():
                file_upload_type = upload_type
                break
        fs = FileSystemStorage()

        try:
            filename = fs.save(join(PROJECT_DIR, "media", "images", file_upload_obj.name), file_upload_obj)
            upload = Upload.objects.create(name=filename,
                                           uploaded_name=file_upload_obj.name,
                                           size=file_upload_obj.size,
                                           type=file_upload_type)
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Option Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            audit_indicator_upload = AuditIndicatorUpload.objects.create(audit=Audit.objects.get(pk=audit),
                                                                         upload=upload,
                                                                         indicator=self.get_object())

        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Option Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, audit_indicator_upload , "success").return_json(), status=status.HTTP_201_CREATED)


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
    queryset = IndicatorType.objects.filter(disabled=False).order_by('type')
    filter_class = IndicatorTypeListFilter


class IndicatorTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = IndicatorType
    serializer_class = IndicatorTypeSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorType.objects.filter(disabled=False)


class IndicatorOptionList(generics.ListCreateAPIView):
    model = IndicatorOption
    serializer_class = IndicatorOptionSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorOption.objects.filter(disabled=False).order_by('option')
    filter_class = IndicatorOptionListFilter

    def put(self, request):
        indicator_option = IndicatorOptionSerializer(data=request.data, partial=True)

        try:
            indicator_option.is_valid(raise_exception=True)
            indicator_option = indicator_option.save()

        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(indicator_option.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Option Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, indicator_option.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndicatorOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    model = IndicatorOption
    serializer_class = IndicatorOptionSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = IndicatorOption.objects.filter(disabled=False)
    filter_class = IndicatorOptionListFilter


class TemplateIndicatorList(generics.ListAPIView):
    model = TemplateIndicator
    serializer_class = TemplateIndicatorSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = TemplateIndicator.objects.filter(disabled=False)
    filter_class = TemplateIndicatorListFilter


class TemplateCategoryList(generics.ListAPIView):
    model = TemplateCategory
    serializer_class = TemplateCategorySerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = TemplateCategory.objects.filter(disabled=False).order_by('category_source__parent')
    filter_class = TemplateCategoryListFilter


class IndicatorCreate(generics.CreateAPIView):
    model = Indicator
    queryset = Indicator.objects.filter(disabled=False).order_by('name')
    serializer_class = IndicatorCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = IndicatorListFilter

    def put(self, request):
        indicator = IndicatorSerializer(data=request.data, partial=True)

        try:
            indicator.is_valid(raise_exception=True)
            indicator = indicator.save()

        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(indicator.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, indicator.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndicatorList(generics.ListAPIView):
    model = Indicator
    queryset = Indicator.objects.filter(disabled=False).order_by('name')
    serializer_class = IndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = IndicatorListFilter


class IndicatorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Indicator
    serializer_class = IndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = Indicator.objects.filter(disabled=False)

    def update(self, request, *args, **kwargs):
        serializer = IndicatorSerializer(instance=self.get_object(),
                                         data=request.data,
                                         partial=True,
                                         read_only=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            result = '{0}:'.format(e)
            print(result)
            result = '{0}:'.format(e)
            logger.error("SerializeR Error: {0}: error: {1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.validated_data, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class CategoryList(generics.ListCreateAPIView):
    model = Category
    queryset = Category.objects.filter(disabled=False).order_by('name')
    serializer_class = CategorySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)
    filter_class = CategoryListFilter

    def put(self, request):
        category = CategorySerializer(data=request.data)
        try:
            category.is_valid(raise_exception=True)
            category = category.save()
        except ValidationError as error:
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
    queryset = Category.objects.filter(disabled=False)


class TemplateCreate(generics.CreateAPIView):
    model = Template
    queryset = Template.objects.filter(disabled=False)
    serializer_class = TemplateCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def put(self, request):

        template = TemplateCreateSerializer(data=request.data)

        try:
            template.is_valid(raise_exception=True)
            template = template.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(template.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Template Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class NoteDetail(generics.ListCreateAPIView):
    model = Note
    queryset = Note.objects.filter(disabled=False)
    serializer_class = NoteSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)

    def put(self, request):
        data = request.data
        company = data.pop("company")
        note = NoteSerializer(data=request.data, context=company)

        try:
            note.is_valid(raise_exception=True)
            note = note.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(note.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Note Failed', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, note.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class TemplateList(generics.ListAPIView):
    model = Template
    queryset = Template.objects.filter(disabled=False).order_by('name')
    serializer_class = TemplateListSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = TemplateListFilter

    def put(self, request):
        data = request.data
        company = data.pop("company")
        template = TemplateListSerializer(data=request.data, context={"company": company})

        try:
            template.is_valid(raise_exception=True)
            template = template.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(template.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Template Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Template
    serializer_class = TemplateDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    queryset = Template.objects.filter(disabled=False)

    def patch(self, request, *args, **kwargs):

        template = TemplateDetailSerializer(self.get_object(), data=request.data, partial=True)

        try:
            template.is_valid(raise_exception=True)
            template = template.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(template.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Template Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class SpecialtyTypeList(generics.ListCreateAPIView):
    model = SpecialtyType
    queryset = SpecialtyType.objects.filter(disabled=False).order_by('type')
    serializer_class = SpecialtyTypeSerializer
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = SpecialtyTypeListFilter
    filter_fields = ('company', )


class SpecialtyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = SpecialtyType
    queryset = SpecialtyType.objects.filter(disabled=False)
    serializer_class = SpecialtyTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_fields = ('company', )


class AuditList(generics.ListAPIView):
    model = Audit
    queryset = Audit.objects.filter(disabled=False).order_by('created')
    serializer_class = AuditListSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditListFilter


class AuditCreate(generics.CreateAPIView, mixins.CreateModelMixin):
    model = Audit
    queryset = Audit.objects.filter(disabled=False)
    serializer_class = AuditCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditDetailFilter

    def create(self, request, *args, **kwargs):

        audit = AuditCreateSerializer(data=request.data)
        try:
            audit.is_valid(raise_exception=True)
            audit = audit.save()
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            result = '{0}:'.format(e)
            print(result)
            result = '{0}:'.format(e)
            print("SerializeR Error: {0}: error:{1}".format(audit.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Audit Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, audit.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Audit
    queryset = Audit.objects.filter(disabled=False)
    serializer_class = AuditDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditDetailFilter


class TemplateIndicatorDetail(generics.RetrieveUpdateAPIView):
    model = TemplateIndicator
    queryset = TemplateIndicator.objects.filter(disabled=False)
    serializer_class = TemplateIndicatorDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser, FormParser, )
    permission_classes = (AllowAny, )


class TemplateCategoryDetail(generics.RetrieveUpdateAPIView):
    model = TemplateCategory
    queryset = TemplateCategory.objects.filter(disabled=False)
    serializer_class = TemplateCategoryDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def get2(self, request):
        template_category = TemplateCategoryDetailSerializer(data=request.data,
                                                             context={"audit": self.request.GET.get("audit")})
        try:
            template_category.is_valid(raise_exception=True)
            template_category = template_category.save()
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)

            logger.error("SerializeR Error: {0}: error:{1}".format(template_category.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, template_category.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class ClinicTypeList(generics.ListCreateAPIView):
    model = ClinicType
    queryset = ClinicType.objects.filter(disabled=False).order_by('type')
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_fields = ('company', )


class NoteTypeList(generics.ListAPIView):
    model = NoteType
    queryset = NoteType.objects.filter(disabled=False).order_by('type')
    serializer_class = NoteTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class ClinicTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = ClinicType
    queryset = ClinicType.objects.filter(disabled=False)
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )


class AuditAreaList(generics.ListCreateAPIView):
    model = AuditArea
    queryset = AuditArea.objects.filter(disabled=False).order_by('name')
    serializer_class = AuditAreaSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = AuditAreaListFilter

    def put(self, request):

        audit_area = AuditAreaSerializer(data=request.data, context={"manager": request.data.pop("manager"),
                                                                     "director": request.data.pop("director"),
                                                                     "phone": request.data.pop("phone")})

        try:
            audit_area.is_valid(raise_exception=True)
            audit_area = audit_area.save()
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)

            logger.error("SerializeR Error: {0}: error:{1}".format(audit_area.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, audit_area.pk, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditAreaDetail(generics.RetrieveUpdateDestroyAPIView):
    model = AuditArea
    queryset = AuditArea.objects.filter(disabled=False)
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
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Audit Area Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)

    def post(self, request):
        pass


class AuditIndicatorOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    model = AuditIndicatorOption
    queryset = AuditIndicatorOption.objects.all()
    serializer_class = AuditIndicatorOptionSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    lookup_fields = ('audit', 'indicator', )

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

    def update(self, request, *args, **kwargs):

        serializer = AuditIndicatorOptionSerializer(self.get_object(), data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Audit Area Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class CompanyList(generics.ListAPIView):
    model = Company
    queryset = Company.objects.filter(disabled=False).order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )
    filter_class = CompanyListFilter

    def get_serializer_context(self):
        return {'user_profile': 2}


class CompanyCreate(generics.CreateAPIView):
    model = Company
    queryset = Company.objects.filter(disabled=False).order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def put(self, request):
        company = CompanySerializer(data=request.data)

        try:
            company.is_valid(raise_exception=True)
            company = company.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(company.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, company.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Company
    queryset = Company.objects.filter(disabled=False)
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        serializer = CompanySerializer(self.get_object(), data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            company = serializer.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Company Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, company.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)
