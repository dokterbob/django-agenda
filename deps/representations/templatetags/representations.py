
from django.template import loader, Node, TemplateSyntaxError
from django import template
from django.template.context import Context
OBJECT_VAR_NAME='representation_object_varOUIAOIUAOUI'
register = template.Library()
def get_representation_content(model, representation, context=None):
    opts = model._meta
    label = "%s.%s" % (opts.app_label, opts.object_name.lower())
    t = loader.get_template("representations/%s/%s" % (label,representation))

    if context is None:
        context = Context()

    context[OBJECT_VAR_NAME] = model
        
    return t.render(context)
    
class DefineObjectNode(Node):
    def __init__(self, object_name_exp):
        self.object_name_exp = object_name_exp

    def render(self, context):
        object_name = self.object_name_exp.resolve(context)
        context[object_name] = context[OBJECT_VAR_NAME]
        return ""
    
def do_defineobject(parser, token):
    bits = token.contents.split()

    if len(bits) != 3 and bits[1] != 'as':
        raise TemplateSyntaxError("Proper syntax is {%% %s as [varname]" % (bits[0],))
    
    return DefineObjectNode(parser.compile_filter(bits[2]))

class RepresentNode(Node):
    def __init__(self, model_name, model_exp, representation_exp):
        self.model_name = model_name
        self.model_exp = model_exp
        self.representation_exp = representation_exp

    def render(self, context):
        model = self.model_exp.resolve(context)
        representation = self.representation_exp.resolve(context)
        
        try:
            opts = model._meta
        except AttributeError:
            raise TemplateSyntaxError("%s is not a model" % (self.model_name,))


        return get_representation_content(model, representation, context=context)

                                
def do_represent(parser, token):
    """
    This tag takes a model and passes it and the context to
    a template in the following location:
    
    representations/app_label.object_name/[template]
    {% represent [model] as "[template]" %}

    This allows you to have the same representation for the object in numerous
    templates.

    This also allows you to have a list of mixed content types and if they all have
    representation templates made, you display them all in the same list.

    For instance you can have a list of videos, photes, blog entries and news stories
    and if all of them has a representation of "summary.html" you could make a single
    list of all the objects.
    """
    bits = token.contents.split()
    try:
        assert len(bits) == 4 and bits[2] == 'as', "Tag format is: {%% %s [model] as [template_name] %%}" % (bits[0])
    except AssertionError, e:
        raise TemplateSyntaxError(str(e))
    
    return RepresentNode(bits[1],
                         parser.compile_filter(bits[1]),
                         parser.compile_filter(bits[3])
                         )

register.tag('represent', do_represent)
register.tag('define_object', do_defineobject)
#register.filter('represent_as', get_representation_content)
