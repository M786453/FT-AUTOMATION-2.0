import tkinter as tk
from tkinter import messagebox

class Popup:

    def show(title, message):
        
        # Create a Tkinter root window
        root = tk.Tk()

        # Hide the root window
        root.withdraw()

        # Create a custom popup window
        popup = tk.Toplevel(root)
        popup.title(title)
        popup.geometry("300x100")

        # Create a label for the popup text
        label = tk.Label(popup, text=message)
        label.pack(pady=20)


        # Configure the popup window to be topmost
        popup.attributes("-topmost", True)

        # Define a function to close the popup
        def close_popup():
            popup.destroy()
            root.quit()

        # # Schedule the close_popup function to be called after 3000 milliseconds (3 seconds)
        root.after(2000, close_popup)

        root.mainloop()
    
