
import numpy as np
import cv2
from sklearn.feature_extraction.image import extract_patches_2d


def get_preprocessed_patches(image_path, num_patches_for_image=8):
    img = cv2.imread(image_path)[...,::-1].astype(np.float32)
    img = local_contrast_normalization(img)
    patches = select_patches(
        extract_patches(img),
        num_patches_for_image
    )
    return [np.expand_dims(patch, axis=0) for patch in patches]


def local_contrast_normalization(image):
    kernel = (0, 0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    float_gray = gray.astype(np.float32)

    blur = cv2.GaussianBlur(float_gray, kernel, sigmaX=3, sigmaY=3)
    num = float_gray - blur

    blur = cv2.GaussianBlur(num*num, kernel, sigmaX=3, sigmaY=3)
    den = cv2.pow(blur, 0.5) + np.finfo(float).eps

    gray = num / den

    return cv2.normalize(gray, dst=gray, alpha=0.0, beta=1.0, norm_type=cv2.NORM_MINMAX)


def extract_patches(image):
    return extract_patches_2d(
        image=image,
        patch_size=(64, 64),
        max_patches=300,
        random_state=3,
    )


def select_patches(patches, n=8):
    # Selects n patches from a patch sequence sorted by patches standart deviations
    half_n = int(n / 2)
    mean_values = [np.std(p) for p in patches]
    sorted_sequence = [p for _, p in sorted(zip(mean_values, patches), key=lambda x: x[0])]
    return sorted_sequence[int(len(patches) / 2) - half_n : int(len(patches) / 2) + half_n]
