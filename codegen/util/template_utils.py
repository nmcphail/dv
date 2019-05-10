import re
from django.template import loader

def render_template(template_name, ctx=None):
        text = loader.render_to_string(template_name, context=ctx)
        regex = r",[\n]*"
        text = re.sub(regex, ',\n', text)
        regex = r", [\n|\n\r]*"
        text = re.sub(regex, ',\n', text)
#        print(text)

        return text
