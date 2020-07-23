import re

from ...handlers import TextOptimizerDefault


class TextOptimizer:
    """
    Optimizes a given string. Accepts text/plain.
    """
    
    @staticmethod
    def remove_redundant_space(
            text: str,
            no_space_after: str = TextOptimizerDefault.no_space_after,
            no_space_before: str = TextOptimizerDefault.no_space_before
    ) -> str:
        return re.sub(
            rf"([{no_space_after}])\s+",
            r"\1",
            re.sub(
                rf'\s+([{no_space_before}])',
                r"\1",
                re.sub(r"\s\s+", " ", text)
            )
        )
    
    @staticmethod
    def space_after_text(
            text: str,
            space_after: str = TextOptimizerDefault.space_after,
            ignore_for_digits: str = TextOptimizerDefault.ignore_for_digits
    ) -> str:
        return re.sub(
            rf"(?<=[{space_after}])(?=[^\s])(?<![\d{ignore_for_digits}](?=\d))", " ", text
        )
    
    @staticmethod
    def space_before_text(
            text: str,
            space_before: str = TextOptimizerDefault.space_after
    ) -> str:
        return re.sub(
            rf"(?<=[^\s])(?=[{space_before}])", " ", text
        )
