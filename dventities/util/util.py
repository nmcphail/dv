from ..models import *

def create_stage_table_field_from_hdbsql_output(field_name, field_type, field_length ):
    stf = StageTableField()
    stf.field_name = field_name
    if 'varchar' in field_type.lower():
        stf.field_type = 'string'
        stf.field_length = int(field_length)
        return stf

    if 'decimal' in field_type.lower():
        parts = field_length.split(',')
        if len(parts) == 2:
            precision = parts[0]
            scale = parts[1]
        else:
            precision=parts[0]
            scale=0
            
        stf.field_type = 'float'
        stf.field_precision = precision
        stf.field_scale = scale
        return stf

    if 'int' in field_type.lower():
        stf.field_type = 'int'
        return stf

    ft = field_type.lower()
    stf.field_type = ft
    return stf


def create_stage_table_from_hdbsql_output(hdbsql_output):
    schema = None
    table_name = None
    lines = hdbsql_output.split('\n')
    fields = []
    
    for line in lines:

        line = line.strip()
        if 'Column Name,Type,Length' in line:
            continue # These are the field headings

        if line.startswith('Table'):
            l = line.replace('Table ', '')
            l = l.replace('"', '')
            schema = l.split('.')[0]
            table_name = l.split('.')[1]
            continue
            #print(schema, table_name)

        if len(line) == 0:
            continue

        line = line.replace('"', '')
        parts = line.split(',')

        f = create_stage_table_field_from_hdbsql_output(
            field_name=parts[0],
            field_type=parts[1],
            field_length=parts[2] )
        
        fields.append(f)

    st = StageTable.objects.all().filter(name=table_name).first()
    if st is None:
        st = StageTable(name=table_name, schema=schema)
        st.clean()
        st.save()

    for f in fields:
        stf = st.stagetablefield_set.all().filter(field_name=f.field_name).first()
        if stf is None:
            stf = f
            stf.stage_table = st
            stf.clean()
            stf.save()
            
    return st    
    #print(st)
        #print(len(line))
        
    
