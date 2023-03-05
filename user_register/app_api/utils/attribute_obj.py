"""attribute obj"""
from .class_objects import MakeObj

custom_error1 = {
    "status": "Failed",
    "message": [
        {
            "field": "field",
            "error_code": "E0004",
            "message": "Already Exists, Please Choose another!",
        }
    ],
}

custom_error_obj1 = MakeObj.convert_to_obj(custom_error1)

custom_error = {"status": "Failed", "message": "message"}

custom_error_obj = MakeObj.convert_to_obj(custom_error)

custom_messages = {
    "E0003": {
        "field": "field",
        "error_code": "E0003",
        "message": "Invalid Data, Please try again!",
    },
    "E0005": {
        "field": "field",
        "error_code": "E0005",
        "message": "Missing data for required field.",
    },
    "E0008": {
        "field": "field",
        "error_code": "E0008",
        "message": "Invalid Type Data, Please try again!",
    },
    "E0001": {
        "field": "field",
        "error_code": "E0001",
        "message": "Value lower than the minimum length {}, Please try again!",
    },
    "E0002": {
        "field": "field",
        "error_code": "E0002",
        "message": "Value exceed the maximum length {}, Please try again!",
    },
    "E0004": {
        "field": "field",
        "error_code": "E0004",
        "message": "Already Exists, Please Choose another!",
    },
    "E0009": {
        "field": "account_id",
        "error_code": "E0009",
        "message": "account_id cannot be modified",
    },
    "E0010": {
        "field": "field",
        "error_code": "E0010",
        "message": "Unknown field, Please enter valid field!",
    },
    "E0011": {
        "field": "field",
        "error_code": "E0011",
        "message": "Unknown choice field, {}",
    },
    "E0012": {
        "error_code": "E0012",
        "message": "Token Expired",
    },
    "E0013": {
        "field": "field",
        "error_code": "E0013",
        "message": "Already exist, but is_active False in id {}",
    },
    "E0014": {
        "error_code": "E0014",
        "message": "{} {} : not active",
    },
    # "E0015": {
    #     "error_code": "E0015",
    #     "message": "{} is {}, but {} is {}.",
    # },
    # "E0016": {
    #     "error_code": "E0016",
    #     "message": "Atleast sales information or purchase information must be true",
    # },
    # "E0017": {
    #     "error_code": "E0017",
    #     "message": "{} must be lessthan {}",
    # },
    # "E0018": {
    #     "error_code": "E0018",
    #     "message": "{} {} {}",
    # },
}

custom_message_obj = MakeObj.convert_to_obj(custom_messages)
