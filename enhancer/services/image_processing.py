import cv2
import numpy as np
import base64
import logging

logger = logging.getLogger(__name__)

def enhance_image(image_bytes, algorithm, gamma=1.0):
    """
    Enhance image using point operations.
    """
    try:
        # Read image from bytes
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            logger.error("Failed to decode image. Buffer might be corrupted.")
            raise ValueError('Invalid image data')
        algo = str(algorithm).lower().strip()
        if algo == 'gamma':
            return gamma_correction(img, gamma)
        elif algo == 'log':
            return log_transform(img)
        elif algo == 'clahe':
            return clahe_enhancement(img)
        elif 'stretch'in algo:
            return contrast_stretching(img)
        else:
            logger.warning(f"Unsupported algorithm received: {algo}")
            raise ValueError(f'Unsupported algorithm: {algo}')
    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        raise

def gamma_correction(img, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype('uint8')
    return cv2.LUT(img, table)

def log_transform(img):
    img_float = img.astype(np.float64)
    max_pixel_value = np.max(img_float)
    if max_pixel_value == 0:
        return img
    c = 255 / np.log(1 + max_pixel_value)
    log_img = c * np.log(1 + img_float)
    return np.array(log_img, dtype=np.uint8)

def clahe_enhancement(img):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge((l, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

def contrast_stretching(img):
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img.copy()
    
    min_val, max_val, _, _ = cv2.minMaxLoc(img_gray)
    if max_val > min_val:
        stretched = ((img_gray - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        if len(img.shape) == 3:
            stretched = cv2.cvtColor(stretched, cv2.COLOR_GRAY2BGR)
        return stretched
    return img

def image_to_base64(img):
    """
    Convert OpenCV image to base64 string.
    """
    _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    img_str = base64.b64encode(buffer).decode()
    return f'data:image/jpeg;base64,{img_str}'

