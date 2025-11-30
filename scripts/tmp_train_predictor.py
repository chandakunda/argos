from ml.enrollment_predictor.models.enrollment_predictor import EnrollmentPredictor

dataset = "data/datasets/processed/enrollment_dataset.csv"
model = EnrollmentPredictor()
model.train(dataset)

print("Training complete. Demo prediction:")
print(model.predict({
    "attendance": 0.85,
    "assignments": 0.9,
    "midterm": 0.88,
    "course_load": 4
}))
