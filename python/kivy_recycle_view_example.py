#! /usr/bin/python3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class RBL(RecycleBoxLayout):
    def __init__(self, **kwargs):
        super(RBL, self).__init__(**kwargs)
        self.default_size_hint = (1, None)
        self.default_size = (None, 100)        
        self.size_hint_y = None
        self.bind(minimum_height=lambda a, b: setattr(self, 'height', b))
        self.orientation = 'vertical'


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.add_widget(RBL())
        self.viewclass = 'Label'
        self.data = [{'text': str(x)} for x in range(100)]


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()