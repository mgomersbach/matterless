"""Manage terminal user interface.

    This module provides a terminal user interface for Matterless.
    It will try to be visually on par with the official released desktop client.
    """

import TermTk
import mattermost as mm


def _debug_title(object):
    """Print the title of the object."""
    name = str(type(object))
    name = name.split(".")[-1]
    name = name.split("'")[0]
    return name


class Terminal(TermTk.TTk):
    """Terminal user interface."""

    def __init__(self, config=None, mattermost=None, *args, **kwargs) -> None:
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self._config = config
        self._mattermost = mattermost
        self._main_frame = MainFrame(parent=self)


class MainFrame(TermTk.TTkFrame):
    """Main frame."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self.setBorder(False)
        self._top_bar = TopBar(parent=self)


class TopBar(TermTk.TTkTabWidget):
    """Top bar.
    Has menu and server switcher.
    Itterate through server configurations to make according tabs
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setTabsClosable(True)
        self.setTitle(_debug_title(self))

        self._mattermost = self.parentWidget().parentWidget()._mattermost
        self._program_menu = self.addMenu("⋮")

        self._file_menu = self._program_menu.addMenu("&File")
        self._edit_menu = self._program_menu.addMenu("&Edit")
        self._view_menu = self._program_menu.addMenu("&View")
        self._history_menu = self._program_menu.addMenu("&History")
        self._window_menu = self._program_menu.addMenu("&Window")
        self._help_menu = self._program_menu.addMenu("&Help")

        self._file_menu.addMenu("&Settings...")
        # TODO: Make menu width configurable so it can fit the text
        # "Sign in to Another Server" instead of "New Server"
        self._file_menu.addMenu("&New Server")
        self._file_menu.addSpacer()
        self._file_menu.addMenu("&Quit")

        self._edit_menu.addMenu("&Undo")
        self._edit_menu.addMenu("&Redo")
        self._edit_menu.addSpacer()
        self._edit_menu.addMenu("&Cut")
        self._edit_menu.addMenu("C&opy")
        self._edit_menu.addMenu("&Paste")
        self._edit_menu.addMenu("Paste and &Match Style")
        self._edit_menu.addMenu("Select &all")

        self._view_menu.addMenu("&Find")
        self._view_menu.addMenu("&Reload")
        self._view_menu.addMenu("&Clear Cache and Reload")
        self._view_menu.addMenu("&Toggle Full Screen")
        self._view_menu.addSpacer()
        self._view_menu.addMenu("&Debug mode")

        self._history_menu.addMenu("&Back")
        self._history_menu.addMenu("&Forward")

        self._window_menu.addMenu("&Minimize")
        self._window_menu.addMenu("&Close")
        self._window_menu.addSpacer()
        self._window_menu.addMenu("&Show Servers")
        self._window_menu.addMenu("Select &next tab")
        self._window_menu.addMenu("Select &previous tab")

        self._help_menu.addMenu("&Learn More")
        self._help_menu.addSpacer()
        self._help_menu.addMenu("&About")

        for servername in (
            self.parentWidget().parentWidget()._mattermost["servers"]
        ):
            self.addTab(
                ServerFrame(
                    server=servername,
                    mattermost=self._mattermost.MattermostManager(
                        options={
                            "url": config["matterless"]["url"],
                            "token": config["matterless"]["token"],
                            "login_id": config["matterless"]["loginid"],
                            "password": config["matterless"]["password"],
                            "mfa_token": config["matterless"]["mfatoken"],
                            "port": 443,
                        }
                    ),
                    border=True,
                ),
                servername["name"],
            )


class ServerFrame(TermTk.TTkFrame):
    """Server frame."""

    def __init__(self, server, mattermost, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkHBoxLayout())
        self.setTitle(_debug_title(self))
        self._server = server
        self._mattermost = mattermost

        self._sidebar_frame = SidebarFrame(parent=self)
        self._channel_frame = ChannelFrame(parent=self)


class SidebarFrame(TermTk.TTkFrame):
    """Sidebar frame.
    Has channel list and user settings."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkVBoxLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))

        self.user_frame = UserFrame(parent=self)
        self.channellist_frame = ChannelListFrame(parent=self)


class ChannelFrame(TermTk.TTkFrame):
    """Channel frame.
    Has channel message exchane and channel info."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkVBoxLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))

        self.channel_header = ChannelHeader(parent=self)
        self.channel_message_exchange = ChannelMessageExchange(parent=self)


class UserFrame(TermTk.TTkFrame):
    """Client frame.
    Contains the user settings."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))


class ChannelHeader(TermTk.TTkFrame):
    """Channel header.
    Has channel name, settings and channel info."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))


class ChannelMessageExchange(TermTk.TTkFrame):
    """Channel messages.
    Has channel message exchange."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))


class ChannelListFrame(TermTk.TTkFrame):
    """Channel list.
    Has channel list."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout())
        self.setBorder(True)
        self.setTitle(_debug_title(self))
        self.channel_frame_layout = self.layout()

        self.search_bar = self.channel_frame_layout.addWidget(
            SearchBar(parent=self), 0, 0
        )
        self.channel_list = self.channel_frame_layout.addWidget(
            ChannelList(parent=self), 1, 0
        )


class SearchBar(TermTk.TTkFrame):
    """Search bar.
    Has search bar."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout(columnMinWidth=1))
        self.setBorder(True)
        self.setTitle(_debug_title(self))

        self.search_layout = self.layout()
        # self.search_label = self.search_layout.addWidget(
        #    TermTk.TTkLabel(text="🔍"), 0, 0
        # )
        self.search_input = self.search_layout.addWidget(
            TermTk.TTkLineEdit(text="🔍 Find channel"), 0, 1
        )

        # self.search_label.setAlignment(TermTk.CENTER_ALIGN)


class ChannelList(TermTk.TTkFrame):
    """Channel list.
    Has channel list."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(TermTk.TTkGridLayout(columnMinWidth=1, border=False))
        self.setBorder(True)
        self.setTitle(_debug_title(self))

        self.channel_list_layout = self.layout()
        self.channel_list = self.channel_list_layout.addWidget(
            TermTk.TTkList(parent=self, maxWidth=20, minWidth=10), 0, 0
        )

        for server in (
            self.parentWidget().parentWidget().parentWidget()._mattermost
        ):
            if (
                server
                == self.parentWidget().parentWidget().parentWidget()._server
            ):
                self.channel_list.addItem(server)
            # self.addItem(
            #    channel["name"],
            # )
        # self.channel_list.textClicked.connect(_channel_list_callback)

        # @TermTk.pyTTkSlot(str)
        # def _channel_list_callback(self, label):
        #    label2.text = f"[ list2 ] {listWidgetMulti.selectedLabels()}"


if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    main_terminal = Terminal(
        config={
            "servers": [
                {
                    "name": "woei",
                },
                {
                    "name": "adyen",
                },
            ]
        },
        mattermost={
            "servers": [
                {
                    "name": "woei",
                    "channels": [
                        {"name": "general"},
                        {"name": "random"},
                        {"name": "random2"},
                        {"name": "random3"},
                        {"name": "random4"},
                    ],
                },
                {
                    "name": "adyen",
                    "channels": [
                        {"name": "general"},
                        {"name": "random"},
                        {"name": "random2"},
                        {"name": "random3"},
                        {"name": "random4"},
                    ],
                },
            ]
        },
    )

    # main_frame = TermTk.TTkFrame(parent=main_terminal, border=True)

    main_terminal.mainloop()
