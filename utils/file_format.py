images_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4']


def get_ext(file_path: str) -> str:
    return file_path.split('.')[-1]


def is_video(file_path: str) -> bool:
    ext = get_ext(file_path)
    return ext in video_ext


def is_photo(file_path: str) -> bool:
    ext = get_ext(file_path)
    return ext in images_ext
