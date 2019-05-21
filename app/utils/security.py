from functools import wraps
from datetime import datetime
from flask import request, make_response, jsonify
import re

ERROR_CODE_MAPPER = {
    # Authentication's Errors
    'AUT_01': 'Authorization code is empty.',
    'AUT_02': 'Access Unauthorized.',

    # Pagination's Errors
    'PAG_01': 'The order is not matched "field,(DESC|ASC)".',
    'PAG_02': 'The field of order is not allow sorting.',

    # User's Errors
    'USR_01': 'Email or Password is invalid.',
    'USR_02': 'The field(s) are/is required.',
    'USR_03': 'The email is invalid.',
    'USR_04': 'The email already exists.',
    'USR_05': 'The email doesn\'t exist.',
    'USR_06': 'this is an invalid phone number.',
    'USR_07': 'this is too long <FIELD NAME>.',
    'USR_08': 'this is an invalid Credit Card.',
    'USR_09': 'The Shipping Region ID is not number',

    # Category's Errors
    'CAT_01': 'Don\'t exist category with this ID.',

    # Department's Errors
    'DEP_01': 'The ID is not a number.',
    'DEP_02': 'Don\'exist department with this ID.'

}

class Security:
    EMAIL_REGEX = re.compile(
        r"^[\-a-zA-Z0-9_]+(\.[\-a-zA-Z0-9_]+)*@[a-z]+\.com\Z", re.I | re.UNICODE)
    
    @staticmethod
    def validator(rules):
        """
        :rules: list -  The sets of keys and rules to be applied
        example: [username|required:max-255:min-120, email|required:email]
        """
        
        def real_validate_request(f):
            
            @wraps(f)
            def decorated(*args, **kwargs):
                if not request.json:
                    return make_response(jsonify({'msg':'Bad Request - Request Must be JSON Formatted'})), 400
                
                payload = request.get_json()

                errors = {}
                
                if payload:
                    #Loop through all validation rules
                    for rule in rules:
                        rule_array = rule.split('|')
                        
                        request_key = rule_array[0]
                        validators = rule_array[1].split(':')
                            
                        # If the key is not in the request payload, and required is not part of the validator rules,
                        # Continue the loop to avoid key errors.
                        if request_key not in payload and 'required' not in validators:
                            continue
                        
                        #Loop all validators specified in the current rule
                        for validator in validators:
                            
                            if validator == 'int' and type(payload.get(request_key)) is str and not payload.get(request_key).isdigit():
                                error_msg = Security.error_msg(None, request_key, '{} must be integer'.format(request_key))
                                errors.__setitem__(request_key, error_msg)
                            
                            if validator == 'float':
                                try:
                                    float(payload.get(request_key))
                                except Exception as e:
                                    error_msg = Security.error_msg(None, request_key,
                                                                   '{} must be float'.format(request_key))
                                    errors.__setitem__(request_key, error_msg)
                            
                            if (validator == 'required' and request_key not in payload) or not payload.get(request_key):
                                error_code = 'USR_02' if request_key == 'email' else None
                                error_msg = Security.error_msg(error_code, request_key, 'The field(s) are/is required.')
                                errors.__setitem__(request_key, error_msg)
                            
                            if validator.find('max') > -1:
                                max_value = int(validator.split('-')[1])
                                if int(payload.get(request_key)) > max_value:
                                    error_msg = Security.error_msg(
                                        None,
                                        request_key,
                                        '{} can only have a max value of {}'.format(request_key, max_value)
                                                                       )
                                    errors.__setitem__(request_key, error_msg)
                            
                            if validator.find('min') > -1:
                                min_value = int(validator.split('-')[1])
                                if int(payload.get(request_key)) < min_value:
                                    errors.__setitem__(request_key, 'Bad Request - {} can only have a min value of {}'.format(request_key, min_value))
                            
                            if validator.find('length') > -1:
                                length_value = int(validator.split('-')[1])
                                if len(str(payload.get(request_key))) > length_value:
                                    error_msg = Security.error_msg(
                                        None,
                                        request_key,
                                        '{} can only have a len of {}'.format(request_key, length_value)
                                    )
                                    errors.__setitem__(request_key, error_msg)
                                
                            if validator == 'exists':
                                import importlib
                                from app.utils import to_pascal_case
                                
                                repo_name = rule_array[2]
                                column_name = rule_array[3]
                                
                                rep = 'app.repositories.{}_repo'.format(repo_name)
                                mod = importlib.import_module(rep)
                                repo_class = getattr(mod, '{}Repo'.format(to_pascal_case(repo_name)))
                                repo = repo_class()
                                
                                if type(payload.get(request_key)) == int:
                                    v = repo.find_first(**{column_name: payload.get(request_key)})
                                        
                                    if not v:
                                        error_msg = Security.error_msg(
                                            None,
                                            request_key,
                                            '{} contains invalid {}(s) for {} table '.format(
                                                request_key, column_name, repo_name)
                                        )
                                        errors.__setitem__(request_key, error_msg)

                                if type(payload.get(request_key)) == list:
                                    for val in payload.get(request_key):
                                        v = repo.find_first(**{column_name:val})
                                        
                                        if not v:
                                            error_msg = Security.error_msg(
                                                None,
                                                request_key,
                                                '{} contains invalid {}(s) for {} table '
                                                    .format(request_key, column_name,
                                                            repo_name)
                                            )
                                            errors.__setitem__(request_key, error_msg)

                            if validator == 'date':
                                try:
                                    datetime.strptime(payload.get(request_key), '%Y-%m-%d')
                                except Exception as e:
                                    error_msg = Security.error_msg(
                                        None,
                                        request_key,
                                        '{} should be valid date. Format: YYYY-MM-DD'.format(request_key)
                                    )
                                    errors.__setitem__(request_key, error_msg)

                            if validator == 'list' and type(payload.get(request_key)) is not list:
                                error_msg = Security.error_msg(
                                    None,
                                    request_key,
                                    '{} must be a list'.format(request_key)
                                )
                                errors.__setitem__(request_key, error_msg)

                            if validator == 'list_int':
                                if type(payload.get(request_key)) is not list:
                                    error_msg = Security.error_msg(
                                        None,
                                        request_key,
                                        '{} must be a list'.format(request_key)
                                    )
                                    errors.__setitem__(request_key, error_msg)

                                for val in payload.get(request_key):
                                    if type(val) is not int:
                                        error_msg = Security.error_msg(
                                            None,
                                            request_key,
                                            '[{}] in list must be integer'.format(val)
                                        )
                                        errors.__setitem__(request_key, error_msg)

                            # Validate email
                            error_msg = Security.validate_email(validator, request_key, payload.get(request_key))
                            errors.__setitem__(request_key, error_msg) if error_msg else None

                            # Validate value already exists
                            error_msg = Security.check_if_exists(validator, request_key, payload.get(request_key))
                            errors.__setitem__(request_key, error_msg) if error_msg else None

                if errors:
                    return make_response(jsonify({'error': [error for error in errors.values()]})), 400

                return f(*args, **kwargs)
            
            return decorated
        
        return real_validate_request

    @classmethod
    def validate_email(cls, validator, key, value):

        if value and validator == 'email':
            if not cls.EMAIL_REGEX.match(value):
                msg = "The email is invalid."
                return Security.error_msg('USR_03', key, msg)

    @classmethod
    def check_if_exists(cls, validator, key, value):

        validator, *other_rules = validator.split('_')

        if value and validator == 'ifExists':
            model_name, column_name = other_rules
            import importlib
            from app.utils.snake_case import SnakeCaseConversion

            mod = importlib.import_module('app.repositories.{}_repo'.format(SnakeCaseConversion.camel_to_snake(model_name)))
            repo = getattr(mod, f'{model_name}Repo')()
            repo_value = repo.find_first(**{column_name: value})
            msg = f"{model_name} with the {key} '{value}' already exists."

            error_code = "USR_04" if column_name == 'email' else None

            return Security.error_msg(error_code, key, msg) if repo_value else None

    @staticmethod
    def error_msg(error_code, key, msg, body='body', status=400):

        return {
            "status": status,
            "code": "{}".format(error_code),
            "message": "{}".format(msg),
            "field": "{}".format(key),
            "in": body
        }
