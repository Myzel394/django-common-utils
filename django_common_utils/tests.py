from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import TestCase
from typing import *

from django_common_utils.libraries.utils import  generate_image, model_verbose
from django_common_utils.libraries.utils.common import combine_fields


class LibrariesTest(TestCase):
    @staticmethod
    def render_template(html: str, context: Optional[Dict[str, Any]] = None):
        context = context or {}
        context = Context(context)
        return Template(html).render(context)
    
    def test_utils(self):
        # Common
        self.assertEqual(
            combine_fields({
                "field_1": ["a", "b"],
                "field_2": ["c", "d"]
            }, {
                "field_1": ["a", "b", "c"],
                "field_2": ["e"]
            }),
            {
                "field_1": ["a", "b", "c"],
                "field_2": ["c", "d", "e"]
            }
        )

        # Image
        self.assertEqual(
            generate_image(url="/my_image.jpg"),
            '<img src="/my_image.jpg" alt="" loading="lazy" style="background-color:rgba(0, 0, 0, 0)"  />'
        )
        self.assertHTMLEqual(
            generate_image(url="/my_image.jpg", attributes={
                "data-test": "test_value"
            }),
            '<img src="/my_image.jpg" alt="" loading="lazy" style="background-color:rgba(0, 0, 0, '
            '0)" data-test="test_value" />'
        )
        
        # Text
        assert model_verbose(User) == model_verbose("auth.User") == model_verbose(User.objects.all())
        
    def test_templatetags(self):
        first_html = """
            {% load exceptions math %}
            {% try %}
                {% divide 23 5 %}
            {% except ZeroDivisionError %}
                Catch block (will not be visible)
            {% endtry %}
            {% try %}
                {% divide 23 0 %}
            {% except ZeroDivisionError %}
                Catch block (one exceptions)
            {% endtry %}
            {% try %}
                {% divide 23 0 %}
            {% except %}
                Catch block (all exceptions)
            {% endtry %}
        """
        second_html = """
            {% load exceptions %}
            {% try %}
                {% divide 23 0 %}
            {% except AnExceptionThatHopefullyDoesNotExist %}
                Catch block (will raise error in Python)
            {% endtry %}
        """
        
        expected_first_html = """
            
            
                4
            
            
                Catch block (one exceptions)
            
            
                Catch block (all exceptions)
            
        """
        
        self.assertEqual(self.render_template(first_html), expected_first_html)
        self.assertRaises(ZeroDivisionError, lambda: self.render_template(second_html))
 
