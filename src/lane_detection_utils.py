import numpy as np
import cv2 as cv

def preprocess_image(image, threshold=175, size=(640, 360)):
    """
    Preprocess the input image to create a binary mask and a resized grayscale image.

    Parameters:
    - image: Original image in BGR format.
    - threshold: Pixel intensity threshold for binary mask creation.
    - size: Target size for resizing the image (width, height).

    Returns:
    - binary_mask: Binary mask where pixels above the threshold are set to 1.
    - resized_image: Resized version of the original image.
    """

    # Resize the image to the specified size
    resized_image = cv.resize(image, size)

    # Convert the resized image to grayscale
    image_gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)

    # Initialize a binary mask with the same shape as the grayscale image
    binary_mask = np.zeros_like(image_gray)

    # Set mask pixels to 1 where the grayscale pixel value is above the threshold
    binary_mask[image_gray > threshold] = 1

    return binary_mask, resized_image


def plot_results(image, mask, ymin, ymax, cx, l_index, r_index = None):
    """
    Overlays the mask on the image with a red stripe indicating the driving path.

    Parameters:
    - image: Original image.
    - mask: Binary mask of the road.
    - ymin: Minimum y-coordinate for the stripe.
    - ymax: Maximum y-coordinate for the stripe.
    - cx: Center x-coordinate of the image.
    - index: Width of the stripe to the left of the center.

    Returns:
    - result: Image with the overlay.
    """
    result = image.copy()
    mask_rgb = cv.cvtColor(mask, cv.COLOR_GRAY2RGB) * 255
    
    # Apply mask to the specified stripe area
    result[ymin:ymax, :, :] = mask_rgb[ymin:ymax, :, :]

    # Add red stripe indicating the path
    result[ymin:ymax, cx - l_index:cx, 1:] = 0

    if not r_index is None:
      result[ymin:ymax, cx: cx + r_index, 0] = 0


    return result

def find_line_center(stripe, min_pixels):
    success = True
    mean_x = None
    index = None

    # Sum the stripe along the vertical axis
    summed = np.sum(stripe, axis=0)

    # Cumulative sum to determine the path width
    cumsum = np.cumsum(summed)

    if np.max(cumsum) < min_pixels:
      success = False
      return success, mean_x, index

    # Find the index where the cumulative sum exceeds min_pixels
    index = np.argmax(cumsum > min_pixels)

    # Get the non-zero coordinates within the stripe up to the index
    y, x = np.nonzero(stripe[:, :index])

    # Compute the mean x-coordinate of the non-zero pixels
    mean_x = np.mean(x)

    if np.isnan(mean_x):
      success = False

    return success, mean_x, index
    
def find_driving_path(image, mask, ymin=270, ymax=285, min_pixels=55, lane_width = 309):
    """
    Finds the driving path within the image based on the mask.

    Parameters:
    - image: Original image.
    - mask: Binary mask of the road.
    - ymin: Minimum y-coordinate for the stripe.
    - ymax: Maximum y-coordinate for the stripe.
    - min_pixels: Minimum number of pixels to consider for the driving path.

    Returns:
    - result: Image with the overlay indicating the driving path.
    """
    height, width = mask.shape
    cx = width // 2  # Center x-coordinate

    # Crop the stripe between ymin and ymax and split it into left and right halves
    l_stripe = mask[ymin:ymax, :cx][::-1]  # Left stripe, flipped vertically
    # r_stripe = mask[ymin:ymax, cx:]        # Right stripe

    # Find the center of the left and right lines
    success_left, xleft, index_left = find_line_center(l_stripe, min_pixels)
    # success_right, xright, index_right = find_line_center(r_stripe, min_pixels)

    if success_left:

      # Transform the left and right line centers to image coordinates
      xleft = cx - xleft
      # xright = cx + xright

      # Calculate lane center
      lane_center = xleft + lane_width//2

      # Caluclate Offset
      offset = int(cx - lane_center)

      # Generate the result image with the overlay
      result = plot_results(image, mask, ymin, ymax, cx, index_left)

      return success_left, result, offset
    
    else:

      return success_left, None, None