from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor

import md5

def get_hexdigest(algorithm, salt, raw_password):
    ''' Implementation for hex digest '''

    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def encrypt_password(password):
    ''' encryption algorithm md5 or sha1 '''
    
    algo = 'sha1'
    salt = get_hexdigest(algo, str(123456), str(123456))[:5]
    hsh = get_hexdigest(algo, salt, password)
    return '%s$%s$%s' % (algo, salt, hsh)
	



    
    