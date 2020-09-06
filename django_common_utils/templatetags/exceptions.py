import re
from typing import *

from django.template import Context, Node, NodeList, TemplateSyntaxError
from django.template.base import FILTER_SEPARATOR, Parser, Token
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


class ForNode(Node):
    child_nodelists = ('nodelist_loop', 'nodelist_empty')

    def __init__(self, loopvars, sequence, is_reversed, nodelist_loop, nodelist_empty=None):
        self.loopvars, self.sequence = loopvars, sequence
        self.is_reversed = is_reversed
        self.nodelist_loop = nodelist_loop
        if nodelist_empty is None:
            self.nodelist_empty = NodeList()
        else:
            self.nodelist_empty = nodelist_empty

    def render(self, context):
        if 'forloop' in context:
            parentloop = context['forloop']
        else:
            parentloop = {}
        with context.push():
            values = self.sequence.resolve(context, ignore_failures=True)
            if values is None:
                values = []
            if not hasattr(values, '__len__'):
                values = list(values)
            len_values = len(values)
            # Empty render
            if len_values < 1:
                return self.nodelist_empty.render(context)
            nodelist = []
            if self.is_reversed:
                values = reversed(values)
            num_loopvars = len(self.loopvars)
            unpack = num_loopvars > 1
            # Create a forloop value in the context.  We'll update counters on each
            # iteration just below.
            loop_dict = context['forloop'] = {'parentloop': parentloop}
            for i, item in enumerate(values):
                # Shortcuts for current loop iteration number.
                loop_dict['counter0'] = i
                loop_dict['counter'] = i + 1
                # Reverse counter iteration numbers.
                loop_dict['revcounter'] = len_values - i
                loop_dict['revcounter0'] = len_values - i - 1
                # Boolean values designating first and last times through loop.
                loop_dict['first'] = (i == 0)
                loop_dict['last'] = (i == len_values - 1)

                pop_context = False
                if unpack:
                    # If there are multiple loop variables, unpack the item into
                    # them.
                    try:
                        len_item = len(item)
                    except TypeError:  # not an iterable
                        len_item = 1
                    # Check loop variable count before unpacking
                    if num_loopvars != len_item:
                        raise ValueError(
                            "Need {} values to unpack in for loop; got {}. "
                            .format(num_loopvars, len_item),
                        )
                    unpacked_vars = dict(zip(self.loopvars, item))
                    pop_context = True
                    context.update(unpacked_vars)
                else:
                    context[self.loopvars[0]] = item

                for node in self.nodelist_loop:
                    nodelist.append(node.render_annotated(context))

                if pop_context:
                    # Pop the loop variables pushed on to the context to avoid
                    # the context ending up in an inconsistent state when other
                    # tags (e.g., include and with) push data to context.
                    context.pop()
        return mark_safe(''.join(nodelist))



@register.tag('fake_for')
def do_for(parser, token):
    # Ensures format
    bits = token.split_contents()
    if len(bits) < 4:
        raise TemplateSyntaxError("'for' statements should have at least four"
                                  " words: %s" % token.contents)

    is_reversed = bits[-1] == 'reversed'
    in_index = -3 if is_reversed else -2
    if bits[in_index] != 'in':
        raise TemplateSyntaxError("'for' statements should use the format"
                                  " 'for x in y': %s" % token.contents)

    invalid_chars = frozenset((' ', '"', "'", FILTER_SEPARATOR))
    loopvars = re.split(r' *, *', ' '.join(bits[1:in_index]))
    for var in loopvars:
        if not var or not invalid_chars.isdisjoint(var):
            raise TemplateSyntaxError("'for' tag received an invalid argument:"
                                      " %s" % token.contents)

    sequence = parser.compile_filter(bits[in_index + 1])
    nodelist_loop = parser.parse(('empty', 'endfor',))
    token = parser.next_token()
    if token.contents == 'empty':
        # Empty tag
        nodelist_empty = parser.parse(('endfor',))
        parser.delete_first_token()
    else:
        nodelist_empty = None
    return ForNode(loopvars, sequence, is_reversed, nodelist_loop, nodelist_empty)


class TryNode(Node):
    nodelist_try: NodeList
    nodelist_catch: Optional[NodeList]
    child_nodelists = ("nodelist_try", "nodelist_except")
    
    def __init__(
            self,
            nodelist_try: NodeList,
            nodelist_except: Optional[NodeList],
            catch_exceptions: Optional[List[str]] = None
    ):
        self.nodelist_try = nodelist_try
        self.nodelist_except = nodelist_except or NodeList()
        self.catch_exceptions = catch_exceptions
    
    def render(self, context: Context):
        nodelist = []
        
        with context.push():
            try:
                try_data = self.nodelist_try.render(context)
            except Exception as e:
                if \
                        type(self.catch_exceptions) is list and (
                                len(self.catch_exceptions) == 0
                                or e.__class__.__name__ in self.catch_exceptions
                        ):
                    nodelist.append(
                        self.nodelist_except.render(context)
                    )
                else:
                    raise e
            else:
                nodelist.append(
                    try_data
                )
                
        return mark_safe("".join(nodelist))
                    
                


@register.tag("try")
def try_func(parser: Parser, token: Token):
    nodelist_try: NodeList
    nodelist_except: Optional[NodeList] = None
    catch_exceptions: Optional[List] = None
    
    # Try
    nodelist_try: Token = parser.parse(("except", "endtry"))
    
    next_token = parser.next_token()
    next_token_name = next_token.contents.lstrip().split(" ")[0].lower()
    
    # Catch
    if next_token_name == "except":
        # Catch
        contents = next_token.contents.split(" ")[1:]
        
        if len(contents) > 0:
            catch_exceptions = contents
        else:
            catch_exceptions = []
        
        nodelist_except = parser.parse(("endtry", ))
    else:
        parser.parse(("endtry",))
    
    parser.next_token()
    
    return TryNode(
        nodelist_try=nodelist_try,
        nodelist_except=nodelist_except,
        catch_exceptions=catch_exceptions,
    )

