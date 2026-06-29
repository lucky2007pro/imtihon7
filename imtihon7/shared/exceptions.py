from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'message': "Xatolik yuz berdi.",
            'data': response.data
        }
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_data['message'] = response.data['detail']
            else:
                # get the first value of the dict which is usually a list of errors
                first_error = list(response.data.values())[0]
                if isinstance(first_error, list) and len(first_error) > 0:
                    custom_data['message'] = str(first_error[0])
                elif isinstance(first_error, str):
                    custom_data['message'] = first_error
            
        response.data = custom_data

    return response
