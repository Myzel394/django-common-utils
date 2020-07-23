from collections import Iterable
from typing import List, Optional, Union


def flat_list(lst: list) -> list:
    flt_lst = []
    
    for value in lst:
        if isinstance(value, list):
            flt_lst.extend(flat_list(value))
        else:
            flt_lst.append(value)
    
    return flt_lst


class UniqueSortedDict(dict):
    def __getitem__(self, item):
        # sort dict
        sorted_dict = {k: v for k, v in sorted(self.items(), key=lambda x: x[0])}
        return sorted_dict[item]
    
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already in use!")
    
    def __iter__(self):
        for key, value in self.items():
            yield value


class FieldsetList:
    INSERT_STRING = "..."
    FORCE_INSERT_CHAR = "!"
    FORCE_INSERT_BEFORE = f"{FORCE_INSERT_CHAR}{INSERT_STRING}"
    FORCE_INSERT_AFTER = f"{INSERT_STRING}{FORCE_INSERT_CHAR}"
    
    def __init__(
            self,
            fields: list,
            name: str,
            appearance: Optional[str] = None,
            classes: list = [],
            description: str = "",
            order: int = 0,
    ):
        self.fields = fields
        self.appearance = appearance
        self.classes = classes
        self.name = name
        self.description = description
        self.order = order
    
    def __str__(self):
        return f"{self.appearance}: {str(self.fields)}"
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, item: int):
        if isinstance(item, int):
            return self.fields[item]
        raise KeyError("You can only slice using int!")
    
    def __add_field(self, value: Union[str, Iterable], index: Optional[int] = None):
        if type(value) is str:
            value: List[str] = [value]
        
        for val in value:
            if val not in self.fields:
                if index:
                    self.fields[index] = val
                else:
                    self.fields.append(val)
    
    def __setitem__(self, key: int, value):
        if isinstance(key, int):
            self.__add_field(value, key)
        raise KeyError("You can only set an value using an int as the key!")
    
    def __insert_fields(self, adds: Union[str, Iterable], insert: str):
        if isinstance(adds, str):
            adds = {adds}
        
        fields: list
        if insert in (fields := self.fields):
            index = fields.index(insert)
            # Get not already declared fields
            adds = [field for field in adds if field not in fields]
            
            # PERFORMANCE: Using `[index:index]` method of fields and adding `len` to index to avoid incrementing
            # index multiple times
            fields[index:index] = adds
            
            # If FORCE_INSERT_BEFORE is used, move it to original position
            if insert == self.FORCE_INSERT_BEFORE:
                # Get index of FORCE_INSERT_BEFORE
                insert_index = index + len(adds)
                
                # Copy insert to old position
                fields.insert(index, fields[insert_index])
                insert_index += 1  # Update index
                
                # Delete copied insert on new position
                del fields[insert_index]
            elif insert != self.FORCE_INSERT_AFTER:  # No need to check FORCE_INSERT_BEFORE again
                index += len(adds)  # Update index of INSERT_STRING
                del fields[index]
            
            # Update fields
            self.fields = fields
            
            return self
        raise KeyError(f'"{insert}" was not found in fields!')
    
    def append_fields(self, adds: Union[str, Iterable]):
        """
            Appends given fields to end of current fields.
        :param adds: If str, will be appended.
        If Iterable, will be extended.
        :return: self
        """
        self.__add_field(adds)
        
        return self
    
    def add_fields(self, fields: Union[str, Iterable], insert_prefix: str = ""):
        """
            Adds fields.
        :param fields: List, containing str as fields to be added
        :param insert_prefix: Prefix for the INSERT_STRING
        :return: self
        """
        
        def get_insert():
            own_fields = self.fields
            checking = [
                f"{insert_prefix}{self.INSERT_STRING}",
                self.INSERT_STRING,
                self.FORCE_INSERT_BEFORE,
                self.FORCE_INSERT_AFTER
            ]
            founds = [field for field in checking if field in own_fields]
            
            if founds:
                return founds[0]
            return
        
        if insert := get_insert():
            self.__insert_fields(fields, insert)
        else:
            self.append_fields(fields)
        
        return self
    
    def __add__(self, other: Union[str, Iterable]):
        self.append_fields(other)
        return self
    
    def __sub__(self, other: str):
        """
            Removes a field from fields.
        :param other: The field to be removed
        :return: self
        """
        self.fields.remove(other)
        return self
    
    def integrate(self, value: "FieldsetList"):
        """
            Extends fields and classes of the other FieldsetList.
        :param value: The other FieldsetList (This fields and classes will be extended to self's fields and classes)
        :return: self
        """
        self.__add_field(value.fields)
        self.classes.extend(value.classes)
        
        return self
    
    def clear_fields_copy(self) -> list:
        """
            Creates a cleared copy of fields.
        :return: The copied, cleared fields
        """
        fields = self.fields
        
        for field in fields:
            if self.INSERT_STRING in field:
                fields.remove(field)
        
        return fields
    
    def render(self) -> list:
        return [
            self.appearance, {
                "fields": self.fields,
                "classes": self.classes,
                "description": self.description
            }
        ]
    
    @property
    def flatten_fields(self):
        return flat_list(self.clear_fields_copy())


class Sections:
    def __init__(self, sets: list, move_fields: bool = False):
        self._fields = UniqueSortedDict()
        self.move_fields = move_fields
        
        for fieldset in sets:  # type: FieldsetList
            self.__add_fieldsetlist(fieldset)
    
    def get(self, value) -> Union[FieldsetList, list, None]:
        try:
            return self[value]
        except (KeyError, StopIteration):
            return None
    
    def __getitem__(self, item: Union[int, slice, str, list]) -> Union[FieldsetList, list]:
        """
            Returns a FieldsetList based on item.
        :param item: int, slice, str or list.
        If item is int, the first FieldsetList whose order matches will be returned.
        If item is slice, a list with FieldsetList with their orders in range will be returned.
        If item is str, the first FieldsetList whose name matches will be returned.
        If item ist list, the first FieldsetList whose fields matches (will be checked by converting both (item and
        the fields of the current FieldsetList) to a set).
        :return: FieldsetList or list containing FieldsetLists
        """
        field: FieldsetList
        
        # If item is int, return whose order matches with item
        if isinstance(item, int):
            return self._fields[item]
        
        # If item is slice, return whose order is in range with item
        elif isinstance(item, slice):
            order_range = range(item.start, item.stop, item.step)
            return [field for field in self._fields if field.order in order_range]
        
        # If item is str, return whose appearance matches with item
        elif isinstance(item, str):
            return next((field for field in self._fields if field.name == item))
        
        # If item is list, return whose field's matches with item
        elif isinstance(item, list):
            return next((field for field in self._fields if set(field.fields) == set(item)))
        
        raise KeyError("Slicing must be either a `slice` or an `int` object.")
    
    def __add_fieldsetlist(self, fieldset: FieldsetList) -> "Sections":
        # If order in use, move it to end
        if (fs_order := fieldset.order) not in self._fields:
            order = fs_order
        else:
            # Get last order number and add one to create a new unique order
            order = max([order for order in self._fields.keys()]) + 1
        
        # Check name duplication
        if self.get(fieldset.name):
            raise KeyError("Name already in use!")
        
        self._fields[order] = fieldset
        return self
    
    # noinspection SpellCheckingInspection
    def add_fieldsetlist(self, fieldsetlist: FieldsetList) -> "Sections":
        """
            Adds a FieldsetList to this Fieldset's fields.
        :param fieldsetlist: The FieldsetList which should be added
        :return: self
        """
        # If fieldset already exists, integrate
        if fieldset := self.get(fieldsetlist.name):
            fieldset.integrate(fieldsetlist)
        else:
            self.__add_fieldsetlist(fieldsetlist)
        
        return self
    
    def _add_dict_fields(self, fields: dict):
        for name, nknown in fields.items():
            try:
                # Get fieldset
                fieldset = self[name]  # type: FieldsetList
            except StopIteration as e:
                if self.move_fields:
                    fieldset = self[0]
                else:
                    raise e
            
            # Add fields
            if isinstance(nknown, dict):
                fieldset.add_fields(
                    fields=nknown["fields"],
                    insert_prefix=nknown["name"]
                )
            elif isinstance(nknown, list):
                fieldset.add_fields(nknown)
            else:
                raise ValueError("The value of the dict must be a dict or a list!")
        
        return self
    
    def add_fields(self, fields: Union[list, dict]):
        """
            Adds fields to the FieldsetLists.
        :param fields: A dict containing as the key the name of the FieldSetList and as value the list with fields.
        The value can also be a dict, but must follow this scheme:
            fields: List, containing fields that should be added.
            name: str, this is the name for the insert_string_prefix.
        If list, it must contain a dict applying the rules above.
        :return: self
        """
        
        if isinstance(fields, dict):
            self._add_dict_fields(fields)
        elif isinstance(fields, list):
            for dct in fields:  # type: dict
                self._add_dict_fields(dct)
        
        return self
    
    def remove_fields(self, other: FieldsetList):
        """
            Removes a FieldsetList from this Fieldset.
        :param other: The FieldsetList to be removed.
        :return: self
        """
        del self._fields[other]
        
        return self
    
    def clear(self):
        """
            Calls the `clear_fields_copy` method of all FieldsetLists and updates them.
        :return: self
        """
        for field in self._fields:  # type: FieldsetList
            field.clear_fields_copy()
        
        return self
    
    def render(self, clear_before_rendering: bool = True, /) -> list:
        """
            Returns the FieldsetLists to a fieldset-like list, usable for Django.
        :return: List, usable as fieldset for Django
        """
        if clear_before_rendering:
            self.clear()
        
        return [
            sets.render()
            for sets in self._fields  # type: FieldsetList
        ]
    
    @property
    def fieldsets(self):
        for fieldset in self._fields:  # type: FieldsetList
            yield fieldset
    
    @property
    def fields(self) -> list:
        """
            Returns a copy of all FieldsetList's fields from this Fieldset.
        :return: List containing all fields of all FieldsetLists of this Fieldset
        """
        sets: FieldsetList
        return [sets.fields for sets in self._fields.values()]
    
    @property
    def flatten_fields(self) -> list:
        """
            Returns a copy of all FieldsetList's fields flatten from this Fieldset.
        :return: list containing all fields flatten of all FieldsetLists of this Fieldset
        """
        sets: FieldsetList
        return flat_list([sets.flatten_fields for sets in self._fields.values()])
    
    @staticmethod
    def from_fieldset(fieldset: list) -> "Sections":
        """
            Creates a Fieldset class from a Django fieldset.
        :param fieldset: The fieldset from django
        :return: A Fieldset
        """
        prepared = []
        
        for sets in fieldset:  # type: tuple
            appearance = sets[0]
            data = sets[1]
            
            prepared.append({
                "appearance": appearance,
                **data
            })
        
        return Sections(prepared)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {' '.join([str(fs) for fs in self.fieldsets])}>"
