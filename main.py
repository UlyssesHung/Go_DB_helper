#!/usr/bin/env Python2.7
# coding=UTF-8
import os
import re
import utility


def column_dealer(querycolumn):
    result = ''
    a = querycolumn.strip().split(' ')
    c_name = a[0]
    c_type = a[1]
    c_allow_null = True
    # created_at timestamp without time zone,
    if len(a) > 3:
        for i in range(len(a) - 1):
            if a[i].upper() == 'NOT' and a[i + 1].upper() == 'NULL':
                c_allow_null = False
    a_name = alphabet_dealer(c_name)
    # Get go type from column type
    go_data_type = ''
    if c_type in [
        'serial', 'serial4', 'smallserial', 'serial2', 'integer',
        'int', 'int4', 'smallint', 'int2'
    ]:
        go_data_type = 'int'
    elif c_type in ['bigserial', 'serial8', 'bigint', 'int8']:
        go_data_type = 'int64'
    elif c_type in ['text']:
        go_data_type = 'string'
    elif c_type in ['timestamp']:
        go_data_type = 'time.Time'
    elif c_type in ['bool']:
        go_data_type = 'bool'
    elif c_type in ['real', 'float4']:
        go_data_type = 'float32'
    elif c_type in ['float8']:
        go_data_type = 'float64'
    if c_allow_null is True and c_name != 'id':
        go_data_type = '*' + go_data_type
    if re.search('[^a-z]*id[^a-z]*', c_name) is not None:
        a_name = a_name.replace('Id', 'ID')
    item = utility.JsonItemClass()
    item.column_name = c_name
    item.attribute_name = a_name
    item.go_data_type = go_data_type
    return item


def alphabet_dealer(c_name):
    a = c_name.split('_')
    result = ''
    for v in a:
        if v == 'id':
            result += v.upper()
        elif v == 'ids':
            result += 'IDs'
        elif v == 'url':
            result += 'URL'
        else:
            result += v[0].upper() + v[1:]
    return result


def model_str(items):
    return '\n'.join(['{0}\t{1}\t`json:"{2}"`'.format(
        v.attribute_name, v.go_data_type, v.column_name) for v in items]) + '\n'


def selectx_rowscan_str(items):
    return ', '.join(['&item.{0}'.format(v.attribute_name) for v in items])


def insert_query_str(items):
    part1 = '\t\t' + ',\n\t\t'.join([v.column_name for v in items
                                     if v.attribute_name != 'ID'])
    part2 = ', '.join(['${0}'.format(k) for k, v in enumerate(items)
                       if v.attribute_name != 'ID'])
    return '(\n{0})\n\tVALUES ({1})'.format(part1, part2)


def insert_queryrow_str(items):
    return ', '.join(['item.{0}'.format(v.attribute_name) for v in items
                      if v.attribute_name != 'ID'])


def update_query_str(items):
    return ',\n\t\t'.join(['{0} = ${1}'.format(v.column_name, k + 1)
                           for k, v in enumerate(items)
                           if v.attribute_name != 'ID'])


def wrapper_str(items):
    return '\n'.join(['newitem.{0} = item.{0}'.format(v.attribute_name)
                      for v in items])


def sortby_comparedfunc_str(items):
    return ' else '.join(["""if columnName == "{0}" {{
        return typeCompareFunc(p1.{1}, p2.{1}, orderstr)
    }}""".format(v.column_name, v.attribute_name) for v in items
        if v.attribute_name != 'ID'])


alltxt = open("db_description.txt").read().lower()
tablecreatetxt = re.search(
    r'\[create\s{1}start\]((.|\n)*)\[create\s{1}end\]', alltxt).group(1)
tablename = re.search(
    r'create\s+table\s+([a-z|\_]+)\s+\(', tablecreatetxt).group(1)
modelname = alphabet_dealer(tablename)
instancename = modelname[0].lower() + modelname[1:]  # first character lower
columnbody = re.search(
    r'create\s+table\s+[a-z|\_]+\s+\(((.|\n)*)\)', tablecreatetxt).group(1)
column_items = [column_dealer(v) for v in columnbody.split(',')]

# Apply template
templatetxt = open("template.go.txt").read()
templatetxt = templatetxt.replace("table_create_demo", tablename)
templatetxt = templatetxt.replace("TableCreateDemo", modelname)
templatetxt = templatetxt.replace("tableCreateDemo", instancename)
templatetxt = templatetxt.replace("[model_str]", model_str(column_items))
templatetxt = templatetxt.replace(
    "[selectx_rowscan_str]", selectx_rowscan_str(column_items))
templatetxt = templatetxt.replace(
    "[insert_query_str]", insert_query_str(column_items))
templatetxt = templatetxt.replace(
    "[insert_queryrow_str]", insert_queryrow_str(column_items))
templatetxt = templatetxt.replace(
    "[update_query_str]", update_query_str(column_items))
templatetxt = templatetxt.replace("[wrapper_str]", wrapper_str(column_items))
templatetxt = templatetxt.replace("[sortby_comparedfunc_str]",
                                  sortby_comparedfunc_str(column_items))
open('result.go', 'w').write(templatetxt)


# c_names = re.findall(
#    r'\s*[\(|\,]{1}\s*([a-z|\_]+)\s+[' + '|'.join(a) + ']+', tablecreatetxt)
# print c_names
