__author__ = 'rh0dium'
#https://stackoverflow.com/questions/21538859/pycharm-set-environment-variable-for-run-manage-py-task/30374246#30374246
# use:
#       from get_env_variable import get_env_variable as ge
#       ge('HOME')
def get_env_variable(var_name, default=False):
    """
    Get the environment variable or return exception
    :param var_name: Environment Variable to lookup
    """
    import os
    try:
        return os.environ[var_name]
    except KeyError:
        import StringIO
        import ConfigParser
        env_file = os.environ.get('PROJECT_ENV_FILE', SITE_ROOT + "/.env")
        try:
            config = StringIO.StringIO()
            config.write("[DATA]\n")
            config.write(open(env_file).read())
            config.seek(0, os.SEEK_SET)
            cp = ConfigParser.ConfigParser()
            cp.readfp(config)
            value = dict(cp.items('DATA'))[var_name.lower()]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name, value)
            return value
        except (KeyError, IOError):
            if default is not False:
                return default
            from django.core.exceptions import ImproperlyConfigured
            error_msg = "Either set the env variable '{var}' or place it in your " \
                        "{env_file} file as '{var} = VALUE'"
            raise ImproperlyConfigured(error_msg.format(var=var_name, env_file=env_file))