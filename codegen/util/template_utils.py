import re
from django.template import loader
import sqlparse

def render_template(template_name, ctx=None, format_sql=False):
        text = loader.render_to_string(template_name, context=ctx)
        if format_sql:
            text = sqlparse.format (text, reindent=True, keyword_case='upper')
        return text
        #regex = r",[\n]*"
        #text = re.sub(regex, ',\n', text)
        #regex = r", [\n|\n\r]*"
        #text = re.sub(regex, ',\n', text)
#        print(text)

        #return text
