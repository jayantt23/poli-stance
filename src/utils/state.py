class ArticleState:
    def __init__(self, text):
        self.text = text
        self.sentences = []
        self.entities = []
        self.ideology_label = None
        self.evidence = []
        self.stances = {}
        self.frame = None