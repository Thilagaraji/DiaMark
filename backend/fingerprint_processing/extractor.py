import numpy as np
import cv2

from fingerprint_processing.feature_utils import calculate_ridge_density

def extract_features(image):

    ridge_density = calculate_ridge_density(image)

    # 🔥 NEW FEATURES

    # Ridge thickness (approx)
    ridge_thickness = np.mean(image)

    # Ridge ratio (white vs black)
    ridge_ratio = np.sum(image > 128) / image.size

    # Minutiae approximation (edge count)
    edges = cv2.Canny(image, 50, 150)
    minutiae_points = np.sum(edges > 0)

    features = {
        "ridge_density": ridge_density,
        "ridge_thickness": ridge_thickness,
        "ridge_ratio": ridge_ratio,
        "minutiae_points": minutiae_points
    }

    return features