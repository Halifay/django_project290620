from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    gem_type = models.CharField(max_length=64)
    gem_quantity = models.IntegerField()
    deal_time = models.DateTimeField()

    def __str__(self):
        return (self.customer.name + ' bought ' + str(self.gem_quantity) +
                ' ' + self.gem_type + ' gems for ' + str(self.total_price) + '$ the ' + str(self.deal_time))


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
