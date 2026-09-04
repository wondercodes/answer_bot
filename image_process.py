import base64
from io import BytesIO

class ImageProcessor:

    @staticmethod
    def encode_image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    @staticmethod
    def decode_base64_to_image(base64_string):
        image_data = base64.b64decode(base64_string)
        return BytesIO(image_data)
