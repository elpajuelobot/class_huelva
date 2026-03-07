from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='main', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal
    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal

class InstrScr(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        txt = Label(text= 'pantalla_1')
        button = ScrButton(self, direction='left', goal='first', text="next")
        vl.add_widget(txt)
        vl.add_widget(button)
        hl.add_widget(vl)
        self.add_widget(hl)

class PulseScr(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        txt = Label(text= 'pantalla_2')
        button = ScrButton(self, direction='left', goal='second', text="next")
        vl.add_widget(txt)
        vl.add_widget(button)
        hl.add_widget(vl)
        self.add_widget(hl)

class CheckSits(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        txt = Label(text= 'pantalla_3')
        button = ScrButton(self, direction='left', goal='third', text="next")
        vl.add_widget(txt)
        vl.add_widget(button)
        hl.add_widget(vl)
        self.add_widget(hl)

class PulseScr2(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        txt = Label(text= 'pantalla_4')
        button = ScrButton(self, direction='left', goal='fourth', text="next")
        vl.add_widget(txt)
        vl.add_widget(button)
        hl.add_widget(vl)
        self.add_widget(hl)

class Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        txt = Label(text= 'pantalla_5')
        #button = ScrButton(self, direction='left', goal='main', text="next")
        vl.add_widget(txt)
        #vl.add_widget(button)
        hl.add_widget(vl)
        self.add_widget(hl)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InstrScr(name='main'))
        sm.add_widget(PulseScr(name='first'))
        sm.add_widget(CheckSits(name='second'))
        sm.add_widget(PulseScr2(name='third'))
        sm.add_widget(Result(name='fourth'))
        return sm

MyApp().run()
