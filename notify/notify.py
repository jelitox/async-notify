import logging
import importlib
from .exceptions import (
    ProviderError,
    notifyException
)

PROVIDERS = {}

class Notify(object):
    """Notify

        Factory object for getting a new Notification Provider.
    Args:
        provider (str): Name of the provider.

    Raises:
        ProviderError: when a driver cannot be loaded.
        NotSupported: when a method is not supported.
    Returns:
        ProviderBase: a Notify Provider.
    """
    def __new__(cls, *args, provider: str = None, **kwargs):
        if provider is not None:
            _provider = None
            try:
                obj = PROVIDERS[provider]
                _provider = obj(*args, **kwargs)
                logging.debug(
                    f':: Load Provider: {provider}'
                )
                return _provider
            except Exception as ex:
                logging.exception(
                    f"Cannot Load provider {provider}: {ex}"
                )
                raise ProviderError(
                    message=f"Cannot Load provider {provider}: {ex}"
                ) from ex
        else:
            return super(Notify, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def provider(cls, provider, *args, **kwargs):
        try:
            obj = PROVIDERS[provider]
            _provider = obj(*args, **kwargs)
            logging.debug(
                f':: Load Provider: {provider}'
            )
            return _provider
        except Exception as ex:
            logging.exception(
                f"Cannot Load provider {provider}: {ex}"
            )
            raise ProviderError(
                message=f"Cannot Load provider {provider}: {ex}"
            ) from ex


def LoadProvider(provider):
    """
    loadProvider.

    Dynamically load a defined provider
    """
    try:
        # try to using importlib
        classpath = f'notify.providers.{provider}'
        module = importlib.import_module(classpath, package='providers')
        obj = getattr(module, provider.capitalize())
        return obj
    except ImportError:
        try:
            obj = __import__(classpath, fromlist=[provider])
            return obj
        except ImportError as e:
            raise notifyException(
                f'Error: No Provider {provider} was Found'
            ) from e
