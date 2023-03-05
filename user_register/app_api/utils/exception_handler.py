"""Custom exception handler"""

from marshmallow import ValidationError
import re
from .attribute_obj import custom_message_obj, custom_error_obj
from .class_objects import MakeObj


class ApiValidationError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    @property
    def messages_dict(self):
        return self.message


class SchemaValidator(object):
    """Validator for schema"""

    def __init__(self, response={}):
        """initialize"""

        self.response = response

    def isTrue(self, schema):
        """return True if schema is valid"""
        custom_messages = []
        try:
            validated_user_data = schema.load(self.response)
        except ValidationError as err:
            message = err.messages
            print("message::", message)
            for key in list(message.keys()):
                if "Must be one of" in message[key][0]:
                    custom_message_obj.E0011.field = key
                    initial_message = custom_message_obj.E0011.message
                    custom_message_obj.E0011.message = (
                        custom_message_obj.E0011.message.format(message[key][0])
                    )
                    custom_messages.append(
                        MakeObj.convert_to_dict(custom_message_obj.E0011)
                    )
                    custom_message_obj.E0011.message = initial_message
                    continue
                if "String does not match expected pattern." in message[key]:
                    custom_message_obj.E0003.field = key
                    custom_messages.append(
                        MakeObj.convert_to_dict(custom_message_obj.E0003)
                    )
                    continue
                if "Unknown field." in message[key]:
                    custom_message_obj.E0010.field = key
                    custom_messages.append(
                        MakeObj.convert_to_dict(custom_message_obj.E0010)
                    )
                    continue
                if "Missing data for required field." in message[key]:
                    custom_message_obj.E0005.field = key
                    custom_messages.append(
                        MakeObj.convert_to_dict(custom_message_obj.E0005)
                    )
                    continue
                if "Not a valid" in message[key][0]:
                    custom_message_obj.E0008.field = key
                    custom_messages.append(
                        MakeObj.convert_to_dict(custom_message_obj.E0008)
                    )
                    continue
                if "Length must" in message[key][0]:
                    data_len = len(self.response[key])
                    len_range = re.findall(r"[0-9]+", message[key][0])
                    if data_len < int(len_range[0]):
                        custom_message_obj.E0001.field = key
                        initial_message = custom_message_obj.E0001.message
                        custom_message_obj.E0001.message = (
                            custom_message_obj.E0001.message.format(len_range[0])
                        )
                        custom_messages.append(
                            MakeObj.convert_to_dict(custom_message_obj.E0001)
                        )
                        custom_message_obj.E0001.message = initial_message
                    elif data_len > int(len_range[1]):
                        custom_message_obj.E0002.field = key
                        initial_message = custom_message_obj.E0002.message
                        custom_message_obj.E0002.message = (
                            custom_message_obj.E0002.message.format(len_range[1])
                        )
                        custom_messages.append(
                            MakeObj.convert_to_dict(custom_message_obj.E0002)
                        )
                        custom_message_obj.E0002.message = initial_message
                    continue
            custom_error_obj.message = custom_messages
            return MakeObj.convert_to_dict(custom_error_obj), 400
        return validated_user_data
