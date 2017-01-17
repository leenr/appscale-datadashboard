from flask import request


def build_url_part(kind_name, is_passed):
    if kind_name.endswith('y'):
        kind_name_plural = kind_name[:-1] + 'ies'
    else:
        kind_name_plural = kind_name + 's'

    return ('/{kind_name_plural}' + ('/<string:{kind_name}>' if is_passed else '')).format(kind_name=kind_name, kind_name_plural=kind_name_plural)

def build_chain_urls(*kinds):
    passed_kinds, current_kind = kinds[:-1], kinds[-1]

    base = ''.join([build_url_part(passed_kind, True) for passed_kind in passed_kinds])

    res = [base + build_url_part(current_kind, False) + '/']
    return res
