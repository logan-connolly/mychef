import debugpy


def start_debugging_server():
    debugpy.listen(("0.0.0.0", 5678))
