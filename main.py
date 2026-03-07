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

#TODO Ventana principal
class Window_manag(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        #! Texto principal
        self.texto = Label(text= 'Inicia sesión')
        #! Entrada usuario
        self.user = Label(text= 'introduce usuario')
        self.input_user = TextInput(multiline=False)
        #! Entrada contraseña
        self.password = Label(text= 'introduce contraseña')
        self.input_pass = TextInput(multiline=False)
        #! Botón para enviar datos
        btn_send = Button(text="Enviar")

        vl.add_widget(self.user)
        vl.add_widget(self.input_user)
        vl.add_widget(self.password)
        vl.add_widget(self.input_pass)
        vl.add_widget(btn_send)
        hl.add_widget(self.texto)
        hl.add_widget(ScrButton(self, direction='up', goal='first', text="siguiente"))
        hl.add_widget(vl)
        self.add_widget(hl)

        #! Comprobar datos
        btn_send.on_press = self.change_text

    def change_text(self):
        if self.input_user.text == "root" and self.input_pass.text == "123":
            self.texto.text = "Correcto"
        else:
            self.texto.text = "Incorrecto"


class Windows_1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=3, spacing=3)
        hl = BoxLayout()
        self.texto = Label(text='Elige día')
        vl.add_widget(ScrButton(self, direction='left', goal='second', text="31/10/2025"))
        hl.add_widget(ScrButton(self, direction='down', goal='main', text="Back"))
        hl.add_widget(vl)
        self.add_widget(hl)


class Windows_2(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        self.texto = Label(text='¡Reservado!')
        hl.add_widget(self.texto)
        self.add_widget(hl)



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Window_manag(name='main'))
        sm.add_widget(Windows_1(name='first'))
        sm.add_widget(Windows_2(name='second'))
        return sm

MyApp().run()
