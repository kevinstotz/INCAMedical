import logging
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from API.models import Company, AuditArea, ClinicType, SpecialtyType, Template, Category, Indicator, TemplateCategory, \
    IndicatorType, IndicatorOption, TemplateIndicator, Audit, Index, NoteType, Note, Upload, UploadType, \
    AuditIndicatorOption, AuditIndicatorUpload, AuditIndicatorNote, UserStatus, CustomUser
from API.classes.utils import ReturnResponse
from API.classes.utils.Email import EmailHandler
from API.filters.filters import TemplateListFilter, TemplateCategoryListFilter, CompanyListFilter, CategoryListFilter, \
    IndicatorOptionListFilter, IndicatorListFilter, IndicatorTypeListFilter, SpecialtyTypeListFilter, AuditListFilter, \
    TemplateIndicatorListFilter, AuditAreaListFilter, AuditDetailFilter
from API.serializer import CompanySerializer, AuditAreaListSerializer, ClinicTypeSerializer, SpecialtyTypeSerializer, \
    TemplateListSerializer, CategorySerializer, IndicatorSerializer, TemplateCategorySerializer, ImageSerializer, \
    IndicatorOptionSerializer, TemplateIndicatorSerializer, AuditDetailSerializer, IndexSerializer, \
    NoteTypeSerializer, NoteSerializer, AuditListSerializer, TemplateIndicatorDetailSerializer, AuditCreateSerializer, \
    TemplateCategoryDetailSerializer, UploadSerializer, TemplateDetailSerializer, IndicatorTypeSerializer, \
    IndicatorCreateSerializer, TemplateCreateSerializer, AuditIndicatorOptionSerializer, AuditAreaDetailSerializer, \
    CustomUserRegisterSerializer, CustomUserLoginSerializer, CustomUserSerializer, CustomUserPasswordResetSerializer, \
    CustomUserDetailSerializer

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from API.settings.Globals import DEFAULT_USER, WEBSITE_DIR, USER_STATUS, EMAIL_TEMPLATE, ACCESS_TOKEN_EXPIRE_SECONDS
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from rest_framework_json_api import renderers
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.oauth2_backends import OAuthLibCore
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import generics, status, permissions
import json
from urllib import parse
from uuid import UUID
from os.path import join
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s', )
logger = logging.getLogger(__name__)


class CustomUserPasswordReset(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser, )
    serializer_class = CustomUserPasswordResetSerializer
    queryset = CustomUser.objects.all()
    model = CustomUser
    lookup_field = 'uuid'

    def get(self, request, *args, **kwargs):
        if self.get_object():
            user = self.get_object()
            return redirect("http://www.www.incamedical.com:10101/static/reset.html?uuid=" + str(user.uuid))
        return redirect("http://www.www.incamedical.com:10101/")

    def update(self, request, *args, **kwargs):
        data = request.data.dict()

        print(data)
        if not data.get("confirm_password"):
            raise ValidationError("Empty Confirm Password")

        if not data.get('password'):
            raise ValidationError("Empty Password")

        if data.get('password') != data.get("confirm_password"):
            raise ValidationError("Mismatch")

        user = self.get_object()
        if data.get('password'):
            user.set_password(data.get('password'))
            user.save()
            return Response(ReturnResponse.Response(0, __name__, user.pk, "success").return_json(),
                            status=status.HTTP_200_OK)

        return Response(ReturnResponse.Response(0, __name__, "failed", "success").return_json(),
                        status=status.HTTP_400_BAD_REQUEST)


class CustomUserForgotPassword(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser, )
    queryset = CustomUser.objects.all()
    model = CustomUser

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            try:
                return self.model.objects.get(email=email)
            except Exception as error:
                return None
        return None

    def get(self, request, *args, **kwargs):
        if self.get_queryset():
            user = self.get_queryset()
            email_handler = EmailHandler(api="http://www.api.incamedical.com:10100",
                                         website="http://www.www.incamedical.com:10101")
            email_handler.send_template(EMAIL_TEMPLATE['FORGOT'], user)
            return Response(ReturnResponse.Response(0, __name__, user.pk, "success").return_json(),
                            status=status.HTTP_200_OK)
        return Response(ReturnResponse.Response(0, __name__, 0, "Not Found").return_json(),
                        status=status.HTTP_400_BAD_REQUEST)


class CustomUserLogin(generics.GenericAPIView, OAuthLibMixin, OAuthLibCore):
    permission_classes = [permissions.AllowAny, ]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserLoginSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
    model = CustomUser

    def validate(self, data):
        print("serializer validate")

        try:
            return CustomUser.objects.get(email=data.get('email'))
        except CustomUser.DoesNotExist:
            raise ValidationError("Username not found")

    def post(self, request):

        if request.auth is None:
            custom_user = None
            try:
                custom_user = CustomUser.objects.get(email=request.data.get('username'))
            except CustomUser.DoesNotExist:
                return Response(ReturnResponse.Response(1, __name__, "no user", "error").return_json(),
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    custom_user = authenticate(request, username=custom_user.username, password=request.data.get('password'))
                    if custom_user is None:
                        return Response(ReturnResponse.Response(1, __name__, "Failed Authentication", "error").return_json(), status=status.HTTP_401_UNAUTHORIZED)
                    login(request, custom_user)
                    uri, http_method, body, headers = self._extract_params(request)
                    data = body
                    params = dict(parse.parse_qsl(data))
                    uri = OAuthLibCore().create_authorization_response(request=request,
                                                                       scopes={"read": "Read Scope", "write": "Write Scope"},
                                                                       credentials={"redirect_uri": params['redirect_uri'], "response_type": params['response_type'], "client_id": params['client_id']},
                                                                       allow=True)

                    params = parse.urlparse(uri[0])
                    params = dict(parse.parse_qsl(params.fragment))
                    return Response(params, status=200)
                    if status_code != 200:
                        raise Exception(json.loads(body).get("error_description", ""))
                    return Response(json.loads(body), status=status_code)
            except Exception as error:
                print("error")
                print(error)
                return Response(ReturnResponse.Response(1, __name__, error, "error").return_json(),
                                status=status.HTTP_400_BAD_REQUEST)

            print("error2")
            return Response(ReturnResponse.Response(1, __name__, "error", "error").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        print("error3")
        return Response(ReturnResponse.Response(1, __name__, "error", "error").return_json(),
                        status=status.HTTP_403_FORBIDDEN)


class CustomUserRegister(OAuthLibMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomUserSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None:
            data = request.data.dict()
            serializer = CustomUserRegisterSerializer(data=data,
                                                      context={"confirm_password": data.get("confirm_password")})
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        new_user = get_user_model().objects.create_user(email=serializer.validated_data.get('email'),
                                                                        password=serializer.validated_data.get('password'),
                                                                        status=USER_STATUS['REGISTERED'],
                                                                        firstname=data.get("firstname"),
                                                                        lastname=data.get("lastname"))
                        email_handler = EmailHandler(api="http://www.api.incamedical.com:10100",
                                                     website="http://www.www.incamedical.com:10101")
                        email_handler.send_template(EMAIL_TEMPLATE['CONFIRM'], new_user)
                    return Response(ReturnResponse.Response(0, __name__, new_user.pk, "success").return_json(),
                                    status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(ReturnResponse.Response(1, __name__, e, "error2").return_json(),
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(ReturnResponse.Response(1, __name__, serializer.errors, "error3").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(1, __name__, "error", "error4").return_json(),
                        status=status.HTTP_403_FORBIDDEN)


class CustomUserConfirmAccount(OAuthLibMixin, generics.ListAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomUserSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def get(self, request, *args, **kwargs):

        try:
            UUID(str(kwargs.get("uuid")), version=3)
        except Exception as error:
            print(error)
            return Response(ReturnResponse.Response(0, __name__, "Bad UUID", "Failed").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            custom_user = CustomUser.objects.get(uuid=str(kwargs.get("uuid")), user_profile__disabled=False)
            custom_user.status = UserStatus.objects.get(pk=USER_STATUS['ACTIVE'])
            custom_user.save()
            email_handler = EmailHandler(api="http://www.www.incamedical.com:10100",
                                         website="http://www.www.incamedical.com:10101")
            email_handler.send_template(EMAIL_TEMPLATE['WELCOME'], custom_user)
            return redirect("http://www.www.incamedical.com:10101/static/login.html")

        except Exception as error:
            print(error)
            return Response(ReturnResponse.Response(0, __name__, "Bad User", "Failed").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)


class IndicatorImageUpload(generics.RetrieveUpdateAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
            filename = fs.save(join(str(audit), str(pk), file_upload_obj.name), file_upload_obj)
            upload = Upload.objects.create(name=filename,
                                           uploaded_name=file_upload_obj.name,
                                           size=file_upload_obj.size,
                                           type=file_upload_type)
            upload_serializer = self.get_serializer(upload)
        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Option Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            AuditIndicatorUpload.objects.create(audit=Audit.objects.get(pk=audit),
                                                                        upload=upload,
                                                                        indicator=self.get_object())

        except (RuntimeError, TypeError, NameError) as e:
            result = '{0}:'.format(e)
            print(result)
            return Response(ReturnResponse.Response(1, __name__, 'Indicator Option Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(0, __name__, json.dumps(upload_serializer.data), "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndexView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = IndexSerializer
    parser_classes = (JSONParser, )
    queryset = Index.objects.all()
    model = Index

    def get(self, request, *args, **kwargs):
        print(request)
        return Response(ReturnResponse.Response(0, __name__, request.data, "success").return_json(),
                        status=status.HTTP_201_CREATED)
    def post(self, request, *args, **kwargs):
        print(request)
        return Response(ReturnResponse.Response(0, __name__, request.data, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class IndicatorTypeList(generics.ListAPIView):
    model = IndicatorType
    serializer_class = IndicatorTypeSerializer
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = IndicatorType.objects.filter(disabled=False).order_by('type')
    filter_class = IndicatorTypeListFilter


class IndicatorTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = IndicatorType
    serializer_class = IndicatorTypeSerializer
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = IndicatorType.objects.filter(disabled=False)


class IndicatorOptionList(generics.ListCreateAPIView):
    model = IndicatorOption
    serializer_class = IndicatorOptionSerializer
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = IndicatorOption.objects.filter(disabled=False)
    filter_class = IndicatorOptionListFilter


class TemplateIndicatorList(generics.ListAPIView):
    model = TemplateIndicator
    serializer_class = TemplateIndicatorSerializer
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = TemplateIndicator.objects.filter(disabled=False)
    filter_class = TemplateIndicatorListFilter


class TemplateCategoryList(generics.ListAPIView):
    model = TemplateCategory
    serializer_class = TemplateCategorySerializer
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = TemplateCategory.objects.filter(disabled=False).order_by('category_source__parent')
    filter_class = TemplateCategoryListFilter


class IndicatorCreate(generics.CreateAPIView):
    model = Indicator
    queryset = Indicator.objects.filter(disabled=False).order_by('name')
    serializer_class = IndicatorCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_class = IndicatorListFilter


class IndicatorDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Indicator
    serializer_class = IndicatorSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    queryset = Category.objects.filter(disabled=False)


class TemplateCreate(generics.CreateAPIView):
    model = Template
    queryset = Template.objects.filter(disabled=False)
    serializer_class = TemplateCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    required_scopes = ['view']
    filter_class = SpecialtyTypeListFilter
    filter_fields = ('company', )


class SpecialtyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = SpecialtyType
    queryset = SpecialtyType.objects.filter(disabled=False)
    serializer_class = SpecialtyTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_fields = ('company', )


class AuditList(generics.ListAPIView):
    model = Audit
    queryset = Audit.objects.filter(disabled=False).order_by('created')
    serializer_class = AuditListSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_class = AuditListFilter


class AuditCreate(generics.CreateAPIView, mixins.CreateModelMixin):
    model = Audit
    queryset = Audit.objects.filter(disabled=False)
    serializer_class = AuditCreateSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_class = AuditDetailFilter


class TemplateIndicatorDetail(generics.RetrieveUpdateAPIView):
    model = TemplateIndicator
    queryset = TemplateIndicator.objects.filter(disabled=False)
    serializer_class = TemplateIndicatorDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser, FormParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]


class TemplateCategoryDetail(generics.RetrieveUpdateAPIView):
    model = TemplateCategory
    queryset = TemplateCategory.objects.filter(disabled=False)
    serializer_class = TemplateCategoryDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]


class ClinicTypeList(generics.ListCreateAPIView):
    model = ClinicType
    queryset = ClinicType.objects.filter(disabled=False).order_by('type')
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_fields = ('company', )


class NoteTypeList(generics.ListAPIView):
    model = NoteType
    queryset = NoteType.objects.filter(disabled=False).order_by('type')
    serializer_class = NoteTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]


class ClinicTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = ClinicType
    queryset = ClinicType.objects.filter(disabled=False)
    serializer_class = ClinicTypeSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]


class AuditAreaList(generics.ListCreateAPIView):
    model = AuditArea
    queryset = AuditArea.objects.filter(disabled=False).order_by('name')
    serializer_class = AuditAreaListSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_class = AuditAreaListFilter

    def put(self, request):

        audit_area = AuditAreaListSerializer(data=request.data,
                                             context={"manager": request.data.pop("manager"),
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
    serializer_class = AuditAreaDetailSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        audit_area = self.get_serializer(self.get_object(), data=request.data, partial=True)
        try:
            audit_area.is_valid(raise_exception=True)
            audit_area = audit_area.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(audit_area.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Audit Area Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(0, __name__, audit_area.id, "success").return_json(),
                        status=status.HTTP_201_CREATED)


class AuditIndicatorOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    model = AuditIndicatorOption
    queryset = AuditIndicatorOption.objects.all()
    serializer_class = AuditIndicatorOptionSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    lookup_fields = ('audit', 'indicator', )

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter_fields = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter_fields[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter_fields)  # Lookup the object

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


class UserDetail(generics.RetrieveUpdateAPIView):
    model = CustomUser
    queryset = CustomUser.objects.filter(user_profile__disabled=False).order_by('id')
    serializer_class = CustomUserSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        serializer = CustomUserDetailSerializer(self.get_object(), data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
        except ValidationError as error:
            result = '{0}:'.format(error)
            logger.error("SerializeR Error: {0}: error:{1}".format(serializer.errors, result))
            return Response(ReturnResponse.Response(1, __name__, 'Custom USer Error', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(ReturnResponse.Response(0, __name__, serializer.id, "success").return_json(),
                        status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    model = CustomUser
    queryset = CustomUser.objects.filter(user_profile__disabled=False).order_by('id')
    serializer_class = CustomUserSerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]


class CompanyList(generics.ListAPIView):
    model = Company
    queryset = Company.objects.filter(disabled=False).order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]
    filter_class = CompanyListFilter


class CompanyCreate(generics.CreateAPIView):
    model = Company
    queryset = Company.objects.filter(disabled=False).order_by('name')
    serializer_class = CompanySerializer
    renderer_classes = (renderers.JSONRenderer, )
    parser_classes = (JSONParser, )
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

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
