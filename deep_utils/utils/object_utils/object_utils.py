from argparse import Namespace
from typing import Union


def get_attributes(obj) -> dict:
    """
    Gets the attributes of an object not the methods.
    :param obj:
    :return:
    """
    out = dict()
    for key in dir(obj):
        val = getattr(obj, key)
        if (key.startswith("__") and key.endswith("__")) or type(val).__name__ == "method":
            continue
        else:
            out[key] = val
    return out


def update_obj_params(obj_instance: object, args: Union[dict, Namespace]):
    """
    This func/method is used for updating parameters of a class especially a config class with input arguments
    :param obj_instance:
    :param args:
    :return:
    """
    if isinstance(args, Namespace):
        variables = vars(args)
    elif isinstance(args, dict):
        variables = args
    else:
        raise ValueError()
    for k, v in variables.items():
        if hasattr(obj_instance, k):
            setattr(obj_instance, k, v)
        else:
            raise ValueError(f"value {k} is not defined in {obj_instance.__class__.__name__}")
