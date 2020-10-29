from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import webbrowser
import subprocess


class BraveExtension(Extension):
    
    NEW_WINDOW_EVENT = 'new window'
    NEW_INCOGNITO_WINDOW_EVENT = 'new incognito window'
    OPEN_URL_EVENT = 'open url'

    def __init__(self):
        super(BraveExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def __init__(self):
        self.events = {
            BraveExtension.NEW_WINDOW_EVENT,
            BraveExtension.NEW_INCOGNITO_WINDOW_EVENT,
            BraveExtension.OPEN_URL_EVENT
        }

    def on_event(self, event, extension):
        items = []
        action = { 'query': event.get_argument() or extension.preferences['default_new_tab_url'] }
        for i in self.events:
            action['action'] = i
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=i,
                    description=str(),
                    on_enter=ExtensionCustomAction(action, keep_app_open=True)
                )
            )

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, listener):
        brave_cmd = "/usr/bin/brave-browser %s"
        browser_controller = webbrowser.get(brave_cmd)
        event_data = event.get_data()
 
        if event_data['action'] == BraveExtension.NEW_WINDOW_EVENT:
            browser_controller.open('', new=1)

        elif event_data['action'] == BraveExtension.NEW_INCOGNITO_WINDOW_EVENT:
            subprocess.check_call([
                'brave-browser',
                '--incognito'
            ])

        elif event_data['action'] == BraveExtension.OPEN_URL_EVENT:
            url = event_data['query']
            browser_controller.open_new_tab(url)

        return HideWindowAction()

if __name__ == '__main__':
    BraveExtension().run()