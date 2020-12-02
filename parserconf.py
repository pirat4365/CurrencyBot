from configparser import ConfigParser


def conf_BD(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]

    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def get_token(filename='config.ini'):
    token = ConfigParser()
    token.read(filename)
    TOKEN = token.get('token', "TOKEN")
    return TOKEN
