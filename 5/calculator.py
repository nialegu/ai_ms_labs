from kivy.app import App
from kivy.lang import Builder

UI = """
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.08, 1
        Rectangle:
            pos: self.pos
            size: self.size

    TextInput:
        id: screen
        text: '0'
        font_size: 56
        size_hint_y: 0.25
        halign: 'right'
        readonly: True
        background_color: 0.1, 0.1, 0.2, 1
        foreground_color: 0.7, 0.9, 1, 1

    GridLayout:
        cols: 4
        spacing: 8

        Button:
            text: 'AC'
            background_color: 0.8, 0.2, 0.3, 1
            on_press: app.reset_all()
        Button:
            text: '±'
            background_color: 0.3, 0.3, 0.4, 1
            on_press: app.flip_sign()
        Button:
            text: '%'
            background_color: 0.3, 0.3, 0.4, 1
            on_press: app.to_percent()
        Button:
            text: '÷'
            background_color: 0.6, 0.2, 1, 1
            on_press: app.choose_op('/')

        Button:
            text: '7'
            on_press: app.add_digit('7')
        Button:
            text: '8'
            on_press: app.add_digit('8')
        Button:
            text: '9'
            on_press: app.add_digit('9')
        Button:
            text: '×'
            background_color: 0.6, 0.2, 1, 1
            on_press: app.choose_op('*')

        Button:
            text: '4'
            on_press: app.add_digit('4')
        Button:
            text: '5'
            on_press: app.add_digit('5')
        Button:
            text: '6'
            on_press: app.add_digit('6')
        Button:
            text: '−'
            background_color: 0.6, 0.2, 1, 1
            on_press: app.choose_op('-')

        Button:
            text: '1'
            on_press: app.add_digit('1')
        Button:
            text: '2'
            on_press: app.add_digit('2')
        Button:
            text: '3'
            on_press: app.add_digit('3')
        Button:
            text: '+'
            background_color: 0.6, 0.2, 1, 1
            on_press: app.choose_op('+')

        Button:
            text: '0'
            on_press: app.add_digit('0')
        Button:
            text: '.'
            on_press: app.add_digit('.')
        Button:
            text: '='
            background_color: 0.2, 0.8, 0.6, 1
            on_press: app.solve()
        Widget:
"""


class CalcApp(App):
    def build(self):
        self._left = None
        self._op = None
        self._clear_next = False
        return Builder.load_string(UI)

    @property
    def screen(self):
        return self.root.ids.screen

    def add_digit(self, value):
        text = self.screen.text

        if self._clear_next:
            text = '0'
            self._clear_next = False

        if value == '.' and '.' in text:
            return

        self.screen.text = value if text == '0' and value != '.' else text + value

    def choose_op(self, op):
        self._left = float(self.screen.text)
        self._op = op
        self._clear_next = True

    def solve(self):
        if not self._op:
            return

        try:
            right = float(self.screen.text)

            operations = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b if b != 0 else None,
            }

            result = operations[self._op](self._left, right)

            if result is None:
                self.screen.text = 'Err'
            else:
                self.screen.text = str(int(result)) if result.is_integer() else str(round(result, 6))

        except:
            self.screen.text = 'Err'

        self._left = None
        self._op = None
        self._clear_next = True

    def reset_all(self):
        self.screen.text = '0'
        self._left = None
        self._op = None
        self._clear_next = False

    def flip_sign(self):
        val = float(self.screen.text)
        val *= -1
        self.screen.text = str(int(val)) if val.is_integer() else str(val)

    def to_percent(self):
        val = float(self.screen.text)
        self.screen.text = str(round(val / 100, 6))


if __name__ == "__main__":
    CalcApp().run()