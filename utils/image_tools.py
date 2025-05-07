import redis
import io
import os
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from celery import shared_task
from django.conf import settings

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@shared_task
def resize_and_store_in_redis(image_path, width, height, image_type):
    try:
        # Read the image data from storage
        original_image = default_storage.open(image_path, 'rb').read()

        # Store the image temporarily in Redis
        r.set(image_path, original_image)

        # Open image using PIL and resize it
        image = Image.open(io.BytesIO(original_image))
        image = image.resize((width, height))

        # Save the resized image to an in-memory file (buffer)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # Determine the correct upload path based on image type
        if image_type == 'profile':
            upload_to = 'profiles/'
        elif image_type == 'banner':
            upload_to = 'banners/'
        elif image_type == 'ads':
            upload_to = 'ads/'
        else:
            raise ValueError("Invalid image type")

        # Create a new filename for the resized image
        new_image_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_resized.jpg"

        # Save resized image to disk (using the correct path under mooshak/media/)
        resized_image = InMemoryUploadedFile(buffer, None, new_image_name, 'image/jpeg', buffer.tell(), None)
        resized_image_path = default_storage.save(f"mooshak/media/{upload_to}{new_image_name}", resized_image)

        # Delete the original image from storage and Redis after processing
        if default_storage.exists(image_path):
            default_storage.delete(image_path)

        r.delete(image_path)  # Remove original image from Redis

        # Return the path to the resized image
        return resized_image_path

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None
