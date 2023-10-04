# Copyright (c) Meta Platforms, Inc. and affiliates.

"""
Provides a list of which functionality an expansion provies.

See the README.md in this directory for more information.

tl;dr: Have a module with TX_MANIFEST that is assigned this class.
"""


from dataclasses import dataclass
import importlib
import typing as t

from threatexchange.exchanges.signal_exchange_api import SignalExchangeAPI
from threatexchange.signal_type.signal_base import SignalType
from threatexchange.content_type.content_base import ContentType


@dataclass
class ThreatExchangeExtensionManifest:
    """
    Class with a list of expansion contents.

    Assign a variable named TX_MANIFEST with this class populated with the
    contents of your extension to make it loadable by ThreatExchange.
    """

    signal_types: t.Tuple[t.Type[SignalType], ...] = ()
    content_types: t.Tuple[t.Type[ContentType], ...] = ()
    apis: t.Tuple[t.Type[SignalExchangeAPI], ...] = ()

    @classmethod
    def load_from_module_name(
        cls, module_name: str
    ) -> "ThreatExchangeExtensionManifest":
        """Following the expected conventions, load an extension"""
        try:
            module = importlib.import_module(module_name)
        except (ImportError, ValueError):
            raise ValueError(f"No such module '{module_name}'")

        try:
            manifest = module.TX_MANIFEST
        except AttributeError:
            raise ValueError(f"Module is missing TX_MANIFEST")

        if not isinstance(manifest, cls):
            raise ValueError(f"TX_MANIFEST is not a {cls.__name__}!")

        try:
            manifest.entrypoint()
        except Exception as exc:
            raise ValueError(f'Manifest failed to init via entrypoint: {module_name}') from exc

        return manifest

    @classmethod
    def entrypoint(cls):
        """
        Entrypoint bootstraps the manifest for the extension to properly execute.
        By default, do nothing for extensions.
        """
        return

