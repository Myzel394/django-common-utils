from types import FunctionType
from typing import *

import htmlmin
from bs4 import BeautifulSoup, Tag

from .text import TextOptimizer
from ..constants import AddAttributesDict, HTMLOptimizerDefault, UnwrapDict
from ...typings import Kwargs
from ...utils import iteration


class TextHTMLOptimizer:
    """
    Optimizes a given string. Accepts text/html
    """
    
    # Dictionary containing as key a list with strings which tags should be unwrapped, the value is a list
    # containing strings with tags which triggers the unwrap action
    
    @staticmethod
    def minify_html(html: str, opts: Optional[Kwargs] = None) -> str:
        if opts is None:
            opts = HTMLOptimizerDefault.minify_opts
        
        return htmlmin.minify(html, **opts)
    
    @staticmethod
    def _change_text(soup: BeautifulSoup, func: FunctionType, *args, **kwargs) -> BeautifulSoup:
        for element in soup.find_all():  # type: Tag
            if len(element.find_all()) > 0:
                continue
            
            new_text = func(element.get_text(), *args, **kwargs)
            element.string = new_text
        
        return soup
    
    @classmethod
    def html_remove_redundant_space(cls, html: str, *args, **kwargs) -> str:
        soup = BeautifulSoup(html, "html.parser")
        cls._change_text(soup, TextOptimizer.remove_redundant_space, *args, **kwargs)
        return str(soup)
    
    @classmethod
    def html_space_after_text(cls, html: str, *args, **kwargs) -> str:
        soup = BeautifulSoup(html, "html.parser")
        cls._change_text(soup, TextOptimizer.space_after_text, *args, **kwargs)
        return str(soup)
    
    @classmethod
    def html_space_before_text(cls, html: str, *args, **kwargs) -> str:
        soup = BeautifulSoup(html, "html.parser")
        cls._change_text(soup, TextOptimizer.space_before_text, *args, **kwargs)
        return str(soup)
    
    @staticmethod
    def html_unwrap(html: str, unwrap: Optional[UnwrapDict] = None) -> str:
        """
        Unwraps html tags.
        Example:
            input: <p><img src="image.jpg" /></p>
            self.unwrap: {
                "p": "img"
            }
            output: <img src="image.jpg" />
        """
        
        if unwrap is None:
            unwrap = HTMLOptimizerDefault.unwrap
        
        soup = BeautifulSoup(html, "html.parser")
        
        for unwrap, trigger in iteration.ensure_dict(unwrap, str, str):
            for element in soup.find_all(unwrap):
                if element.find_all(trigger, recursive=False):
                    element.unwrap()
        
        return str(soup)
    
    @staticmethod
    def html_add_attributes_to_tags(html: str, add_attributes: Optional[AddAttributesDict] = None) -> str:
        """Adds attributes to html tags"""
        
        if add_attributes is None:
            add_attributes = HTMLOptimizerDefault.add_attributes
        
        soup = BeautifulSoup(html, "html.parser")
        
        for tag, attributes in iteration.ensure_dict(add_attributes, str, dict):
            for element in soup.find_all(tag):
                for key, value in iteration.ensure_dict(attributes, str, str):
                    element[key] = value
        
        return str(soup)
