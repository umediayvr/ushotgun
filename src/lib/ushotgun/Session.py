import os
import json
import shotgun_api3

class SessionConfigError(Exception):
    """
    Session Config Error.
    """

class Session(object):
    """
    Singleton shotgun session.
    """

    __sessionSingleton = None
    __sessionConfigEnv = 'USHOTGUN_SESSION_CONFIG_PATH'
    __shotgunUrlEnv = 'UMEDIA_SHOTGUN_URL'

    @classmethod
    def get(cls, config='default'):
        """
        Return the current session.
        """
        if cls.__sessionSingleton is None:
            config = cls.__loadConfig(config)

            # creating a singleton session object
            cls.__sessionSingleton = shotgun_api3.Shotgun(
                os.environ[cls.__shotgunUrlEnv],
                script_name=config['auth']['scriptName'],
                api_key=config['auth']['apiKey']
            )

        return cls.__sessionSingleton

    @classmethod
    def __loadConfig(cls, name):
        """
        Return a dict with the session configuration.
        """
        configDir = os.environ.get(cls.__sessionConfigEnv, '')
        if not configDir:
            raise SessionConfigError(
                'Environment "{}" is not defined!'.format(
                    cls.__sessionConfigEnv
                )
            )

        # looking for the configuration under the config path
        configFile = None
        for configDirectory in filter(os.path.exists, configDir.split(':')):
            targetConfig = os.path.join(configDir, '{}.json'.format(name))
            if os.path.exists(targetConfig):
                configFile = targetConfig
                break

        # making sure the configuration file exists
        if not configFile:
            raise SessionConfigError(
                'Could not find configuration "{}.json" under {} environment'.format(
                        name,
                        cls.__sessionConfigEnv
                    )
                )

        # loading configuration json file
        result = {}
        with open(configFile) as jsonFile:
            result = json.load(jsonFile)

        return result
