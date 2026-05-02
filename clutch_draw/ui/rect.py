# Checks if a point (x, y) is inside a rectangle that is defined by its position and size
def inside_rect(x: int, y: int, left: int, top: int, width: int, height: int) -> bool:
    return left <= x <= left + width and top <= y <= top + height
