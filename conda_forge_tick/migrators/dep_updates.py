import logging
import typing
from typing import Any

from conda_forge_tick.migrators.core import MiniMigrator
from conda_forge_tick.update_deps import apply_dep_update, get_dep_updates_and_hints
from conda_forge_tick.utils import get_keys_default

if typing.TYPE_CHECKING:
    from ..migrators_types import AttrsTypedDict

logger = logging.getLogger(__name__)


class DependencyUpdateMigrator(MiniMigrator):
    post_migration = True

    def __init__(self, python_nodes):
        self.python_nodes = python_nodes

    def filter(self, attrs: "AttrsTypedDict", not_bad_str_start: str = "") -> bool:
        update_deps = get_keys_default(
            attrs,
            ["conda-forge.yml", "bot", "inspection"],
            {},
            "hint",
        )
        if update_deps in ["update-all", "update-source", "update-grayskull"]:
            return False

        return True

    def migrate(self, recipe_dir: str, attrs: "AttrsTypedDict", **kwargs: Any) -> None:
        update_deps = get_keys_default(
            attrs,
            ["conda-forge.yml", "bot", "inspection"],
            {},
            "hint",
        )
        logger.info("bot.inspection: %s", update_deps)
        try:
            dep_comparison, _ = get_dep_updates_and_hints(
                update_deps,
                recipe_dir,
                attrs,
                self.python_nodes,
                "new_version",
            )
        except (BaseException, Exception):
            logger.warning("Dep update failed!", exc_info=True)
        else:
            logger.info("applying deps: %s", update_deps)
            apply_dep_update(
                recipe_dir,
                dep_comparison,
            )
