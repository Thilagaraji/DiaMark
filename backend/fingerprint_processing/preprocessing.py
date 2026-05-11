import cv2
import numpy as np



# =========================
# LOAD IMAGE
# =========================
def load_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    return img


# =========================
# CONVERT TO GRAYSCALE
# =========================
def convert_to_gray(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return gray


# =========================
# ENHANCE FINGERPRINT
# =========================
def enhance_fingerprint(gray_img):

    # Improve contrast
    enhanced = cv2.equalizeHist(gray_img)

    # Smooth small noise
    enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

    return enhanced
# =========================
# REMOVE NOISE
# =========================
def remove_noise(img):

    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    return blurred


# =========================
# BINARIZE IMAGE
# =========================
def binarize_image(img):

    _, binary = cv2.threshold(
        img,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return binary


# =========================
# RESIZE IMAGE
# =========================
def resize_image(img):

    resized = cv2.resize(img, (256, 256))

    return resized


# =========================
# MAIN PREPROCESS FUNCTION
# =========================
def preprocess_fingerprint(image_path):

    img = load_image(image_path)

    gray = convert_to_gray(img)

    enhanced = enhance_fingerprint(gray)

    denoised = remove_noise(enhanced)

    binary = binarize_image(denoised)

    resized = resize_image(binary)

    return resized