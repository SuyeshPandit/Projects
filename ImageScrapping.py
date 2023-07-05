import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def download_images(person_name, num_images):
    # Create a directory to save the images
    save_dir = person_name
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    count = 0
    page_num = 0

    while count < num_images:
        # Perform Google search
        query = quote(person_name + ' photo')
        url = f"https://www.google.com/search?q={query}&tbm=isch&start={page_num * 5}"
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and download the images
        for img in soup.select('img[src^="https://"]'):
            img_url = img['src']
            try:
                # Download the image
                response = requests.get(img_url)
                response.raise_for_status()

                # Save the image to the directory
                file_name = f"{person_name}_{count + 1}.jpg"
                file_path = os.path.join(save_dir, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                count += 1

                print(f"Downloaded image {count}/{num_images}")

                # Stop when desired number of images is reached
                if count >= num_images:
                    break

            except requests.exceptions.RequestException as e:
                print(f"Failed to download image: {e}")

        # Stop when desired number of images is reached
        if count >= num_images:
            break

        # Move to the next page of search results
        page_num += 1

# Prompt the user for the person's name
person_name = input("Enter the person's name: ")

# Download 50 images of the person
download_images(person_name, 50)
