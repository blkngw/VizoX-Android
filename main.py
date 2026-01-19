from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import requests
import threading
import subprocess

# GLAVNI EKRAN ZA LOGIN
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(Label(text="VizoX ANDROID", font_size=50, bold=True))
        
        self.dns = TextInput(hint_text="Server URL", multiline=False, size_hint_y=None, height=100)
        self.user = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=100)
        self.pw = TextInput(hint_text="Password", multiline=False, size_hint_y=None, height=100) # VIDLJIVA ŠIFRA
        
        layout.add_widget(self.dns)
        layout.add_widget(self.user)
        layout.add_widget(self.pw)
        
        btn = Button(text="ULOGUJ SE", size_hint_y=None, height=120, background_color=(0, 0.5, 1, 1))
        btn.bind(on_press=self.login)
        layout.add_widget(btn)
        self.add_widget(layout)

    def login(self, instance):
        App.get_running_app().config_data = {
            'dns': self.dns.text.strip('/'),
            'user': self.user.text,
            'pw': self.pw.text
        }
        self.manager.current = 'main'

# GLAVNI EKRAN ZA STRIMING
class MainScreen(Screen):
    def on_enter(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Meni na vrhu
        menu = BoxLayout(size_hint_y=None, height=100)
        btn_live = Button(text="KANALI")
        btn_live.bind(on_press=lambda x: self.fetch_data("get_live_streams"))
        btn_vod = Button(text="FILMOVI")
        btn_vod.bind(on_press=lambda x: self.fetch_data("get_vod_streams"))
        btn_series = Button(text="SERIJE")
        btn_series.bind(on_press=lambda x: self.fetch_data("get_series"))
        
        menu.add_widget(btn_live)
        menu.add_widget(btn_vod)
        menu.add_widget(btn_series)
        self.layout.add_widget(menu)

        # Scroll oblast za kartice
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=2, spacing=20, padding=20, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        
        self.add_widget(self.layout)
        self.fetch_data("get_live_streams")

    def fetch_data(self, action):
        self.grid.clear_widgets()
        d = App.get_running_app().config_data
        url = f"{d['dns']}/player_api.php?username={d['user']}&password={d['pw']}&action={action}"
        
        def task():
            try:
                r = requests.get(url).json()
                Clock.schedule_once(lambda dt: self.render_items(r, action))
            except: pass
        threading.Thread(target=task).start()

    def render_items(self, items, action):
        d = App.get_running_app().config_data
        for item in items[:100]: # Limit radi brzine
            name = item.get('name', 'N/A')
            btn = Button(text=name[:20], size_hint_y=None, height=250)
            
            if action == "get_series":
                btn.bind(on_press=lambda x, s_id=item.get('series_id'): self.pusti_seriju(s_id))
            else:
                s_id = item.get('stream_id')
                if action == "get_live_streams":
                    link = f"{d['dns']}/{d['user']}/{d['pw']}/{s_id}"
                else:
                    ext = item.get('container_extension', 'mp4')
                    link = f"{d['dns']}/movie/{d['user']}/{d['pw']}/{s_id}.{ext}"
                btn.bind(on_press=lambda x, l=link: self.pusti_media(l))
            
            self.grid.add_widget(btn)

    def pusti_seriju(self, series_id):
        # Ovde bi išao onaj tvoj GUI za sezone, za početak pušta prvu epizodu radi testa
        d = App.get_running_app().config_data
        url = f"{d['dns']}/player_api.php?username={d['user']}&password={d['pw']}&action=get_series_info&series_id={series_id}"
        def task():
            try:
                r = requests.get(url).json()
                ep = list(r['episodes'].values())[0][0]
                link = f"{d['dns']}/series/{d['user']}/{d['pw']}/{ep['id']}.{ep['container_extension']}"
                self.pusti_media(link)
            except: pass
        threading.Thread(target=task).start()

    def pusti_media(self, link):
        # Na Androidu koristimo sistemski plejer ili šaljemo link plejeru
        webbrowser.open(link)

class VizoXApp(App):
    def build(self):
        self.config_data = {}
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    VizoXApp().run()