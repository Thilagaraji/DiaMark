import cv2
import numpy as np
import fingerprint_enhancer
import cv2
import numpy as np
import fingerprint_enhancer

def preprocess_fingerprint(image_path):
    """
    Complete preprocessing pipeline
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enhanced = fingerprint_enhancer.enhance_fingerprint(gray)
    enhanced = (enhanced * 255).astype("uint8")
    denoised = cv2.GaussianBlur(enhanced, (5, 5), 0)
    _, binary = cv2.threshold(denoised, 127, 255, cv2.THRESH_BINARY)
    return binary


def load_image(image_path):
    """
    Load fingerprint image
    """
    img = cv2.imread(image_path)
    return img


def convert_to_gray(img):
    """
    Convert image to grayscale
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def enhance_fingerprint(gray_img):
    """
    Enhance fingerprint ridges
    """
    enhanced = fingerprint_enhancer.enhance_fingerprint(gray_img)

    # convert boolean image to uint8 (0–255)
    enhanced = (enhanced * 255).astype("uint8")

    return enhanced


def remove_noise(img):
    """
    Remove noise using Gaussian Blur
    """
    blurred = cv2.GaussianBlur(img, (5,5), 0)
    return blurred


def binarize_image(img):
    """
    Convert to binary image
    """
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return binary


def preprocess_image(image_path):
    """
    Complete preprocessing pipeline
    """
    img = load_image(image_path)
    gray = convert_to_gray(img)
    enhanced = enhance_fingerprint(gray)
    denoised = remove_noise(enhanced)
    binary = binarize_image(denoised)
    return binary