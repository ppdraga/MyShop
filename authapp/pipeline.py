from social_core.exceptions import AuthForbidden

def save_user_profile (backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2" :
        if 'gender' in response.keys():
            if response['gender'] == 'male' :
                user.shopuserprofile.gender = 'M'
            else :
                user.shopuserprofile.gender = 'W'
        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']
        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']
        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18 :
                user.delete()
                raise AuthForbidden( 'social_core.backends.google.GoogleOAuth2' )
        user.save()
    return