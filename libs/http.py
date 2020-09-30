import json

from django.http import HttpResponse

from tantan import settings


def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG is True:
        json_str = json.dumps(result,ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_str = json.dumps(result,ensure_ascii=False,separators=(',',':'))

    response = HttpResponse(content=json_str, content_type='application/json')

    return response