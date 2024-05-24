from datetime import datetime
from typing import Union, Optional, Any

from .admins import Admin
from .user import User
from .flights import Flight
from .tournaments import Tournament
from .hole import Hole
from .score import Score, TotalScore

OBJS = (
    Admin,
    User,
    Flight,
    Tournament,
    Hole,
    Score,
    TotalScore,
)


def serializer(
        target: Optional[Union[*OBJS]] = None,
        result_dict: dict = None,
        k: str = None,
        v: Any = None,
):
    if isinstance(target, list):
        result_list = []
        for i_target in target:
            result_dict = serializer(target=i_target)
            result_list.append(result_dict)
        return result_list
    if isinstance(target, str):
        return target
    if result_dict is None:
        result_dict = {}
    if target:
        if isinstance(target, OBJS):
            target_dict = target.__dict__
            for k, v in target_dict.items():
                result_dict = serializer(result_dict=result_dict, k=k, v=v)
    if v:
        if isinstance(v, (str, int, float, datetime)):
            result_dict[k] = v
        if isinstance(v, (list, tuple)):
            result_dict[k] = []
            for elem in v:
                result = serializer(target=elem)
                result_dict[k].append(result)
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                result_dict = serializer(result_dict=result_dict, k=sub_k, v=sub_v)
    if k and not v:
        result_dict[k] = v
    return result_dict
