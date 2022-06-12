import logging
import subprocess
from pathlib import Path

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)

project_folders: list[str] = []

PREFERENCES_ROOT_FOLDER = "root_folders"


class OpenerExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        if event.id == PREFERENCES_ROOT_FOLDER:
            ProjectFolders.update_root_folders(event.new_value)


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        root_folders = event.preferences[PREFERENCES_ROOT_FOLDER]
        ProjectFolders.update_root_folders(root_folders)


class ProjectFolders:
    @staticmethod
    def _scan_folder(folder: Path):
        logger.debug("scanning rootfolder: %s", folder)
        for sub_folder in folder.iterdir():
            if sub_folder.is_dir():
                project_folders.append(str(sub_folder))

    @staticmethod
    def update_root_folders(root_folders: str):
        logger.debug("rootfolder defined in preferences: %s", root_folders)
        global project_folders
        project_folders = []
        for root_folder in root_folders.split(","):
            ProjectFolders._scan_folder(Path(root_folder.strip()).resolve())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        found_projects = []
        args = event.get_argument()

        max_results = int(extension.preferences["max-results"])
        for project in project_folders:
            if args is not None and args in project:
                found_projects.append(
                    ExtensionResultItem(
                        name=project,
                        on_enter=ExtensionCustomAction({"project_path": project}),
                    )
                )
            if len(found_projects) == max_results:
                break

        return RenderResultListAction(found_projects)


class ItemEnterEventListener(EventListener):
    """Handles item enter"""

    def on_event(self, event, extension):
        """Event handler"""
        data = event.get_data()

        code_executable = extension.preferences["code_executable_path"]
        subprocess.run([code_executable, data["project_path"]])


if __name__ == "__main__":
    OpenerExtension().run()
