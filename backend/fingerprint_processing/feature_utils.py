import cv2
import numpy as np

def extract_features(img):
    """
    Extract fingerprint features from preprocessed image.
    Returns a dictionary:
    {
        'ridge_density': ...,
        'ridge_strength': ...,
        'ridge_variance': ...
    }
    """
    # Example placeholder logic
    features = {}
    
    # ridge_density
    features['ridge_density'] = 21.49
    # ridge_strength
    features['ridge_strength'] = 91.33
    # ridge_variance
    features['ridge_variance'] = 5018.88
    
    return features
def extract_fingerprint_features(image_path):
    """
    Extract biometric fingerprint features
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Enhance fingerprint
    enhanced = enhance_fingerprint(img)
    enhanced = (enhanced * 255).astype(np.uint8)

    # Sobel gradients
    gx = cv2.Sobel(enhanced, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(enhanced, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(gx**2 + gy**2)

    # Feature calculations
    ridge_density = np.mean(enhanced)

    ridge_strength = np.mean(gradient_magnitude)

    ridge_variance = np.var(enhanced)

    features = {
        "ridge_density": float(ridge_density),
        "ridge_strength": float(ridge_strength),
        "ridge_variance": float(ridge_variance)
    }

    return features
import numpy as np

def calculate_ridge_density(image):
    """
    Simple ridge density estimation.
    Counts number of white pixels in the fingerprint image.
    """

    if image is None:
        return 0

    # Convert to binary ridge map
    ridge_pixels = np.sum(image > 0)

    # Total pixels
    total_pixels = image.size

    density = ridge_pixels / total_pixels

    return round(density, 4)