def inside_rect(x: int, y: int, left: int, top: int, width: int, height: int) -> bool:
    return left <= x <= left + width and top <= y <= top + height
