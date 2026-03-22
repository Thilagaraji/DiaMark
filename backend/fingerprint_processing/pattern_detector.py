import cv2
import numpy as np
from fingerprint_enhancer import enhance_fingerprint


def load_image(path):
    """
    Load fingerprint image in grayscale
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")

    return img


def preprocess_image(img):
    """
    Enhance fingerprint ridges using fingerprint_enhancer
    """
    enhanced = enhance_fingerprint(img)

    # convert boolean to uint8 image
    enhanced = (enhanced * 255).astype(np.uint8)

    return enhanced


def compute_gradients(img):
    """
    Compute image gradients using Sobel operator
    """
    gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    return gx, gy


def get_orientation_field(img, block_size=16):
    """
    Compute ridge orientation field using block-based method
    """

    rows, cols = img.shape

    orientation = np.zeros((rows // block_size, cols // block_size))

    gx, gy = compute_gradients(img)

    for i in range(0, rows - block_size, block_size):
        for j in range(0, cols - block_size, block_size):

            gxi = gx[i:i + block_size, j:j + block_size]
            gyi = gy[i:i + block_size, j:j + block_size]

            v_x = 2 * np.sum(gxi * gyi)
            v_y = np.sum(gxi**2 - gyi**2)

            angle = 0.5 * np.arctan2(v_x, v_y)

            orientation[i // block_size, j // block_size] = angle

    return orientation


def analyze_orientation_distribution(orientation):
    """
    Analyze ridge orientation distribution
    """

    angles = np.degrees(orientation).flatten()

    angles = np.mod(angles, 180)

    mean_angle = np.mean(angles)
    std_angle = np.std(angles)

    return mean_angle, std_angle


def classify_pattern(mean_angle, std_angle):
    """
    Improved fingerprint classification
    """

    # Whorl → very circular pattern
    if std_angle > 55:
        return "Whorl"

    # Loop → moderate orientation variation
    elif 30 < std_angle <= 55:
        return "Loop"

    # Arch → mostly straight ridges
    else:
        return "Arch"
# def detect_pattern(img):
#     """
#     Full fingerprint pattern detection pipeline
#     """

#     img = load_image(img)

#     enhanced = preprocess_image(img)

#     orientation = get_orientation_field(enhanced)

#     mean_angle, std_angle = analyze_orientation_distribution(orientation)

#     # Debug information (useful for tuning)
#     print("Mean Orientation:", mean_angle)
#     print("Std Orientation:", std_angle)

#     pattern = classify_pattern(mean_angle, std_angle)

#     return pattern
def detect_pattern(img):
    """
    Full fingerprint pattern detection pipeline
    img: preprocessed grayscale fingerprint image (NumPy array)
    """
    # img is already preprocessed, no need to reload

    # Enhance if needed (optional)
    # enhanced = enhance_fingerprint(img)
    enhanced = img  # already preprocessed

    # Compute orientation field
    orientation = get_orientation_field(enhanced)

    mean_angle, std_angle = analyze_orientation_distribution(orientation)

    # Debug info
    print("Mean Orientation:", mean_angle)
    print("Std Orientation:", std_angle)

    pattern = classify_pattern(mean_angle, std_angle)

    return pattern