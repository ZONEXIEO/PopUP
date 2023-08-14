import tkinter as tk
from PIL import Image, ImageTk
import multiprocessing
import random, time, requests
import win32gui
import win32.lib.win32con as win32con


class ImageWindow:
    image_paths = [""] # List here all images you want to have pop up
    approve = requests.get("").text # Fetch approval status 

    def __init__(self, root, image_path, x, y):
        self.root = root  # Store the root (main) window of the application
        self.image_path = image_path  # Store the path to the image file
        self.x = x  # Store the x-coordinate for the image's initial position
        self.y = y  # Store the y-coordinate for the image's initial position

        # Open and resize the image to fit the screen dimensions
        self.image = Image.open(image_path)
        self.image = self.image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

        # Create a PhotoImage object from the resized image
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a Label widget and attach the PhotoImage to display the image
        self.label = tk.Label(root, image=self.photo)
        self.label.place(x=x, y=y)  # Set the initial position of the label on the window
        self.label.pack(fill="both", expand=True)  # Pack the label to expand and fill available space





def open_image():
    x = random.randint(0,1920) # Random x positon on the screen
    y = random.randint(0,1080) # Random y positon on the screen
    # You can change x and y according to your screen resoulution. #

    random_show_time = random.randint(2,5)

    if ImageWindow.approve == "1":
        root = tk.Tk()
        root.title(f"Image {random.randint(0,100000)}")
        root.geometry(f"+{x}+{y}")  # Set initial position of root window
        root.geometry(f"600x600") # Screen size
        image_window = ImageWindow(root, random.choice(ImageWindow.image_paths), x, y)
        
        # Continuously check the condition and break when it's not met

        start_req_time = time.time()  # Get the current time
        start_new_image_time = time.time() # Get the current time


        while ImageWindow.approve == "1": # Check if approval is granted
            root.update()
            elapsed_req_time = time.time() - start_req_time
            elapsed_new_image_time = time.time() - start_new_image_time
            
            # Fetch updated approval status every 1 second

            if (elapsed_req_time >= 1):
                ImageWindow.approve = requests.get("").text
                start_req_time = time.time()

            # Display a new image in different positon (x,y) after a random show time interval
            if (elapsed_new_image_time >= random_show_time):
                root.destroy()
                open_image()
            
        
        root.quit()  # Quit the mainloop when condition is not met


def hide_console():
    the_program_to_hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

def main():
    iterations = 40 # That's the maximum number of images that can be opened at the same time
    for i in range(iterations):
        process = multiprocessing.Process(target=open_image) # Create a new process that runs the open_image function
        time.sleep(0.1)
        process.start()

if __name__ == "__main__":
    hide_console()
    main()
    exit()
