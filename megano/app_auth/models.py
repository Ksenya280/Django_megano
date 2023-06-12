import os
from uuid import uuid4


def avatar_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return f'avatars/{instance.user.username}_{uuid4().hex}{ext}'

