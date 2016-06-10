from copy import copy
from functools import wraps

from rest_framework.metadata import SimpleMetadata
from rest_framework.relations import RelatedField


class MyMetadata(SimpleMetadata):

    def get_field_info(self, field):

        if isinstance(field, RelatedField):
            def kill_queryset(f):
                @wraps(f)
                def wrapped(*args, **kwargs):
                    qs = f(*args, **kwargs)
                    if qs is not None:
                        qs = qs.none()
                    return qs
                return wrapped

            field = copy(field)
            field.get_queryset = kill_queryset(field.get_queryset)

        result = super(MyMetadata, self).get_field_info(field)

        if not result.get('choices'):
            result.pop('choices', None)
