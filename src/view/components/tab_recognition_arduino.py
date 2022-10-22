from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty

class TabRecognitionArduino(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    icon = ObjectProperty()
