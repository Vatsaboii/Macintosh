import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from tkinter import Tk, Label, Button, filedialog, Entry, StringVar

class DataCompressionUtility:
    def __init__(self, master):
        self.master = master
        master.title("Data Compression Utility")

        self.label = Label(master, text="Enter the path of the image:")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()

        self.browse_button = Button(master, text="Browse", command=self.browse_image)
        self.browse_button.pack()

        self.compress_button = Button(master, text="Compress", command=self.compress_image)
        self.compress_button.pack()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.entry.delete(0, 'end')
        self.entry.insert(0, file_path)

    def show(self, img, title="Image"):
        figure = plt.figure(figsize=(10, 10))
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        plt.axis('off')
        plt.title(title)
        plt.show()

    def compress_image(self):
        image_path = self.entry.get()

        if os.path.exists(image_path):
            img = cv2.imread(image_path)

            if img is not None:
                initial_size = os.path.getsize(image_path) / 1024  # in KB

                # Adjust the threshold value to control compression
                threshold = 100  # Adjust this threshold as needed
                encoded_R = self.RLE_encoding(img, bits=8, threshold=threshold)

                if encoded_R is not None:
                    dimg_R = self.RLE_decode(encoded_R, img.shape[:2])

                    if dimg_R is not None:
                        self.show(img, title="Original Image")
                        self.show(dimg_R[0], title="Decoded Image")

                        # Save the decoded image in the same directory as the original image
                        original_directory, image_filename = os.path.split(image_path)
                        save_path = os.path.join(original_directory, "decoded_" + image_filename)
                        cv2.imwrite(save_path, dimg_R[0])
                        print(f"Decoded image saved in the same directory as the original image: {save_path}")

                        # Display sizes of the initial and decompressed images
                        decoded_size = os.path.getsize(save_path) / 1024  # in KB
                        print(f"Initial image size: {initial_size} KB")
                        print(f"Decompressed image size: {decoded_size} KB")
                    else:
                        print("Error decoding the image.")
                else:
                    print("Error encoding the image.")
            else:
                print("Error loading the image. Please check the file path and file format.")
        else:
            print("Invalid file path. Please select a valid image file.")

    def RLE_encoding(self, img, bits=8, threshold=100):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)

        encoded = []
        count = 0
        prev = None

        for pixel in binary_img.flatten():
            if prev is None:
                prev = pixel
                count += 1
            else:
                if prev != pixel:
                    encoded.append((count, prev))
                    prev = pixel
                    count = 1
                else:
                    if count < (2 ** bits) - 1:
                        count += 1
                    else:
                        encoded.append((count, prev))
                        prev = pixel
                        count = 1
        encoded.append((count, prev))

        return np.array(encoded)

    def RLE_decode(self, encoded, shape):
        decoded = []
        channel_data = []

        for rl in encoded:
            r, p = rl[0], rl[1]
            channel_data.extend([p] * r)

        decoded_channel = np.array(channel_data)
        decoded_channel.resize(shape)
        decoded.append(decoded_channel)

        return np.array(decoded)

root = Tk()
app = DataCompressionUtility(root)
root.mainloop()
