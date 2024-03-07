class learnable_agent:

    def __init__(self, user_model, learner_model):
        self.learner_model = learner_model
        self.usermodel = user_model

    def learn(self, train, evaluator):
        return self.learner_model(train=train, tooluser=self.usermodel, evaluator=evaluator)

    def __call__(self, data):
        return self.usermodel(problem_input=data)
