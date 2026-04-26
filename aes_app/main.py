# main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.properties import BooleanProperty
import crypto_manager

class AESApp(MDApp):
    password_hidden = BooleanProperty(True)

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light" # Default theme
        return Builder.load_file("encryptor.kv")

    def toggle_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

    def toggle_password_visibility(self):
        self.password_hidden = not self.password_hidden

    def encrypt_text(self, plain_text):
        password = self.root.ids.password_input.text.strip()
        if not password:
            return "Error: Password cannot be empty."
        if not plain_text:
            return "Error: Input text cannot be empty."

        try:
            result = crypto_manager.encrypt(plain_text, password)
            Clipboard.copy(result)
            return result
        except Exception as e:
            return f"Encryption Error: {str(e)}"

    def decrypt_text(self, encrypted_text):
        password = self.root.ids.password_input.text.strip()
        if not password:
            return "Error: Password cannot be empty."
        if not encrypted_text:
            return "Error: Input text cannot be empty."

        try:
            return crypto_manager.decrypt(encrypted_text, password)
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_fields(self):
        self.root.ids.input_text.text = ""
        self.root.ids.output_text.text = ""
        self.root.ids.password_input.text = ""

if __name__ == "__main__":
    AESApp().run()
