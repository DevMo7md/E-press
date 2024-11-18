from django.db import models
from django.contrib.auth.models import User
from docx import Document
from django.core.files.base import ContentFile
import os
# Create your models here.


class Journalist(models.Model):
    author =  models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='journalist/photos/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}'

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='category/photos/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        # تحويل العنوان والنص إلى أحرف صغيرة
        self.name = self.name.lower()
        super().save(*args, **kwargs)    


class Article(models.Model):
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=False)
    info = models.TextField(null=True, blank=False)
    content = models.TextField(null=True, blank=False)
    word_file = models.FileField(upload_to='articles/word_files/', null=True, blank=True)  # حقل لملف وورد
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_special = models.BooleanField(default=False)
    is_trend = models.BooleanField(default=False)
    num_of_comments = models.IntegerField(default=0, null=True, blank=True)
    num_of_views = models.IntegerField(default=0, null=True, blank=True)

    # حقل لتتبع المستخدمين الذين شاهدوا المقال
    viewed_by = models.ManyToManyField(User, related_name='viewed_articles', blank=True)




    def __str__(self):
        return f'{self.title}'
    

    def save(self, *args, **kwargs):
    
        # تحقق مما إذا كان هناك ملف وورد تم رفعه
        
        if self.word_file:
            doc = Document(self.word_file)
            content = []
            # استخراج النصوص من الفقرات
            for para in doc.paragraphs:
                content.append(para.text)

            # استخراج الصور وحفظها
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    img_data = rel.target_part.blob
                    image_name = os.path.basename(rel.target_part.partname)
                    image_file = ContentFile(img_data, name=image_name)
                    self.image.save(image_name, image_file, save=False)  # حفظ الصورة

            self.content = "\n".join(content)  # دمج النصوص في حقل المحتوى
            self.word_file.delete(save=False)  # حذف ملف الوورد بعد قراءته

        super().save(*args, **kwargs)  # حفظ النموذج بعد التعديل

        self.num_of_comments = Comment.objects.filter(article=self).count()

        # حفظ المقال مرة أخرى بعد تحديث عدد التعليقات
        super().save(update_fields=['num_of_comments'])        

class Advertisment(models.Model):

    content = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.content}'

class Comment(models.Model):

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):

        return f' علق على--  {self.article.title} --{self.creator}'

    def save (self, *args, **kwargs):
        super().save(*args, **kwargs)
        # تحديث عدد التعليقات في المقال بعد إضافة تعليق جديد
        self.article.save()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)
    viewed_by = models.ManyToManyField(User, related_name='viewed_message', blank=True)
    is_viewd = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f'{self.subject}: ارسل حول موضوع {self.user.username}'