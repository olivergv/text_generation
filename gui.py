from kivy.lang import Builder
import torch
from kivymd.app import MDApp
import kivy
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from googletrans import Translator
import tensorflow as tf
import wikipedia
from text_generator import write
import os
from text_generator import gpu
from text_generator import get_response
from text_generator import prepare_model
from text_generator import prepare_data
from text_generator import write_with_own_data

gpu()
prepare_model()
KV = '''
MDScreen:
    query: query
    MDBoxLayout:
        orientation: "vertical"


        MDToolbar:
            title: "JARVIS"
            right_action_items: [["dots-vertical", lambda x: app.callback()]]

        MDLabel:
            text: "Jarvis Text Generation:"
            halign: "center"
            font_style: "H5"

        MDLabel:
            text: "In order for Jarvis to create the essay, simple write the desired topic, or the path to a txt file"
            halign: "center"

        MDTextFieldRect:
            size_hint: 1, None
            height: "200dp"
            id: query
        MDRectangleFlatIconButton:
            text: "Create essay!"
            icon: "typewriter"
            pos_hint: {"center_x": .5, "center_y": .5}
            font_size: "32sp"
            on_press: app.btn()
            on_press: app.btn2()
            on_release: app.show_dialog()

'''

class Test(MDApp):
    def callback(self):
        text = "hello"
        return text

    def btn(self):
            write(self.root.ids.query.text, 'essay')

    def btn2(self):
        self.dialog = MDDialog(
            text="Generating Essay, Please wait... Generation takes up to 5 minutes, depending on the word count, when finished, the essay would be saved at: " + os.path.abspath("essay.txt")

            )
        self.dialog.open()


    def build(self):
        return Builder.load_string(KV)

    def show_dialog(self):
        self.dialog = MDDialog(
            text="The essay has been succesfully created, and saved at" + os.path.abspath('essay.txt')

        )
        self.dialog.open()


Test().run()
