import os
import shutil
import random
from PIL import Image

def find_unique_icons(folder_path):
    # Find all images in "spell-images" folder
    image_files = [
        f for f in os.listdir(folder_path) 
        if f.lower().endswith(('png', 'jpg', 'jpeg'))
    ]
    
    unique_images = []
    image_hashes = set()
    
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        img = Image.open(img_path)
        img_hash = hash(img.tobytes())  # Create a hash of the image content

        if img_hash not in image_hashes:
            unique_images.append(img_path)
            image_hashes.add(img_hash)

    return unique_images

def resize_images_to_fit(image_paths, wallpaper_size=(1920, 1080)):
    # Shuffle the images randomly to help distribute colors
    random.shuffle(image_paths)
    
    # Calculate number of rows and columns based on number of images
    num_images = len(image_paths)
    cols = int(num_images ** 0.5)
    rows = (num_images // cols) + (1 if num_images % cols else 0)
    
    # Calculate the maximum width and height each image can have
    img_width = wallpaper_size[0] // cols
    img_height = wallpaper_size[1] // rows

    resized_images = []
    for img_path in image_paths:
        img = Image.open(img_path)

        # Convert to RGBA if the image has a palette (mode "P") to avoid transparency issues
        if img.mode == 'P':
            img = img.convert("RGBA")

        # Resize the image while maintaining aspect ratio
        img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)

        resized_images.append(img)

    return resized_images, rows, cols, img_width, img_height

def create_checkerboard_wallpaper(resized_images, rows, cols, img_width, img_height, wallpaper_size=(1920, 1080)):
    # Create a blank wallpaper canvas (black background)
    wallpaper = Image.new('RGB', wallpaper_size, (0, 0, 0))  # Start with black background

    # Loop through and create a checkerboard pattern
    x_offset = 0
    y_offset = 0
    img_index = 0

    for row in range(rows):
        for col in range(cols):
            if img_index < len(resized_images) and (row + col) % 2 == 0:
                # Place an image in every other position (checkerboard effect)
                img = resized_images[img_index]
                wallpaper.paste(img, (x_offset, y_offset))
                img_index += 1

            # Update the x offset
            x_offset += img_width

        # Move to the next row
        x_offset = 0
        y_offset += img_height

    return wallpaper

def save_wallpaper(wallpaper, output_folder='.', base_filename='wallpaper.png'):
    # Check if the file exists and add an incrementer if necessary
    output_path = os.path.join(output_folder, base_filename)
    base_name, ext = os.path.splitext(base_filename)
    
    increment = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_folder, f"{base_name}{increment}{ext}")
        increment += 1
    
    wallpaper.save(output_path, 'PNG')
    print(f"Wallpaper saved to {output_path}")

def main():
    source_folder = './spell-images'  # Folder containing the spell icons
    output_folder = '.'  # Save in the current directory

    # Step 1: Find unique images in the "spell-images" folder
    icon_images = find_unique_icons(source_folder)

    if not icon_images:
        print("No relevant images found.")
    else:
        # Step 2: Resize the images to fit the wallpaper
        resized_images, rows, cols, img_width, img_height = resize_images_to_fit(icon_images)

        # Step 3: Create the checkerboard wallpaper
        wallpaper = create_checkerboard_wallpaper(resized_images, rows, cols, img_width, img_height)

        # Step 4: Save the wallpaper with an incrementer to avoid overwriting
        save_wallpaper(wallpaper, output_folder)

if __name__ == '__main__':
    main()
