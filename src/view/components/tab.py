import cv2
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivy.base import EventLoop

    
class TabDetection(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    icon = ObjectProperty()

class Tab2(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    icon = ObjectProperty()
