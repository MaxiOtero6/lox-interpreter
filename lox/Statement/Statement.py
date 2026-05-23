class Statement():
    def ast_label(self):
        return self.__class__.__name__

    def ast_children(self):
        return []
