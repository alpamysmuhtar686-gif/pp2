import pygame

def rotate_center(image, angle, center):
    # Rotate the image by the given angle
    rotated_image = pygame.transform.rotate(image, angle)
    # Get the rotated image's rectangle centered at the specified point
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    # Return the rotated image and its rectangle
    return rotated_image, new_rect