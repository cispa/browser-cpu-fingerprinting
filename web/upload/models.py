from django.db import models

class BenchmarkResult(models.Model):
    model = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    times = models.JSONField()
    benchmark_results = models.JSONField()
    b64_charts = models.JSONField()

    def __str__(self):
        return self.model 