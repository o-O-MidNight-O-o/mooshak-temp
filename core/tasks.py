from celery import shared_task
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import redis
r = redis.Redis.from_url(getattr(settings, "REDIS_URL", "redis://localhost:6379/0"))

@shared_task
def send_email_task(subject, message, recipient_list, from_email=None):
    """
    General email task that can be used for various purposes (verification, ads, etc.)
    """
    send_mail(
        subject,
        message,
        from_email or settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

@shared_task
def send_verification_email(user_id, domain, subject="Verify your email address"):
    from django.contrib.auth.models import User

    user = User.objects.get(id=user_id)

    message = render_to_string(
        "emails/verification_email.html",
        {"user": user, "domain": domain}
    )

    send_mail(
        subject,
        '',  # plain text empty
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message  # ✅ Send HTML message properly
    )
    
@shared_task
def send_ad_email(user_id, subject, message, domain):
    """
    Send promotional emails (ads) to the user.
    """
    from django.contrib.auth.models import User

    user = User.objects.get(id=user_id)

    message = render_to_string(
        "emails/advertisement_email.html",
        {"user": user, "subject": subject, "message": message, "domain": domain}
    )

    send_email_task.delay(subject, message, [user.email])  # Send ad email


@shared_task
def resize_and_store_in_redis(profile_id, field_name, width, height):
    import traceback
    from PIL import Image
    try:
        from profiles.models import UserProfile
        profile = UserProfile.objects.get(id=profile_id)
        image_field = getattr(profile, field_name)
        if not image_field:
            print(f"[ERROR] No image found in field {field_name} for profile {profile_id}")
            return None
        image_path = image_field.path


        # Move this check BEFORE opening the file
        base_name, ext = os.path.splitext(os.path.basename(image_path))
        ext = ext.lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            ext = '.jpg'

        if base_name.endswith('_resized'):
            print(f"[DEBUG] Image already resized, skipping: {image_path}")
            return image_path

        print(f"[DEBUG] Starting resize task for {image_path}")
        print(f"[DEBUG] Does original exist? {default_storage.exists(image_path)}")

        original_image = default_storage.open(image_path, 'rb').read()
        r.set(image_path, original_image)

        image = Image.open(io.BytesIO(original_image))
        print(f"[DEBUG] Original image size: {image.size}")

        # If already correct size, just rename and save
        if image.size == (width, height):
            print(f"[DEBUG] Image already correct size, just renaming.")
            new_image_name = f"{base_name}_resized{ext}"
            upload_to = "profiles/"
            if field_name == "banner_image":
                upload_to = "banners/"
            resized_image_path = f"{upload_to}{new_image_name}"
            default_storage.save(resized_image_path, InMemoryUploadedFile(
                io.BytesIO(original_image), None, new_image_name, f'image/{ext.replace(".", "")}', len(original_image), None
            ))
            setattr(profile, field_name, resized_image_path)
            profile.save(update_fields=[field_name])
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
            r.delete(image_path)
            print(f"[DEBUG] Renamed image saved to {resized_image_path}")
            return resized_image_path

        # Otherwise, crop and resize as before
        original_width, original_height = image.size
        target_ratio = width / height
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            new_width = int(target_ratio * original_height)
            offset = (original_width - new_width) // 2
            box = (offset, 0, offset + new_width, original_height)
        else:
            new_height = int(original_width / target_ratio)
            offset = (original_height - new_height) // 2
            box = (0, offset, original_width, offset + new_height)

        image = image.crop(box)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        print(f"[DEBUG] Resized image size: {image.size}")

        new_image_name = f"{base_name}_resized{ext}"
        upload_to = "profiles/"
        if field_name == "banner_image":
            upload_to = "banners/"
        resized_image_path = f"{upload_to}{new_image_name}"

        buffer = io.BytesIO()
        save_format = 'JPEG' if ext in ['.jpg', '.jpeg'] else 'PNG'
        image.save(buffer, format=save_format)
        buffer.seek(0)

        default_storage.save(resized_image_path, InMemoryUploadedFile(
            buffer, None, new_image_name, f'image/{save_format.lower()}', buffer.tell(), None
        ))

        setattr(profile, field_name, resized_image_path)
        profile.save(update_fields=[field_name])
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
        r.delete(image_path)
        print(f"[DEBUG] Resized image saved to {resized_image_path}")
        return resized_image_path

    except Exception as e:
        print(f"[ERROR] Error processing image for profile {profile_id}: {e}")
        traceback.print_exc()
        return None