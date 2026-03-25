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
            raise ValueError('Invalid image file')

        if algorithm == 'gamma':
            return gamma_correction(img, gamma)
        elif algorithm == 'log':
            return log_transform(img)
        elif algorithm == 'stretch':
            return contrast_stretching(img)
        else:
            raise ValueError('Unknown algorithm')
    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        raise

def gamma_correction(img, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype('uint8')
    return cv2.LUT(img, table)

def log_transform(img):
    c = 255 / np.log(1 + np.max(img))
    log_img = c * np.log(1 + img)
    return np.array(log_img, dtype=np.uint8)

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

