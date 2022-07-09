class ModelsTracker:
    _instance = None
    models:set

    def __init__(self,models:list=[]):
        self.models = set(models,)

    def register(self,model):
        self.models.add(model)
    def is_register(self,model):
        for registerModel in self.models:
            if isinstance(model,registerModel):
                return True
        return False


modelTracker = ModelsTracker()