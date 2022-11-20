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
                tab = TabRecognitionArduino(title=f"Recognition and Detection with Arduino")
                self.root.ids.tabs.add_widget(tab)
            elif i == 1:
                tab = TabRecognition(title=f"Recognition")
                self.root.ids.tabs.add_widget(tab)
            # elif i == 2: 
            #     tab = TabSettings(title=f"Settings")
            #     self.root.ids.tabs.add_widget(tab)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print(f"[DEBUG] {tab_text}")

##################LAYERS################## 
KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Gesture classification and recognition with Arduino"

    MDTabs:
        id: tabs
        on_tab_switch: app.on_tab_switch(*args)

<TabRecognitionArduino>
    GridLayout: 
        rows: 3
        cols: 1
       
        GridLayout: 
            cols: 3
            rows: 1
            
            Image:
                size_hint: .9, 0
                padding: [0, 100, 0, 0]
                halign: "center"
                source: '/Users/vincenzo/Documents/Developer/progetto-visione/assets/graphics/shemaArduino.png'
                
            GridLayout: 
                size_hint: .2, .1
                padding: [0, 130, 0, 0]
                halign: "center"
                cols: 1
                rows: 5

                MDIconButton:
                    id: led_red
                    icon: "led-variant-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    md_bg_color: [1, 0, 0, 0.1]
                    radius: [12, ]
                
                MDIconButton:
                    id: led_green
                    icon: "led-variant-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    md_bg_color: [0, 1, 0, 0.1]
                    radius: [12, ]

                MDIconButton:
                    id: led_blue
                    icon: "led-variant-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    md_bg_color: [0, 0, 1, 0.1]
                    radius: [12, ]

                MDIconButton:
                    id: piezometro
                    icon: "volume-mute"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    md_bg_color: [1, 1, 1, 0.1]
                    radius: [24, ]

                MDIconButton:
                    id: servo_motor
                    icon: "sync"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    md_bg_color: [1, 1, 1, 0.1]
                    radius: [24, ]


            KivyCamera:
                id: camera
                size_hint_x: None
                width: 1000
                halign: "center"
                pos_hint: {"center_x": .5, "center_y": .5}
                # size_hint: .9, .1
        
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
                id: buttonClassification
                halign: 'center'
                text: root.buttonClassification
                disabled: root.isDisabledClassification
                on_press: root.onClassification()
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

            MDRoundFlatIconButton:
                icon: "camera"
                halign: 'center'
                id: buttonCamera
                text: root.buttonCamera
                on_press: root.onCamera()

            MDRoundFlatIconButton:
                icon: "checkerboard"
                id: buttonGrayScale
                halign: 'center'
                text: root.buttonGrayScale
                disabled: True
                on_press: root.onGrayScale()
            
            MDRoundFlatIconButton:
                icon: "checkerboard"
                id: buttonBackground
                halign: 'center'
                text: root.buttonBackground
                disabled: True
                on_press: root.onBackground()
            
            MDRoundFlatIconButton:
                icon: "allergy"
                id: buttonClassification
                halign: 'center'
                text: root.buttonClassification
                disabled: root.isDisabledClassification
                on_press: root.onClassification()

# <TabSettings>
#     GridLayout: 
#         rows: 2
#         cols: 2
#         height: 50
#         pos_hint: {'center_x': 0.5, 'center_y': 0.5}

#         MDLabel:
#             halign: "center"
#             height: 50
#             text: "Path Model"
        
#         MDLabel:
#             id: pathModel
#             halign: "center"
#             text: root.getLabelPathModel()
#             height: 50
#             pos_hint: {"center_y": .5}
        
            
#         MDLabel:
#             halign: "center"
#             height: 50
#             text: "Path File Label"
        
#         MDLabel:
#             id: pathLabel
#             halign: "center"
#             height: 50
#             text: root.getLabelPathLabel()

#     BoxLayout:
#         orientation: "vertical"
#         heith: 2000
#         size_hint_x: None
        
#         MDLabel:
#             halign: "center"

    



'''
##########################################


