class HistoryStack: 
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
            cls._instance.undo_stack = []
            cls._instance.redo_stack = []
            cls._instance.max_stack_size = 10
        return cls._instance
    
    def add_to_undo(self, changes):
        if changes:
            if len(self.undo_stack) > self.max_stack_size:
                self.undo_stack.pop(0)
            self.undo_stack.append(changes)

    def add_to_redo(self, changes):
        if changes:
            if len(self.redo_stack) > self.max_stack_size:
                self.redo_stack.pop(0)
            self.redo_stack.append(changes)