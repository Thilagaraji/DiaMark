import cv2

def preprocess_fingerprint(image_path):
    """
    Load and preprocess fingerprint image
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Resize for consistency
    img = cv2.resize(img, (256, 256))

    # Noise reduction
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Binary threshold
    _, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

    return thresh
# import cv2
# import numpy as np

# def preprocess_image(image_path):
#     """
#     Load and preprocess a fingerprint image
#     """
#     # Load image
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         raise FileNotFoundError(f"Fingerprint image not found: {image_path}")

#     # Example preprocessing steps (you can adjust to your existing code)
#     # 1️⃣ Normalize
#     img = cv2.equalizeHist(img)

#     # 2️⃣ Gaussian blur to reduce noise
#     img = cv2.GaussianBlur(img, (3, 3), 0)

#     # 3️⃣ Optional: binarization / ridge enhancement (if implemented)
#     # img = your_ridge_enhancement_function(img)

#     return img