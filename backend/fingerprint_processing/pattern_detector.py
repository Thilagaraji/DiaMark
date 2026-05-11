import cv2
import numpy as np

# ─────────────────────────────────────────────────────────────────
# STEP 1 – FOREGROUND MASK
# ─────────────────────────────────────────────────────────────────
def build_foreground_mask(img, block_size=16, std_threshold=8):
    """
    Returns a boolean grid (num_r × num_c).
    True  → block contains ridges (foreground).
    False → background / empty.
    Threshold lowered to 8 (from 10) to handle faint real ink prints.
    """
    rows, cols = img.shape
    num_r = rows // block_size
    num_c = cols // block_size
    mask = np.zeros((num_r, num_c), dtype=bool)
    for i in range(num_r):
        for j in range(num_c):
            r0, r1 = i * block_size, (i + 1) * block_size
            c0, c1 = j * block_size, (j + 1) * block_size
            if np.std(img[r0:r1, c0:c1]) > std_threshold:
                mask[i, j] = True
    return mask


# ─────────────────────────────────────────────────────────────────
# STEP 2 – ORIENTATION FIELD  (doubled-angle method)
# ─────────────────────────────────────────────────────────────────
def compute_orientation_field(img, block_size=16):
    """
    Returns orientation field (num_r × num_c) in radians [-π/2, π/2].
    Uses Hong et al. (1998) doubled-angle formulation.
    """
    rows, cols = img.shape
    num_r = rows // block_size
    num_c = cols // block_size

    gx = cv2.Sobel(img.astype(np.float64), cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img.astype(np.float64), cv2.CV_64F, 0, 1, ksize=3)

    Vx = np.zeros((num_r, num_c), dtype=np.float64)
    Vy = np.zeros((num_r, num_c), dtype=np.float64)

    for i in range(num_r):
        for j in range(num_c):
            r0, r1 = i * block_size, (i + 1) * block_size
            c0, c1 = j * block_size, (j + 1) * block_size
            bx = gx[r0:r1, c0:c1]
            by = gy[r0:r1, c0:c1]
            Vx[i, j] = 2.0 * np.sum(bx * by)
            Vy[i, j] = np.sum(bx ** 2 - by ** 2)

    Vx = cv2.GaussianBlur(Vx, (5, 5), 1.0)
    Vy = cv2.GaussianBlur(Vy, (5, 5), 1.0)

    return 0.5 * np.arctan2(Vx, Vy)


# ─────────────────────────────────────────────────────────────────
# STEP 3 – POINCARÉ INDEX
# ─────────────────────────────────────────────────────────────────
def poincare_index(orientation, i, j):
    """
    Poincaré index at grid cell (i, j) using 8 CCW neighbours.
        +0.5  → core   (loop centre / whorl inner ring)
        -0.5  → delta  (divergence point)
         0    → regular ridge area
    Returns 0.0 for boundary cells.
    """
    neighbours = [
        (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
        (i,     j + 1),
        (i + 1, j + 1), (i + 1, j), (i + 1, j - 1),
        (i,     j - 1),
        (i - 1, j - 1),
    ]
    rows, cols = orientation.shape
    angles = []
    for (r, c) in neighbours:
        if 0 <= r < rows and 0 <= c < cols:
            angles.append(orientation[r, c])
        else:
            return 0.0

    total = 0.0
    for k in range(len(angles) - 1):
        d = angles[k + 1] - angles[k]
        if d > np.pi / 2:    d -= np.pi
        elif d < -np.pi / 2: d += np.pi
        total += d

    return total / (2.0 * np.pi)


# ─────────────────────────────────────────────────────────────────
# STEP 4 – CLUSTER SUPPRESSION
# ─────────────────────────────────────────────────────────────────
def cluster_points(pts, min_dist=5):
    """
    Merge adjacent detections of the same singular point into one.
    pts: list of (row, col, value)
    Returns list of (row, col).
    """
    if not pts:
        return []
    kept = []
    used = set()
    for idx, (i, j, v) in enumerate(pts):
        if idx in used:
            continue
        cluster = []
        for idx2, (i2, j2, v2) in enumerate(pts):
            if abs(i2 - i) <= min_dist and abs(j2 - j) <= min_dist:
                cluster.append((i2, j2))
                used.add(idx2)
        ci = int(np.mean([x[0] for x in cluster]))
        cj = int(np.mean([x[1] for x in cluster]))
        kept.append((ci, cj))
    return kept


# ─────────────────────────────────────────────────────────────────
# STEP 5 – DETECT SINGULAR POINTS  (foreground-aware)
# ─────────────────────────────────────────────────────────────────
def detect_singular_points(orientation, fg_mask, threshold=0.45, margin_frac=0.12):
    """
    Only checks blocks that are:
      (a) inside the central region (inside margin_frac border)
      (b) inside the fingerprint foreground
      (c) surrounded by 8 foreground neighbours

    This eliminates false detections at image edges.
    Returns (num_cores, num_deltas).
    """
    rows, cols = orientation.shape
    margin_r = max(2, int(rows * margin_frac))
    margin_c = max(2, int(cols * margin_frac))

    raw_cores  = []
    raw_deltas = []

    for i in range(margin_r, rows - margin_r):
        for j in range(margin_c, cols - margin_c):
            if not fg_mask[i, j]:
                continue
            all_fg = all(
                0 <= r < rows and 0 <= c < cols and fg_mask[r, c]
                for (r, c) in [
                    (i-1,j-1),(i-1,j),(i-1,j+1),
                    (i,  j+1),(i+1,j+1),(i+1,j),
                    (i+1,j-1),(i,  j-1)
                ]
            )
            if not all_fg:
                continue

            pi = poincare_index(orientation, i, j)
            if pi >= threshold:
                raw_cores.append((i, j, pi))
            elif pi <= -threshold:
                raw_deltas.append((i, j, pi))

    cores  = cluster_points(raw_cores,  min_dist=5)
    deltas = cluster_points(raw_deltas, min_dist=5)

    print(f"[Poincaré] Cores={len(cores)}, Deltas={len(deltas)}")
    return len(cores), len(deltas)


# ─────────────────────────────────────────────────────────────────
# STEP 6 – CLASSIFY  (robust to partial/faint prints)
# ─────────────────────────────────────────────────────────────────
def classify_pattern(num_cores, num_deltas, orientation_std_deg=50):

    print("Cores:", num_cores)
    print("Deltas:", num_deltas)
    print("Orientation STD:", orientation_std_deg)

    # ARCH
    if num_cores == 0 and num_deltas == 0:
        if orientation_std_deg < 30:
            return "Arch"
        else:
            return "Loop"

    # LOOP
    elif num_cores == 1 and num_deltas <= 1:
        return "Loop"

    # WHORL
    elif num_cores >= 1 and num_deltas >= 2:
        return "Whorl"

    # ARCH fallback
    elif num_cores == 0 and num_deltas >= 1:
        return "Arch"

    # Default
    return "Loop"

# ─────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────
def detect_pattern(img):
    """
    Fingerprint pattern detection using Poincaré Index with:
    - Foreground-aware singular-point detection (no edge noise)
    - Cluster suppression (each singular point counted once)
    - Robust classification for faint/partial real ink prints

    Input : preprocessed grayscale numpy array (uint8)
    Output: "Arch", "Loop", or "Whorl"
    """
    # 1. Enhance ridges
    # 1. Use already preprocessed image
    enhanced = img.copy()
    # 2. Foreground mask
    fg_mask = build_foreground_mask(enhanced, block_size=16, std_threshold=8)

    # 3. Orientation field
    orientation = compute_orientation_field(enhanced, block_size=16)

    # 4. Orientation std (used as tiebreaker for 0-singular-point case)
    fg_angles = np.degrees(orientation[fg_mask]) if np.any(fg_mask) else np.array([0.0])
    orientation_std_deg = float(np.std(fg_angles))
    print(f"[Orientation] std={orientation_std_deg:.2f}°")

    # 5. Singular points
    num_cores, num_deltas = detect_singular_points(
        orientation, fg_mask, threshold=0.45, margin_frac=0.12
    )

    # 6. Classify
    pattern = classify_pattern(num_cores, num_deltas, orientation_std_deg)
    cv2.imwrite("processed_debug.png", img)
    print(f"[Pattern Result] → {pattern}")
    return pattern