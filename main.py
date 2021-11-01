
########################################################################
#                                              .""--.._                #
#                                              []      `'--.._         #
#                                              ||__           `'-,     #
#                                            `)||_ ```'--..       \    #
#                      _                      /|//}        ``--._  |   #
#                   .'  ` `'.                /////}              `\/   #
#                  /    .""".\              //{///                     #
#                   /  /_  _`\\            // `||                      #
#                   | |(_)(_)||          _//   ||                      #
#                   | |  /\  )|        _///\   ||                      #
#                   | |L====J |       / |/ |   ||                      #
#                  /  /'-..-' /    .'`  \  |   ||                      #
#                 /   |  :: | |_.-`      |  \  ||                      #
#                /|   `\-::.| |          \   | ||                      #
#              /` `|   /    | |          |   / ||                      #
#            |`    \   |    / /          \  |  ||                      #
#           |       `\_|    |/      ,.__. \ |  ||                      #
#           /                     /`    `\ ||  ||                      #
#          |           .         /        \||  ||                      #
#          |                     |         |/  ||                      #
#          /         /           |         (   ||                      #
#         /          .           /          )  ||                      #
#        |            \          |             ||                      #
#       /             |          /             ||                      #
#      |\            /          |              ||                      #
#      \ `-._       |           /              ||                      #
#       \ ,//`\    /`           |              ||                      #
#        ///\  \  |             \              ||                      #
#       |||| ) |__/             |              ||                      #
#       |||| `.(                |              ||                      #
#       `\\` /`                 /              ||                      #
#          /`                   /              ||                      #
# YT|R    /                     |              ||                      #
#        |                      \              ||                      #
#       /                        |             ||                      #
#     /`                          \            ||                      #
#   /`                            |            ||                      #
#   `-.___,-.      .-.        ___,'            ||                      #
#            `---'`   `'----'`                           art by: jgs   #
########################################################################

import os
import threading
import time
import tkinter as tk
from pytube import YouTube, exceptions
from tkinter import filedialog


#======================================================================#
#     [YT|R3ap3R] | Jarrod Burns | ta747839@gmail.com | 11/01/2021     #
# -------------------------- Version  1.0.0 -------------------------- #
#======================================================================#


class YouTubeReaper:
    def __init__(self, root):
        """
        [TY|R3ap3R] requests a YouTube video URL from the user. If a
        valid one is provided, the file is saved to the local machine.

        (4) Four file quality options are offered, (2) two for
        "audio only" and (2) two for "audio with video".

        The user may specify a directory to save their files to, the
        path for which is retained in "settings.txt". If they choose not
        do so, a directory is created locally instead.
        """
        self.root = root

        self.radio_choice = tk.StringVar()
        self.download_button_text = tk.StringVar()
        self.download_button_text.set("Download Now")

        self.context_menu_options = {
            "Cut": f"Cut{' '*18}Ctrl+X",
            "Copy": f"Copy{' '*15}Ctrl+C",
            "Paste": f"Paste{' '*15}Ctrl+V",
            "Separator": None,
            "SelectAll": f"Select All{' '*8}Ctrl+A"
        }

        self.itags = [
            ("48kbps", 139),
            ("128kbps", 140),
            ("360p", 18),
            ("720p", 22)
        ]

        self.pallet = {
            "font_default": ("Sans Serif", 10),
            "font_large": ("Sans Serif", 12, "bold"),
            "white": "#ffffff",
            "yt_white": "#fafafa",
            "yt_red": "#ff0000",
            "light_grey": "#6e6e6e",
            "charcoal": "#232323",
            "dark_coal": "#212121"
        }

        self.radio_choice.set(self.itags[-1][1])

        self.app_container = tk.Frame(                  # Master Frame
            self.root,
            width=350,
            height=220,
            highlightthickness=2,
            relief="groove",
            bg=self.pallet["charcoal"],
            highlightbackground=self.pallet["yt_white"]
        )
        self.app_container.pack(expand=False, padx=10, pady=10)

        self.url_textbox = tk.Text(                     # URL Box
            self.app_container,
            width=45,
            height=1,
            font=self.pallet["font_default"],
            bg=self.pallet["yt_white"],
            fg=self.pallet["dark_coal"],
        )
        self.url_textbox.pack(padx=(10, 10), pady=(10, 0))
        self.insert_message_to_textbox("Enter a YouTube URL to download...")
        self.m1_clears_textbox = self.bind_clear_key("<Button-1>")
        self.m3_clears_textbox = self.bind_clear_key("<Button-3>")

        self.all_radio_choices_containter = tk.Frame(   # All Radio Frame
            self.app_container,
            width=400,
            height=300,
            highlightthickness=2,
            relief="groove",
            bg=self.pallet["charcoal"],
            highlightbackground=self.pallet["charcoal"]
        )
        self.all_radio_choices_containter.pack(expand=False, padx=0, pady=10)
        self.all_radio_choices_containter.pack_propagate(False)

        self.auido_only_container = tk.Frame(           # Audio Only Frame
            self.all_radio_choices_containter,
            width=140,
            height=100,
            highlightthickness=2,
            bg=self.pallet["dark_coal"],
            highlightbackground=self.pallet["yt_white"]
        )
        self.auido_only_container.grid(row=0, column=0,
                                       padx=(0, 10),
                                       pady=(10, 10),
                                       sticky="w")
        self.auido_only_container.pack_propagate(False)

        tk.Label(                                       # Audio Only Label
            self.auido_only_container,
            text="Audio Only",
            font=self.pallet["font_default"],
            bg=self.pallet["dark_coal"],
            fg=self.pallet["yt_white"]
        ).pack(padx=(10, 10), pady=(10, 0))

        self.assign_radio_buttons(self.auido_only_container, self.itags[:2])

        self.audio_with_video_container = tk.Frame(     # Audio & Video Frame
            self.all_radio_choices_containter,
            width=140,
            height=100,
            highlightthickness=2,
            bg=self.pallet["dark_coal"],
            highlightbackground=self.pallet["yt_white"]
        )
        self.audio_with_video_container.grid(row=0, column=1,
                                             padx=(10, 0),
                                             pady=(10, 10),
                                             sticky="e")
        self.audio_with_video_container.pack_propagate(False)

        tk.Label(                                       # Audio & Video Label
            self.audio_with_video_container,
            text="Audio with Video",
            font=self.pallet["font_default"],
            bg=self.pallet["dark_coal"],
            fg=self.pallet["yt_white"]
        ).pack(padx=(10, 10), pady=(10, 0))

        self.assign_radio_buttons(self.audio_with_video_container,
                                  self.itags[2:])

        self.button_container = tk.Frame(               # Button Frame
            self.app_container,
            width=100,
            height=120,
            bg=self.pallet["charcoal"]
        )
        self.button_container.pack(expand=False, padx=(10, 10), pady=(0, 10))
        self.button_container.pack_propagate(False)

        self.download_button = tk.Button(               # Download Button
            self.button_container,
            width=15,
            height=1,
            textvariable=self.download_button_text,
            font=self.pallet["font_large"],
            bg=self.pallet["yt_red"],
            fg=self.pallet["yt_white"],
            disabledforeground=self.pallet["dark_coal"],
            command=lambda: self.in_new_thread(self.download_file)
        )
        self.download_button.grid(row=0, column=0)

        tk.Button(                                      # Set File Path Button
            self.button_container,
            width=15,
            height=1,
            text="Save File Location",
            font=self.pallet["font_large"],
            bg=self.pallet["yt_red"],
            fg=self.pallet["yt_white"],
            command=self.choose_save_file_directory
        ).grid(row=0, column=1)

        self.context_menu = tk.Menu(root, tearoff=0)    # Right Click Options
        self.build_context_menu_options(self.context_menu_options)

    def assign_radio_buttons(
        self,
        container: tk.Frame,
        itags: list[tuple[str, int], ...]
    ) -> None:
        """
        Iterates through a given list of tuples and assigns a
        corresponding value, and its text representation, to a radio
        button.
        """
        for itag in itags:
            tk.Radiobutton(
                container,
                text=itag[0],
                value=itag[1],
                variable=self.radio_choice,
                font=self.pallet["font_default"],
                bg=self.pallet["dark_coal"],
                fg=self.pallet["yt_white"],
                activebackground=self.pallet["dark_coal"],
                activeforeground=self.pallet["yt_white"],
                selectcolor=self.pallet["dark_coal"]
            ).pack()

    def build_context_menu_options(
        self,
        context_menu_options: dict[str: str, ...]
    ) -> None:
        """
        Iterates through a given dictionary and assigns a corresponding
        virtual event, and its text representation, to the context menu.

        If the term "Separator" is passed, a separator line is added to
        the menu instead.
        """
        for virtual_event, text_representation in context_menu_options.items():

            if virtual_event == "Separator":
                self.context_menu.add_separator()
                continue

            self.context_menu.add_command(label=text_representation)

            self.context_menu.entryconfigure(
                text_representation,
                command=lambda _virtual_event=virtual_event:
                self.url_textbox.event_generate(f"<<{_virtual_event}>>")
            )

    def show_context_menu(self, event: tk.Event) -> None:
        """
        Displays the context menu at the users current mouse position.
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def download_file(self) -> None:
        """
        This method is intended to be executed in a separate thread from
        the main loop.

        Checks the URL textbox for for a string value. If one is not
        returned the function is exited.

        If a value other than None is provided, the URL is assigned to
        the "YouTube" constructor for validation.

        If the user provided a valid URL, the "download_in_progress"
        flag is set to True, and a new thread is opened in order to
        display the in progress animation. The "YouTube" constructor
        downloads the file, of user specified quality, to the defined
        directory. Once the download is complete "download_in_progress"
        is set to False and a success message in inserted into the URL
        textbox.

        If the user provided an invalid URL, the download button's
        appearance is updated to reflect its idle state and a message
        is inserted into the URL box to alert the user.

        If the file is not available in the specified quality, the
        "download_in_progress" flag is set to false and an an error
        message is inserted into the URL textbox to reflect the
        appropriate exception.

        Lastly, left and right mouse click are bound to clear the value
        from the URL textbox on the next click event within it.
        """
        url = self.url_textbox.get("1.0", 'end-1c')
        if not url:
            return

        try:
            yt = YouTube(url)
            download_quality_choice = self.radio_choice.get()

            self.download_in_progress = True
            self.in_new_thread(self.download_animation)

            yt.streams.get_by_itag(download_quality_choice).download(
                output_path=self.save_file_directory()
            )

            self.download_in_progress = False
            self.insert_message_to_textbox("Download completed successfully!")

        except exceptions.RegexMatchError:
            self.idle_state_download_button()
            self.insert_message_to_textbox("Invalid URL...")

        except AttributeError:
            self.download_in_progress = False
            self.insert_message_to_textbox(
                "Specified quality is not available for the supplied URL."
            )

        finally:
            self.m1_clears_textbox = self.bind_clear_key("<Button-1>")
            self.m3_clears_textbox = self.bind_clear_key("<Button-3>")

    def download_animation(self):
        """
        This method is intended to be executed in a separate thread from
        the main loop.

        Changes the appearance of the download button to reflect its
        active state, and then disables user input.

        While the attribute "download_in_progress" is set to True, the
        text of the download button is updated from the frames list in
        order to display an active animation.

        Once the attribute "download_in_progress" is set to False, the
        appearance of the download button is set to its idle state and
        user input is enabled.
        """
        frames = [
            "Downloading |...",
            "Downloading .|..",
            "Downloading ..|.",
            "Downloading ...|",
            "Downloading ...."
        ]

        self.active_state_download_button()
        self.download_button["state"] = "disabled"

        while self.download_in_progress:
            for frame in frames:
                self.download_button_text.set(frame)
                time.sleep(0.3)

        self.idle_state_download_button()
        self.download_button["state"] = "normal"

    def active_state_download_button(self) -> None:
        """
        Alters the appearance of the download button to reflect its
        active state.
        """
        self.download_button.configure(
            relief="sunken",
            fg=self.pallet["dark_coal"],
            bg=self.pallet["yt_white"]
        )
        self.download_button_text.set("Downloading ...")

    def idle_state_download_button(self) -> None:
        """
        Alters the appearance of the download button to reflect its
        idle state.
        """
        self.download_button.configure(
            relief="raised",
            fg=self.pallet["yt_white"],
            bg=self.pallet["yt_red"]
        )
        self.download_button_text.set("Download Now")

    def insert_message_to_textbox(self, error_message: str) -> None:
        """
        Clears the URL textbox of all values and inserts the supplied
        message.
        """
        self.url_textbox.delete(1.0, "end")
        self.url_textbox.insert(1.0, error_message)

    def clear_message_text(self, event: tk.Event) -> None:
        """
        Removes all values from the URL box and unbinds left and right
        mouse click to prevent a callback from preforming this action
        again without being reassigned.

        Right mouse click is then bound allowing the context menu to be
        displayed.

        If the event is a right mouse click, the context menu is
        displayed.
        """
        self.url_textbox.delete(1.0, "end")
        self.url_textbox.unbind("<Button-1>", self.m1_clears_textbox)
        self.url_textbox.unbind("<Button-3>", self.m3_clears_textbox)
        self.url_textbox.bind("<Button-3>", self.show_context_menu)

        if event.num == 3:
            self.show_context_menu(event)

    def bind_clear_key(self, key_event: str) -> None:
        """
        Binds the given key event to delete the current value of the URL
        textbox.
        """
        self.url_textbox.bind(key_event, self.clear_message_text)

    @staticmethod
    def in_new_thread(function) -> None:
        """
        Executes the supplied function in a new thread.
        """
        threading.Thread(target=function).start()

    @staticmethod
    def choose_save_file_directory() -> None:
        """
        Prompts the user with a directory selection dialog.

        If a directory is chosen by the user, that path is saved in
        "settings.txt" for future reference.
        """
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            with open("settings.txt", "w") as file_handle:
                file_handle.writelines(folder_selected)

    @staticmethod
    def save_file_directory() -> str:
        """
        Checks "settings.txt" for a user defined directory preference.

        If the user has not previously specified a download location,
        then a local directory is created and the files are saved within.

        If the user has specified a download location, the files are
        saved in the given directory, defined by the "settings.txt" file.
        """
        if os.stat("settings.txt").st_size == 0:
            cwd = os.getcwd()
            os.makedirs(f"{cwd}\\youtube_downloads\\", exist_ok=True)
            return f"{cwd}\\youtube_downloads"

        with open("settings.txt", "r") as file_handle:
            return file_handle.readline().rstrip()


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry("370x240")
    root.iconbitmap("img/favicon.ico")
    root.title("[YT | R3ap3R]")
    root.configure(bg="#6e6e6e")
    app = YouTubeReaper(root)
    root.mainloop()
