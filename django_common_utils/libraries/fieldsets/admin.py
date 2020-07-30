import logging
from collections import Iterable as collections_Iterable
from typing import *

from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db.models.options import Options
from django.http import HttpRequest
from django.utils.translation import gettext as _

from .sections import FieldsetList, Sections
from ..typings import *
from ..utils import camelcase_to_underscore, model_verbose


class AdminFieldsetMixin:
    name = "__"
    
    def __init__(self):
        self.name = camelcase_to_underscore(
            self.__class__.__name__
                .replace("Admin", "")
                .replace("Fieldset", "")
                .replace("Mixin", "")
        )
    
    def get_mixin_fields(self, **_) -> Dict[str, List[str]]:
        return {}
    
    def get_fieldsetslist(self, **_) -> Union[list, FieldsetList, None]:
        return None
    
    def get_readonly_fields(self, **_) -> Union[Iterable[str], str, None]:
        return None
    
    def get_search_fields(self, **_) -> Union[list, str, set, None]:
        return None
    
    def get_list_display(self, **_) -> Union[list, str, set, None]:
        return None
    
    def get_list_display_links(self, **_) -> Union[list, str, set, None]:
        return None
    
    def get_list_filter(self, **_) -> Union[list, str, set, None]:
        return None
    
    def get_autocomplete_fields(self, **_) -> Union[list, str, set, None]:
        return None
    
    def get_actions(self, **_) -> Union[list, str, set, None]:
        return None


class BaseAdminMixinsMixin:
    mixins = []
    order_by_required = True  # type: Optional[bool]
    fieldset_fields = {
        "default": ["...!"],
        "advanced": ["...!"],
        "created": ["...!"]
    }
    fieldset_descriptions = {}
    make_not_editable_readonly = True
    allow_mixin_methods = "*"  # type: Union[list, str]
    
    def get_section(self) -> Sections:
        # Default sections
        return Sections([
            FieldsetList(
                order=0,
                appearance=None,
                name="default",
                fields=[]
            ),
            FieldsetList(
                order=2,
                appearance=_("Advanced Settings"),
                classes=["collapse", ],
                name="advanced",
                description=_("Pay attention when editing these fields."),
                fields=[]
            ),
            FieldsetList(
                order=3,
                appearance=_("Visible after creation"),
                classes=["collapse", ],
                name="created",
                description=_("These fields are visible after this object got created."),
                fields=["id"]
            )
        ])
    
    def get_collected_fieldsets(self) -> Sections:
        fieldset = self.get_section()
        
        for fs in self.get_fieldsetslist():  # type: FieldsetList
            fieldset.add_fieldsetlist(fs)
        
        return fieldset
    
    def __get_fields(self, method: str, **kwargs) -> list:
        """
            Collects all fields from this class using a given method.
            Return types of the method should be a str, Iterable or None.
            If returned type is an Iterable, these fields will be added.
            If returned type is None, no field will be added.
            If returned type is anything else, it'll added to a list and that list will be added.
        :param method: The method that should be executed
        :param kwargs: **kwargs that should be passed to the method
        :return: set containing all fields
        """
        if self.allow_mixin_methods != "*" and (isinstance(method, list) and method not in self.allow_mixin_methods):
            raise ValueError(f"Method \"{method}\" is not allowed for mixins!")
        
        all_fields = []
        
        for mixin in self.mixins:  # type: AdminFieldsetMixin.__class__
            init = mixin()  # type: AdminFieldsetMixin
            fields = getattr(init, method)(**kwargs)
            
            # Add fields
            # Append, if it's a str
            if isinstance(fields, collections_Iterable) and type(fields) is not str:
                all_fields.extend(fields)
            elif fields is not None:
                all_fields.append(fields)
        
        # Add super() fields, if super() has this method
        if hasattr(super(), method):
            all_fields += getattr(super(), method)(**kwargs)
        
        return all_fields
    
    def __get_fieldsets(self, **kwargs) -> Sections:
        fieldset = self.get_collected_fieldsets()
        
        # Add fieldsets of mixins
        for fieldsetlist in self.get_fieldsetslist(**kwargs):  # type: FieldsetList
            fieldset.add_fieldsetlist(fieldsetlist)
        fieldset.add_fields(self.fieldset_fields)  # Add given fields from ModelAdmin
        
        # Add fields of mixins
        fieldset.add_fields(self.get_mixin_fields(**kwargs))
        
        for name, description in self.fieldset_descriptions.items():  # type: str
            if description not in getattr((fl := fieldset[name]), "description"):
                fl.description += "\n" + description
        
        return fieldset
    
    @staticmethod
    def __get_kwargs(*args) -> dict:
        request, obj = args
        
        if obj is HttpRequest:
            obj, request = request, obj
        
        return {
            "obj": obj,
            "request": request
        }
    
    def get_fieldsets(self, request=None, obj=None) -> list:
        return self.__get_fieldsets(**self.__get_kwargs(request, obj)).render()
    
    def get_readonly_fields(self, request=None, obj=None) -> list:
        # Get predefined readonly fields and from mixins
        readonly = \
            list(super().get_readonly_fields(request, obj)) + \
            self.__get_fields("get_readonly_fields", **self.__get_kwargs(request, obj))
        
        if self.make_not_editable_readonly:
            # noinspection PyProtectedMember
            meta = self.model._meta  # type: Options
            
            for field in self.__get_fieldsets(request=request, obj=obj).flatten_fields:  # type: str
                try:
                    # If field is not editable, add it to the readonly fields
                    if not meta.get_field(field).editable:
                        readonly.append(field)
                # If field does not exist, just continue. Maybe it`s a custom property from the admin class
                except FieldDoesNotExist:
                    continue
        
        return readonly
    
    def get_search_fields(self, request):
        return self.__get_fields("get_search_fields", request=request)
    
    def get_list_display(self, request):
        return self.__get_fields("get_list_display", request=request)
    
    def get_list_display_links(self, request, list_display):
        return self.__get_fields("get_list_display_links", request=request, list_display=list_display)
    
    def get_list_filter(self, request):
        return self.__get_fields("get_list_filter", request=request)
    
    def get_autocomplete_fields(self, request):
        return self.__get_fields("get_autocomplete_fields", request=request)
    
    # <-> Helpers <-> #
    
    def get_true_mixins(self) -> Generator[Type[AdminFieldsetMixin], None, None]:
        for mixin in self.mixins:
            if issubclass(mixin, AdminFieldsetMixin):
                yield mixin
    
    def get_mixin_fields(self, **kwargs) -> list:
        """
            Collects all fields from the mixins.
        :param kwargs: kwargs to be passed to the `get_mixin_fields` method
        :return: dict containing all fields as value and name as key
        """
        all_fields = []
        
        name: str
        value: list
        
        # Iterate through all fields from the mixins
        for mixin in self.get_true_mixins():
            instance = mixin()  # type: AdminFieldsetMixin
            
            # Get fields
            for name, fields in instance.get_mixin_fields(**kwargs).items():
                all_fields.append({
                    name: {
                        "fields": fields,
                        "name": instance.name
                    }
                })
        
        return all_fields
    
    def get_fieldsetslist(self, **kwargs) -> list:
        return self.__get_fields("get_fieldsetslist", **kwargs)
    
    def get_view_on_site_url(self, obj: Optional[ModelInstance] = None) -> Optional[str]:
        if obj:
            try:
                obj.url
            except (NotImplementedError, AttributeError):
                logging.warning(f"You forgot to implement some methods on `{model_verbose(obj)}`")
            else:
                return obj.reversed_url
        return


class AdminMixinsMixin(BaseAdminMixinsMixin, admin.ModelAdmin):
    pass
