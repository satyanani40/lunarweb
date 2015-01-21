import os


    # Running on local machine. Let's just use the local mongod instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'test'
MONGO_PASSWORD = 'test'
MONGO_DBNAME = 'test'

URL_PREFIX = 'api'


TOKEN_SECRET = os.environ.get('SECRET_KEY') or 'JWT Token Secret String'


    # let's not forget the API entry point (not really needed anyway)
    #SERVER_NAME = '127.0.0.1:5000'

XML = False
# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
people = {
    # 'title' tag used in item links.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'schema': {
        'name': {
            'type': 'dict',
            'schema': {
                'first': {
                    'type': 'string',
                    'minlength': 1,
                    'maxlength': 10,
                },
                'last': {
                    'type': 'string',
                    'minlength': 1,
                    'maxlength': 15,
                    'unique': True,
                },	
                'title': {
                    'type': 'string'
                }
            }
        },
        'email': {
            'type': 'string',
            'minlength': 1,
            'required': True,
            'unique': True,
        },
	      'username': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 25,
            'unique': True,
        },

	      'password': {
            'type': 'string'
        },
	      'password_test': {
            'type': 'string'
        },
        'role': {
            'type': 'string',
            'default': 'normal',
            'allowed': ["admin", "normal", "test"],
        },
        'gender': {
            'type': 'string',
        },
        'location': {
            'type': 'dict',
            'schema': {
                'street': {'type': 'string'},
                'city': {'type': 'string'},
                'state': {'type': 'string'},
                'zip': {'type': 'string'}
            },
        },
        'picture': {
            'type': 'dict',
            'schema': {
                'large': {'type': 'string'},
                'medium': {'type': 'string'},
                'thumbnail': {'type': 'string'}
            },
        },
        'born': {
            'type': 'string',
        },
        'phone': {
            'type': 'string',
        },
        'notifications': {
            'type': 'dict',
            'schema': {
                'friend-requests': {
                    'type': 'list',
                    'schema': {
                        'type': 'objectid',
                        'unique': True,
                        'data_relation': {
                            'resource': 'people',
                            'embeddable': True
                        }
                    }
                },
                'updates': {'type': 'string'}
            },
        },
        'friends': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'people',
                    'embeddable': True
                }
            }
        }
    }
}

posts = {
    'item_title': 'post',
    #'url': 'people/<regex("[a-f0-9]{24}"):author>/posts',
    'url' : 'people/posts',

    'schema': {

        'author': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                     'resource': 'people',
                     'field': '_id',
                     'embeddable': True
            },
        },
        'type': {
            'type': 'string',
            'allowed': ["text", "image", "video"],
        },
        'content': {
            'type': 'string',
            'required': True
        },
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            }
        },
        'keywords': {
            'type': 'list',
        },

    }
}

searchActivity = {
    'item_title': 'searchActivity',
    'url' : 'people/searchActivity',

    'schema': {
        'content': {
            'type': 'string',
            'required': True,
            'unique':True
        },
        'author': {
            'type': 'objectid',
            'data_relation': {
                     'resource': 'people',
                     'field': '_id',
                     'embeddable': True
            },
        },

    }
}
# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'people': people,
    'posts': posts,
    'searchActivity': searchActivity
    }
