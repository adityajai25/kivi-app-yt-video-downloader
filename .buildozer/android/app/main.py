from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from pytube import YouTube
from kivy.utils import platform
import os
import validators

class HoverButton(Button):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.4, 0.4, 0.4, 1)
        self.bind(on_enter=self.on_enter)
        self.bind(on_leave=self.on_leave)
    
    def on_enter(self, instance):
        self.background_color = (0.5, 0.5, 0.5, 1)
    
    def on_leave(self, instance):
        self.background_color = (0.4, 0.4, 0.4, 1)

class ClearableTextInput(BoxLayout):
    def __init__(self, **kwargs):
        super(ClearableTextInput, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(30)
        
        # TextInput widget
        self.text_input = TextInput(multiline=False, hint_text='e.g., https://www.youtube.com/watch?v=...')
        self.add_widget(self.text_input)
        
        # Clear button ('X')
        self.clear_button = Button(text='X', size_hint_x=None, width=dp(30), background_normal='', background_color=(0.5, 0.5, 0.5, 1))
        self.clear_button.bind(on_press=self.clear_text)
        self.add_widget(self.clear_button)
    
    def clear_text(self, instance):
        self.text_input.text = ''

class Downloader(BoxLayout):
    def __init__(self, **kwargs):
        super(Downloader, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create a BoxLayout for better organization
        self.box_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.8, None))
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))
        
        # Add welcome label
        self.welcome_label = Label(text='Welcome to YouTube Video Downloader', size_hint_y=None, height=dp(40))
        self.box_layout.add_widget(self.welcome_label)

        # Add description label
        self.description_label = Label(text='Download your favorite YouTube video with ease!', size_hint_y=None, height=dp(40))
        self.box_layout.add_widget(self.description_label)
        
        # Add Label and TextInput for URL input
        self.label = Label(text='Paste any YouTube video/shorts URL:', size_hint_y=None, height=dp(40))
        self.box_layout.add_widget(self.label)

        self.url_input = ClearableTextInput()
        self.box_layout.add_widget(self.url_input)
        
        # Add Download Button with hover effect
        self.download_button = HoverButton(text='Download Video', size_hint_y=None, height=dp(30), width=dp(50))
        self.download_button.bind(on_press=self.download_video)
        self.box_layout.add_widget(self.download_button)

        # Create an AnchorLayout to center the BoxLayout
        self.anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.anchor_layout.add_widget(self.box_layout)
        
        self.add_widget(self.anchor_layout)

    def download_video(self, instance):
        url = self.url_input.text_input.text.strip()
        
        # Check if the input is a valid URL using validators library
        if not validators.url(url):
            self.show_popup("Error", "Please enter a valid URL", scrollable=False)
            return

        try:
            yt = YouTube(url)
            if not yt.streams:
                self.show_popup("Error", "No YouTube video found to download, please provide a valid URL")
                return
            
            video = yt.streams.get_highest_resolution()
            video = yt.streams.get_highest_resolution()
            if platform == 'android':
                # Get the external storage directory
                download_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'Download')
            else:
                # Default path for other platforms (PC)
                download_path = os.path.expanduser('~/Downloads')
    
            title = yt.title
            file_path = os.path.join(download_path, f"{title}.mp4")
            
            # Check for duplicates and rename accordingly
            base, extension = os.path.splitext(file_path)
            counter = 1
            while os.path.exists(file_path):
                file_path = f"{base} ({counter}){extension}"
                counter += 1
            
            video.download(output_path=download_path, filename=os.path.basename(file_path))
            self.show_success_popup(f"Success! Video downloaded successfully.\n\nTitle: {yt.title}\nDirectory: {download_path}")
            
            # Clear the text input after successful download
            self.url_input.text_input.text = ''
            
        except Exception as e:
            self.show_popup("Error", f"Error: Video Not found, please provide a valid URL")

    def show_success_popup(self, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message, size_hint_y=None, height=dp(100), text_size=(600, None))
        popup_label.bind(size=popup_label.setter('texture_size'))
        
        popup_scrollview = ScrollView()
        popup_scrollview.add_widget(popup_label)
        popup_layout.add_widget(popup_scrollview)
        
        popup_button = Button(text='OK', size_hint_y=None, height=dp(40))
        popup_layout.add_widget(popup_button)

        # Calculate new size based on 0.5% increase
        current_width, current_height = 600, 400
        new_width = current_width * 1.005
        new_height = current_height * 1.005
        
        popup = Popup(title="Success", content=popup_layout, size_hint=(None, None), size=(new_width, new_height))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_popup(self, title, message, scrollable=True):
        popup_layout = BoxLayout(orientation='vertical', padding=(10, 0), spacing=10)
        
        if scrollable:
            popup_label = Label(text=message, size_hint_y=None, height=dp(50), text_size=(400, None))
            popup_label.bind(size=popup_label.setter('text_size'))
            
            popup_scrollview = ScrollView()
            popup_scrollview.add_widget(popup_label)
            popup_layout.add_widget(popup_scrollview)
        else:
            popup_label = Label(text=message, size_hint_y=None, height=dp(50), text_size=(400, None))
            popup_label.bind(size=popup_label.setter('text_size'))
            popup_layout.add_widget(popup_label)
        
        popup_button = Button(text='OK', size_hint_y=None, height=dp(30))
        popup_layout.add_widget(popup_button)
        
        if title == "Error":
            popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(400, 250))
        else:
            popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(600, 400))
        
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

class YouTubeDownloaderApp(App):
    def build(self):
        self.title = 'YouTube Downloader'
        return Downloader()

if __name__ == '__main__':
    YouTubeDownloaderApp().run()