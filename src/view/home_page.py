from kivy.lang import Builder
from kivymd.app import MDApp

from view.components.tab_recognition_arduino import TabRecognitionArduino
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
                tab = TabRecognition(title=f"Recognition") # TabRecognition
                self.root.ids.tabs.add_widget(tab)
            elif i == 1: 
                tab = TabRecognitionArduino(title=f"Recognition+Detection+Arduino")
                self.root.ids.tabs.add_widget(tab)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        instance_tab.ids.label.text = tab_text


##################LAYERS################## 
KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Project visione e percezione"

    MDTabs:
        id: tabs
        on_tab_switch: app.on_tab_switch(*args)

<TabRecognition>

    MDLabel:
        id: label
        size_hint_y: None
        width: 1
        height: 1

    GridLayout: 
        rows: 3
        cols: 1

        KivyCamera:
            id: camera
            halign: "center"

        MDLabel:
            id: labelOutput
            size_hint_y: None
            halign: "center"
            height: 100


        GridLayout: 
            rows: 1
            padding: 10
            spacing: 10
            valign: 'bottom'
            halign: 'center'
            size_hint_y: None

            MDRectangleFlatButton:
                id: buttonStartCamera
                halign: 'center'
                text:  'Start Camera'
                on_press: root.onStart()

            MDRectangleFlatButton:
                id: buttonStopCamera
                halign: 'center'
                text: 'Stop Camera'
                disabled: True
                on_press: root.onStop()

            MDRectangleFlatButton:
                id: buttonbackgroundCamera
                halign: 'center'
                text: 'background Camera'
                disabled: True
                on_press: root.onBackground()

            MDRectangleFlatButton:
                id: buttonStartClassification
                halign: 'center'
                text: 'Start Classification'
                disabled: True
                on_press: root.classificationHandle()

<TabRecognitionArduino>
    MDLabel:
        id: label
        halign: "center"
'''
##########################################