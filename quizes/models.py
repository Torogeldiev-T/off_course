from django.db import models
from courses.models import ItemBase
from accounts.models import User

DIFFICULTY_CHOICES = (("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard"))


class Quiz(ItemBase):
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the quiz in minutes")
    required_score = models.IntegerField(
        help_text="Required score to pass the quiz in %"
    )
    diffculty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)

    class Meta:
        verbose_name_plural = "Quezes"

    def __str__(self):
        return f"{self.topic} - {self.title}"

    def get_questions(self):
        return self.questions.all()


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

    def get_answers(self):
        return self.answers.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Question: {self.question},  Answer: {self.text},  Correct {self.correct}"
        )


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"Your quiz result on: {self.quiz} is {self.score} percent"
