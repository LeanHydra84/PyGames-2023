class CaptureState:
    def __init__(self, state):
        self.reference_state = state
        pass

    def draw(self):
        pass

    def register_click(self):
        pass

    def register_click(self, position):
        pass

    def update(self):
        pass

    def togglecapture(self):
        if self.reference_state.captureState == None:
            self.reference_state.captureState = self
        else:
            self.reference_state.captureState = None
