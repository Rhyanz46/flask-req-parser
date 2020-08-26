from flask import abort, make_response, jsonify
from typing import List
from datetime import datetime, date


def result(data, code):
    return make_response(jsonify(data), code)


class ReqParser(object):
    def __init__(self, data_request):
        self.data_request = data_request
        self.type = type(data_request)
        self.__parsed = {}

    def append(self, key, value):
        self.__parsed.update({key: value})

    def get_parsed(self):
        return self.__parsed

    def parse(
            self, field, field_type, nullable: bool = False,
            length=float("inf"), enum: List = None, unique_from_model=None,
            before_process=None, after_process=None):

        is_dict = self.type == dict
        wrong_type = False
        wrong_len = False

        data_request = self.data_request
        if before_process is not None:
            data_request = before_process(data_request)
        if isinstance(None, self.type):
            if not nullable:
                msg = {
                    "message": 'you have to set a data'
                }
                abort(result(msg, 400))
                if after_process is not None:
                    value = after_process(data_request)
            return self.__parsed.update({field: None})

        if enum != None and type(enum) != list:
            raise ValueError("enum must be list, for '{}' field".format(field))

        if unique_from_model != None:
            must_field = {'model', 'field'}
            if type(unique_from_model) != dict:
                raise ValueError("unique_from_model must be dict, for '{}' field".format(field))
            if must_field != set(unique_from_model.keys()):
                raise ValueError("key must be {} for '{}' field".format(must_field, field))
            if len(unique_from_model.keys()) != 2:
                raise ValueError(
                    "expected {} keys, and we got {} keys, for '{}' field"
                        .format(len(must_field), len(unique_from_model.keys()), field)
                )

        if is_dict:
            value = data_request.get(field)
            if enum:
                if value not in enum:
                    msg = {
                        "message": 'value error for field {}'.format(field)
                    }
                    abort(result(msg, 400))

            if unique_from_model:
                model = unique_from_model['model']
                model_field = unique_from_model['field']
                if hasattr(model, model_field):
                    obj_model = getattr(getattr(model, 'query'), 'filter')(
                        getattr(model, model_field) == value).first()
                    if obj_model:
                        msg = {
                            "message": '{} with {}={} is already exist'.format(model.__tablename__, model_field,
                                                                               value)
                        }
                        abort(result(msg, 400))

            if not nullable:
                if isinstance(None, type(value)):
                    msg = {
                        "message": 'field {} it\'s can\'t be null'.format(field)
                    }
                    abort(result(msg, 400))
            else:
                if isinstance(None, type(value)):
                    if after_process is not None:
                        value = after_process(data_request)
                    return self.__parsed.update({field: value})
            if field_type == date:
                try:
                    value = datetime.strptime(value, "%d-%m-%Y").date()
                    wrong_type = False
                    wrong_len = False
                except:
                    msg = {
                        "message": 'for field {} date type format must be  : dd-mm-yyyy'.format(field)
                    }
                    abort(result(msg, 400))
            else:
                wrong_type = type(value) != field_type
                wrong_len = len(str(value)) > length

            if wrong_type:
                msg = {
                    "message": 'field {} it\'s must be {}'.format(field, field_type.__name__)
                }
                abort(result(msg, 400))
            if wrong_len:
                msg = {
                    "message": 'length of filed {} can\'t over {}'.format(field, length)
                }
                abort(result(msg, 400))
            if after_process is not None:
                value = after_process(data_request)
            self.__parsed.update({field: value})




