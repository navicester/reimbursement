from django.http import HttpResponse, HttpResponseRedirect
import csv
import codecs
from django.utils.encoding import force_str, force_text
from django.db import models

def gen_csv(model, qs, filename, fields_display, fields_fk, fields_datetime, excludes, fields_multiple=None):
        response = HttpResponse(content_type='text/csv')        
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        response.write(codecs.BOM_UTF8) # add bom header
        writer = csv.writer(response)
        print excludes

        row = []
        # fields_display = [ "use_condition", ]
        # fields_fk = ["equipment",  ]
        # fields_datetime = ["updated","completed_time", ]
        for field in model._meta.get_fields():
            if field.name in excludes:
                continue
            print field.name
            row.append(field.verbose_name)
        writer.writerow(row)

        for obj in qs:
            row = []
            for field in model._meta.get_fields():
                if field.name in excludes:
                    continue
                    
                #row.append(field.value_to_string(obj).encode('utf8'))
                value = getattr(obj, field.name) 
                if value:
                    if field.name in fields_datetime:
                        if isinstance(field, models.DateTimeField):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            value = value.strftime('%Y-%m-%d')                        
                    elif field.name in fields_display:
                        value = obj._get_FIELD_display(field)
                    elif field.name in fields_fk:
                        value = force_text(value, strings_only=True)
                    elif fields_multiple and field.name in fields_multiple:
                        str = "{0}{1}()".format("obj.get_",field.name)
                        value = eval(str)
                    value = "%s" %  (value)
                    if fields_multiple and field.name in fields_multiple:
                        row.append(value)
                    else:
                        row.append(value.encode('utf8'))
                else:
                    row.append("")
            writer.writerow(row)    

        return response
