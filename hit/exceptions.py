class CaptchaNeeded(Exception):
    def __init__(self, *args: object) -> None:
        self.sess = args[0]
        self.image = args[1]


class LoginFailed(Exception):
    pass
