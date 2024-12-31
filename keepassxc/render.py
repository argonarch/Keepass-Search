from ulauncher.api.shared.item.ResultItem import ResultItem
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.BaseAction import BaseAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.ActionList import ActionList

# from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

NO_SEARCH_RESULTS_ITEM = ExtensionResultItem(
    icon="images/not_found.svg",
    name="No matching entries found...",
    description="Please check spelling or make the query less specific",
    on_enter=DoNothingAction(),
)


def item_more_results_available(cnt: int) -> ResultItem:
    """
    Item showing how many more results are available
    """
    return ExtensionSmallResultItem(
        icon="images/empty.png",
        name="...{} more results available, please refine the search query...".format(
            cnt
        ),
        on_enter=DoNothingAction(),
    )


def search_results(
    keyword: str, arg: str, entries: list[str], max_items: int
) -> BaseAction:
    """
    Build list of result items `max_items` long
    """
    items = []
    if not entries:
        items.append(NO_SEARCH_RESULTS_ITEM)
    else:
        for entry in entries[:max_items]:
            # FUTURE replace with call_object_method
            action = ExtensionCustomAction(
                {
                    "action": "activate_entry",
                    "entry": entry,
                    "keyword": keyword,
                    "prev_query_arg": arg,
                },
                keep_app_open=True,
            )
            items.append(
                ExtensionSmallResultItem(
                    icon="images/key.svg", name=entry, on_enter=action
                )
            )
        if len(entries) > max_items:
            items.append(item_more_results_available(len(entries) - max_items))
    return RenderResultListAction(items)


def ask_to_enter_query() -> BaseAction:
    """
    Ask user to start entering the search query
    """
    return RenderResultListAction(
        [
            ExtensionResultItem(
                icon="images/keepassxc-search.svg",
                name="Enter search query...",
                description="Please enter your search query",
                on_enter=DoNothingAction(),
            )
        ]
    )
