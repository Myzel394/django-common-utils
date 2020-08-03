from dataclasses import dataclass
from typing import *

from .base import BaseHandlerMixin
from ..constants import AddAttributesDict, HandleOn, HTMLOptimizerDefault, TextOptimizerDefault, UnwrapDict
from ..optimizers.html import TextHTMLOptimizer
from ...typings import *


@dataclass
class HTMLOptimizerHandler(BaseHandlerMixin):
    space_after: str = TextOptimizerDefault.space_after
    space_before: str = TextOptimizerDefault.space_before
    no_space_before: str = TextOptimizerDefault.no_space_before
    no_space_after: str = TextOptimizerDefault.no_space_after
    ignore_for_digits: str = TextOptimizerDefault.ignore_for_digits
    
    def __init__(
            self,
            unwrap: Optional[UnwrapDict] = None,
            add_attributes: Optional[AddAttributesDict] = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.unwrap = unwrap if unwrap is not None else HTMLOptimizerDefault.unwrap
        self.add_attributes = add_attributes if add_attributes is not None else HTMLOptimizerDefault.add_attributes
    
    @staticmethod
    def HANDLE_ON():
        return {HandleOn.CREATION, HandleOn.SAVE}
    
    def handle(self, value: str):
        return TextHTMLOptimizer.html_remove_redundant_space(
            TextHTMLOptimizer.html_space_after_text(
                TextHTMLOptimizer.html_space_before_text(
                    TextHTMLOptimizer.html_add_attributes_to_tags(
                        TextHTMLOptimizer.html_unwrap(
                            "" if value is None else str(value),
                            unwrap=self.unwrap
                        ),
                        add_attributes=self.add_attributes
                    ),
                    space_before=self.space_before
                ),
                space_after=self.space_after,
                ignore_for_digits=self.ignore_for_digits
            ),
            no_space_after=self.no_space_after,
            no_space_before=self.no_space_before,
        )
