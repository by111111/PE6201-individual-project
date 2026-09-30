# Evaluation dataset

`evaluation_cases.csv` contains ten synthetic SME scenarios created before the experiment. No personal, client, or confidential data is included.

Every case uses the same fields collected by the application: industry/company type, use case, intended pilot group, duration, pain point, constraint, and start date. The same ten cases are evaluated under two conditions:

1. **Structured workflow:** the form fields and fixed system prompt in `pilot_planner/core.py`.
2. **Raw baseline:** one direct user request with no system prompt and no form-enforced output structure.

Both conditions are scored on five binary components: named test group, dated stages, numeric success measure with baseline/comparison, specified feedback instrument, and explicit human approval checkpoint. The cases are version-controlled so the test set cannot be changed after seeing the results.

