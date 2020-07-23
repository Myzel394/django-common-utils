import re
from dataclasses import dataclass

from .base import BaseHandlerMixin
from ..constants import HandleOn, TextOptimizerDefault

__all__ = [
    "RegexHandler", "WhiteSpaceStripHandler", "TextOptimizerHandler"
]

from ..optimizers.text import TextOptimizer


class RegexHandler(BaseHandlerMixin):
    PATTERN = ""
    REPLACEMENT = " "
    
    @staticmethod
    def HANDLE_ON():
        return {HandleOn.CREATION, HandleOn.SAVE}
    
    def handle(self, value: str) -> str:
        return re.sub(self.__class__.PATTERN, self.__class__.REPLACEMENT, value)


class WhiteSpaceStripHandler(RegexHandler):
    PATTERN = r"\s+"
    REPLACEMENT = " "
    
    def handle(self, value: str) -> str:
        return super().handle(value).lstrip().rstrip()


@dataclass
class TextOptimizerHandler(BaseHandlerMixin):
    space_after: str = TextOptimizerDefault.space_after
    space_before: str = TextOptimizerDefault.space_before
    no_space_before: str = TextOptimizerDefault.no_space_before
    no_space_after: str = TextOptimizerDefault.no_space_after
    ignore_for_digits: str = TextOptimizerDefault.ignore_for_digits
    
    @staticmethod
    def HANDLE_ON():
        return {HandleOn.CREATION, HandleOn.SAVE}
    
    def handle(self, value: str) -> str:
        return TextOptimizer.space_before_text(
            TextOptimizer.space_after_text(
                TextOptimizer.remove_redundant_space(
                    value,
                    no_space_after=self.no_space_after,
                    no_space_before=self.no_space_before
                ),
                space_after=self.space_after,
                ignore_for_digits=self.ignore_for_digits,
            ),
            self.space_before
        )
