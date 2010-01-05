from django.contrib.contenttypes.models import ContentType


def get_object(obj_ct, obj_id):
    type = ContentType.objects.get(pk = obj_ct)
    model = type.model_class()
    obj = model.objects.get(pk = obj_id)

    return obj

def get_model_class(ct_id):
    return ContentType.objects.get(pk=ct_id).model_class()