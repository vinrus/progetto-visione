import cv2
from kivy.lang import Builder

from kivymd.app import MDApp


from utility.utility import Utility
from view.components.tab import TabDetection, Tab2
from view.components.tab_recognition import TabRecognition

class HomePage(MDApp):
    def build(self):
        # self.theme_cls.colors = Utility.colors
        # self.theme_cls.primary_palette = "Teal"
        # self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
         for i in range(3):
            if i == 0:
                tab = TabRecognition(title=f"Recognition")
                self.root.ids.tabs.add_widget(tab)
            elif i == 1: 
                tab = TabDetection(title=f"Recognition+Detection")
                self.root.ids.tabs.add_widget(tab)
            elif i == 2: 
                tab = Tab2(title=f"Recognition+Detection+Arduino")
                self.root.ids.tabs.add_widget(tab)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print("id: " + str(instance_tab.ids))
        print("instance_tabs: " + str(instance_tabs))
        instance_tab.ids.label.text = tab_text


##################LAYERS################## 
KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Progetto visione e percezione"

    MDTabs:
        id: tabs
        on_tab_switch: app.on_tab_switch(*args)

<TabRecognition>

    MDLabel:
        id: label
        size_hint_y: None
        width: 100
        height: 100

    GridLayout: 
        rows: 2
        cols: 1

        KivyCamera:
            id: camera
            halign: "center"

        GridLayout: 
            rows: 1
            cols: 3
            padding: 10
            spacing: 10
            halign: "bottom"
            size_hint_y: None
            
            MDRectangleFlatButton:
                id: buttonStartCamera
                text:  'Start Camera'
                on_press: root.onStart()

            MDRectangleFlatButton:
                id: buttonStopCamera
                text: 'Stop Camera'
                disabled: True
                on_press: root.onStop()

            MDRectangleFlatButton:
                id: buttonStartRecognition
                text: 'Start Recognition'
                on_press: root.recogntionHandle()
    

<TabDetection>
    MDLabel:
        id: label
        halign: "center"
    
                
<Tab2>
    MDLabel:
        id: label
        halign: "center"
    
'''
########################################## 