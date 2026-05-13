import cv2
from skimage.metrics import structural_similarity as ssim

def compare_images(ref_path, upload_path):
    original = cv2.imread(ref_path)
    test = cv2.imread(upload_path)

    test = cv2.resize(test, (original.shape[1], original.shape[0]))

    gray1 = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(gray1, gray2, full=True)
    return score * 100