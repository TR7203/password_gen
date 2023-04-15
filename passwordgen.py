import csv
import random
import string
import os
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class PasswordGeneratorApp(MDApp):
    def build(self):
        # Define the layout using KivyMD's built-in widgets
        layout = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(20)
    padding: dp(20)

    MDLabel:
        text: 'Password Generator'
        theme_text_color: 'Secondary'

    MDTextField:
        id: password_length_field
        hint_text: 'Password Length'
        color_mode: 'custom'
        #line_color_normal: 0, 0, 1, 1 # Set line color to blue when not focused
        #line_color_focus: 0, 1, 0, 1  # Set line color to green when focused
        input_filter: 'int'
        helper_text_mode: 'on_focus'
        helper_text: 'Enter a number'
        max_text_length: 5



    MDRaisedButton:
        text: 'Generate Password'
        on_release: app.generate_password()

    MDLabel:
        id: password_label
        text: ''
        theme_text_color: 'Primary'
''')

        return layout

    def generate_password(self):
        # Get the password length from the text field
        password_length = self.root.ids.password_length_field.text

        if password_length:
            # Convert the input to an integer
            password_length = int(password_length)

            # Call the password generation function and update the label with the generated password
            password = self._generate_password(password_length)
            self.root.ids.password_label.text = 'Generated Password: {}'.format(password)

            # Export the password to a local CSV file
            self._export_password_to_csv(password)
        else:
            # If no password length is entered, display an error message
            self.root.ids.password_label.text = 'Error: Please enter a password length'

    def _generate_password(self, length):
        """Generate a random password of given length."""
        # Define characters to choose from for each type of character
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = string.punctuation

        # Create a pool of characters to choose from
        pool = lowercase + uppercase + digits + special_chars

        # Ensure that the password length is at least 8 characters
        if length < 8:
            length = 8

        # Generate the password by randomly selecting characters from the pool
        password = ''.join(random.choice(pool) for _ in range(length))

        return password

    def _export_password_to_csv(self, password):
        i = 1
        while True:
            filename = f"password_{i}.csv"
            if not os.path.exists(filename):
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Password"])
                    writer.writerow([password])
                print(f"Password has been exported to {filename}")
                break
            i += 1

    def export_password(self):
        password = self.password_label.text
        if password:
            self._export_password_to_csv(password)
        else:
            print("No password generated yet!")


if __name__ == '__main__':
    PasswordGeneratorApp().run()
