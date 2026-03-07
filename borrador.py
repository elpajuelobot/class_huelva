from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import ast, operator

# --- Evaluador seguro ---
class SafeEval:
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
    }

    def eval_expr(self, expr):
        try:
            node = ast.parse(expr, mode='eval').body
            return self._eval(node)
        except Exception:
            return "Error"

    def _eval(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            op = self.allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError("Operador no permitido")
            return op(self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            op = self.allowed_operators.get(type(node.op))
            return op(self._eval(node.operand))
        else:
            raise ValueError("Expresión no válida")

# --- Botón personalizado ---
class CustomButton(Button):
    def __init__(self, is_operator=False, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.font_size = '22sp'
        self.is_operator = is_operator
        self.normal_color = (0.3, 0.7, 1, 1) if is_operator else (0.92, 0.92, 0.92, 1)
        self.text_color = (1, 1, 1, 1) if is_operator else (0.1, 0.1, 0.1, 1)
        self.color = self.text_color

        with self.canvas.before:
            Color(*self.normal_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        self.rect.size = (self.width * 0.95, self.height * 0.95)

    def on_release(self):
        self.rect.size = self.size

# --- App principal ---
class CalculatorApp(App):
    def build(self):
        self.safe_eval = SafeEval()
        self.operators = ['+', '-', '*', '/']
        self.last_was_operator = None
        self.last_was_equal = False

        Window.size = (400, 600)
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        self.title = "Calculadora Segura"

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        display_layout = BoxLayout(size_hint_y=0.25)

        self.input_box = TextInput(
            font_size=48,
            readonly=True,
            halign='right',
            multiline=False,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0, 0, 0),
            padding=(25, 25),
            font_name='Roboto'
        )
        display_layout.add_widget(self.input_box)
        main_layout.add_widget(display_layout)

        buttons_layout = GridLayout(cols=4, spacing=12, padding=[2, 10, 2, 2])
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '⌫', '0', '=', '+',
            'C'
        ]
        for button in buttons:
            is_operator = button in self.operators or button in ['C', '=', '⌫']
            btn = CustomButton(
                text=button,
                is_operator=is_operator,
                on_press=self.on_button_press
            )
            buttons_layout.add_widget(btn)

        main_layout.add_widget(buttons_layout)

        # Soporte teclado físico
        Window.bind(on_key_down=self._on_key_down)
        return main_layout

    def on_button_press(self, instance):
        text = instance.text
        current = self.input_box.text

        if text == 'C':
            self.input_box.text = ""
        elif text == '⌫':
            self.input_box.text = current[:-1]
        elif text == '=':
            result = self.safe_eval.eval_expr(current)
            self.input_box.text = str(result)
            self.last_was_equal = True
        else:
            if self.last_was_equal and text not in self.operators:
                self.input_box.text = text
                self.last_was_equal = False
            else:
                self.input_box.text += text

    def _on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if text.isdigit() or text in self.operators:
            self.input_box.text += text
        elif keycode == 40:  # Enter
            self.on_button_press(type("btn", (), {"text": "="})())
        elif keycode == 42:  # Backspace
            self.input_box.text = self.input_box.text[:-1]
        elif text.lower() == 'c':
            self.input_box.text = ""

if __name__ == "__main__":
    CalculatorApp().run()
