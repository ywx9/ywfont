class Command:
    def __init__(self, name: str):
        self.name = name
        self.params = []
    def print(self):
        print(f"Command: {self.name}, Params: {self.params}")


# SVGのpath要素を分解して返す
def parse_path(d: str) -> list[Command]:
    commands = d.split()
    path = []
    current_command = None
    for cmd in commands:
        if cmd in ["M", "m", "L", "l", "H", "h", "V", "v", "C", "c", "S", "s", "Q", "q", "T", "t", "A", "a", "Z", "z"]:
            current_command = Command(cmd)
            path.append(current_command)
        elif current_command:
            current_command.params.append(float(cmd))
    return path
