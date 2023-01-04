'''
Get the user id request parameter passed from serializer
'''
def get_created_by(req):
    '''
    Validate user is authenticate or not
    '''
    request = req.get('request', None)
    if not request.user.is_anonymous:
        return request.user
    else:
        return ''
