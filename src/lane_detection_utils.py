import numpy as np
import cv2 as cv


def remove_small_components(image, min_size=30):
    num_labels, labels_im = cv.connectedComponents(image)

    # Create an output image the same size as the original, initialized to zero (black)
    output = np.zeros_like(image)

    for label in range(1, num_labels):
        # Create a mask where the components are equal to the current label
        component = labels_im == label
        if np.sum(component) > min_size:  # If the component is larger than min_size
            output[component] = 255

    return output

def preprocess_image(image, lower_white=None, upper_white=None, size=(640, 360)):
    """
    Preprocess an image to extract a mask of the road based on specified white color ranges.
    Allows resizing the image to a specified size for consistent processing.

    Args:
    image (np.array): The input image in BGR color space.
    lower_white (np.array): Lower bound for the white color range, default if None.
    upper_white (np.array): Upper bound for the white color range, default if None.
    size (tuple): The target size for resizing the image, format (width, height).

    Returns:
    np.array: A binary mask where white areas within the specified range are marked.
    """

    # Set default color ranges using the 'or' operator for concise default assignment
    lower_white = lower_white or np.array([0, 0, 170], dtype=np.uint8)
    upper_white = upper_white or np.array([255, 30, 255], dtype=np.uint8)

    # Resize the image to the specified size for uniform processing
    resized_image = cv.resize(image, size, interpolation=cv.INTER_LINEAR)

    # Convert the image from BGR to HSV color space
    hsv_image = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV)

    # Create a mask to isolate the white regions in the image
    mask = cv.inRange(hsv_image, lower_white, upper_white)

    # Remove noise using morphological operations
    mask = remove_small_components(mask)

    # Normalize the mask to binary values (0 or 1) by integer division
    mask = mask // 255

    return mask, resized_image

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
    total_pixels = None

    # Sum the stripe along the vertical axis
    summed = np.sum(stripe, axis=0)

    # Cumulative sum to determine the path width
    cumsum = np.cumsum(summed)

    total_pixels = np.max(cumsum)

    if total_pixels < min_pixels:
      success = False
      return success, mean_x, index, total_pixels

    # Find the index where the cumulative sum exceeds min_pixels
    index = np.argmax(cumsum > min_pixels)

    # Get the non-zero coordinates within the stripe up to the index
    y, x = np.nonzero(stripe[:, :index])

    # Compute the mean x-coordinate of the non-zero pixels
    mean_x = np.mean(x)

    if np.isnan(mean_x):
      success = False

    return success, mean_x, index, total_pixels
    
def find_driving_path(image, mask, ymin=260, ymax=275, min_pixels=55, lane_width = 309):
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
    success_left, xleft, index_left, total_pixels = find_line_center(l_stripe, min_pixels)
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

      return success_left, result, offset, total_pixels
    
    else:

      return success_left, None, None, None