import os
import sys
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    ItemEnterEvent,
    PreferencesUpdateEvent,
)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from .keepassxc import KeepassXC
from . import render


class KeepassxcExtension(Extension):
    def __init__(self):
        super().__init__()
        self.keepassxc_db = KeepassXC(self.get_passfile_path(), self.get_db_path())
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener(self.keepassxc_db))
        # self.subscribe(ItemEnterEvent, ItemEnterEventListener(self.keepassxc_db))
        self.subscribe(
            PreferencesUpdateEvent, PreferencesUpdateEventListener(self.keepassxc_db)
        )

    def get_db_path(self) -> str:
        """
        Normalized and expanded path to the database file
        """
        return os.path.expanduser(self.preferences["database-path"])

    def get_passfile_path(self) -> str:
        """
        Normalized and expanded path to the database file
        """
        return os.path.expanduser(self.preferences["passfile-path"])

    def get_max_result_items(self) -> int:
        """
        Maximum number of search results to show on screen
        """
        return int(self.preferences["max-results"])


class KeywordQueryEventListener(EventListener):
    def __init__(self, keepassxc_db) -> None:
        super().__init__()
        self.keepassxc_db = keepassxc_db

    def process_keyword_query(self, event, extension) -> BaseAction:
        """
        Handle a search query entered by user
        """
        query_keyword = event.get_keyword()
        query_arg = event.get_argument()

        if not query_arg:
            if extension.recent_active_entries:
                return render.search_results(
                    query_keyword,
                    "",
                    extension.recent_active_entries,
                    extension.get_max_result_items(),
                )
            return render.ask_to_enter_query()

        entries = self.keepassxc_db.search(query_arg)
        return render.search_results(
            query_keyword, query_arg, entries, extension.get_max_result_items()
        )


# class ItemEnterEventListener(EventListener):
#     """KeywordQueryEventListener class used to manage user input"""
#
#     def __init__(self, keepassxc_db):
#         self.keepassxc_db = keepassxc_db

# # FUTURE replace with CallObjectMethodEventListener
# def on_event(self, event, extension) -> BaseAction:
#     try:
#         data = event.get_data()
#         action = data.get("action", None)
#         if action == "read_passphrase":
#             self.read_verify_passphrase()
#             return DoNothingAction()
#         if action == "activate_entry":
#             keyword = data.get("keyword", None)
#             entry = data.get("entry", None)
#             extension.set_active_entry(keyword, entry)
#             prev_query_arg = data.get("prev_query_arg", None)
#             extension.set_active_entry_search_restore(entry, prev_query_arg)
#             extension.add_recent_active_entry(entry)
#             return SetUserQueryAction("{} {}".format(keyword, entry))
#         if action == "show_notification":
#             Notify.Notification.new(data.get("summary")).show()
#     except KeepassxcCliNotFoundError:
#         return render.cli_not_found_error()
#     except KeepassxcFileNotFoundError:
#         return render.db_file_not_found_error()
#     except KeepassxcCliError as exc:
#         return render.keepassxc_cli_error(exc.message)
#     return DoNothingAction()


class PreferencesUpdateEventListener(EventListener):
    """Handle preferences updates"""

    def __init__(self, keepassxc_db):
        self.keepassxc_db = keepassxc_db

    def on_event(self, event, extension) -> None:
        if event.new_value != event.old_value:
            if event.id == "database-path":
                self.keepassxc_db.change_pathDB(event.new_value)
            elif event.id == "passfile-path":
                self.keepassxc_db.change_pathPass(event.new_value)
