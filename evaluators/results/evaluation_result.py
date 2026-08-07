class EvaluationResult:

    @staticmethod
    def build(
        *,
        generator,
        requirement,
        generated_json,
        schema,
        testcase,
        coverage,
        deepeval,
        score,
    ):

        return {
    #Generator        
    "generator": generator,

    #Requirments Information
    "requirementId": requirement.requirement_id,
    "title": requirement.title,
    "description": requirement.description,
    "businessRules": requirement.business_rules,
    "priority": requirement.priority,

    #Generated Output
    "generatedJson": generated_json,

    #Ground Truth 
    "groundTruth": requirement.ground_truth,

    #Testcase format validation
    "schemaValidation": schema,
    "testCaseValidation": testcase,
    "coverageValidation": coverage,

    #DeepEval Metrics
    "deepEval": deepeval,

    #Overall Score
    "overall": score,
}