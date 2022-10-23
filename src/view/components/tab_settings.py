from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase

from utility.constants import Constants


class TabSettings(MDFloatLayout, MDTabsBase, BoxLayout):
    
    def getLabelPathModel(self):
        return Constants.PATH_MODEL

    def changePathModel(self):
        # self.random_number = str(random.randint(1, 100))
        print(f'[DEBUG] pathModel: {self.ids.pathModel.text}')

    def getLabelPathLabel(self):
        return Constants.PATH_LABEL

