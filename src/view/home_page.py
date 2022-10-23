from kivy.lang import Builder
from kivymd.app import MDApp

from view.components.tab_recognition_arduino import TabRecognitionArduino
from view.components.tab_recognition import TabRecognition
from view.components.tab_settings import TabSettings

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
            elif i == 2: 
                tab = TabSettings(title=f"Settings")
                self.root.ids.tabs.add_widget(tab)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print(f"[DEBUG] {tab_text}")

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
                id: buttonCamera
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
                text: 'Background Camera'
                disabled: True
                on_press: root.onBackground()

            MDRectangleFlatButton:
                id: buttonStartClassification
                halign: 'center'
                text: 'Start Classification'
                disabled: True
                on_press: root.classificationHandle()

<TabRecognitionArduino>
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

            MDRoundFlatIconButton:
                icon: "camera"
                width: dp(250)
                id: buttonCamera
                halign: 'center'
                text: root.buttonCamera
                on_press: root.onStart()

            MDRoundFlatIconButton:
                icon: "all-inclusive-box-outline"
                width: dp(250)
                id: buttonConnectionArduino
                halign: 'center'
                text: root.buttonConnectionArduino
                disabled: root.isDisabledConnectionArduino
                on_press: root.onArduino()

            MDRoundFlatIconButton:
                icon: "allergy"
                width: dp(250)
                id: buttonStartClassification
                halign: 'center'
                text: root.buttonClassification
                disabled: root.isDisabledClassification
                on_press: root.onClassification()

<TabSettings>
    GridLayout: 
        rows: 2
        cols: 2
        height: 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        MDLabel:
            halign: "center"
            height: 50
            text: "Path Model"
        
        MDLabel:
            id: pathModel
            halign: "center"
            text: root.getLabelPathModel()
            height: 50
            pos_hint: {"center_y": .5}
        
        # MDTextField: ##TODO per evoluzione modifca dei path
        #     id: pathModel
        #     hint_text: root.getLabelPathModel()
        #     helper_text: root.getLabelPathModel()
        #     helper_text_mode: "on_error"
        #     pos_hint: {"center_y": .5}
            
        MDLabel:
            halign: "center"
            height: 50
            text: "Path File Label"
        
        MDLabel:
            id: pathLabel
            halign: "center"
            height: 50
            text: root.getLabelPathLabel()

    BoxLayout:
        orientation: "vertical"
        heith: 2000
        size_hint_x: None
        
        MDLabel:
            halign: "center"

    



'''
##########################################


