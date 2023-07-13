from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name

        # Faculty_details


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=200)
    mail_id = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    connect_id = models.IntegerField()
    role = models.IntegerField()   # roles {1,2,3} 1(Admin), 2(HOD), 3(Staff)


class Faculty_details(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=200, unique=True)
    role = models.ForeignKey(Users, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='photo/%Y/%m/%d', default='images/Screenshot_3.png')
    id_number = models.IntegerField()
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200, unique=True)
    designation = models.CharField(max_length=200, default='designation')
    date_of_join = models.DateField(default=timezone.now)
    department = models.CharField(max_length=200, default='department')
    qualififcation = models.CharField(max_length=200, default='qualification')
    assessment_period = models.IntegerField(default=0)  # auto update....
    experience = models.IntegerField(default=0)
    bio = models.CharField(max_length=200, default='No Bio yet.')

    # Internal test evaluation


class Subjects(models.Model):
    subject_image = models.CharField(max_length=200)
    subject_name = models.CharField(max_length=200, unique=True)
    subject_code = models.CharField(max_length=200, unique=True)
    semester = models.IntegerField()
    department = models.CharField(max_length=200)
    discription = models.CharField(
        max_length=200, default='No Discription yet.')


class Subject_handled(models.Model):
    faculty_id = models.IntegerField()
    subject_staff = models.ForeignKey(
        Faculty_details, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=200)
    target_pass = models.CharField(max_length=200, default='10')
    actual_pass = models.CharField(max_length=200, default='10')


class Test_evaluation(models.Model):
    # it's can be access to subject.name, subject.code
    subject_detials = models.ForeignKey(
        Subject_handled, on_delete=models.CASCADE)
    test = models.CharField(max_length=200)
    target_pass = models.CharField(max_length=200)
    actual_pass = models.CharField(max_length=200)


class Details(models.Model):
    faculty_id = models.IntegerField()
    image = models.ImageField(
        upload_to='photo/%Y/%m/%d', default='images/user_image.png')
    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    designation = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    coming_from = models.CharField(max_length=200)
    mail_id = models.CharField(max_length=200)


# chat_room
class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=10000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    room = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)


class class_enrolled(models.Model):
    user_id = models.IntegerField()
    mail_id = models.CharField(max_length=200)
    class_id = models.IntegerField(primary_key=True)
    subject_code = models.CharField(max_length=200)


class ClassRooms(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    owner = models.ForeignKey(Faculty_details, on_delete=models.CASCADE)
    class_image = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=200, unique=True)
    semester = models.IntegerField()
    department = models.CharField(max_length=200)
    class_type = models.CharField(max_length=200)
    discription = models.CharField(
        max_length=200, default='No Discription yet.')


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/Student/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mail_id = models.CharField(max_length=40,unique=True) 
    parent_mail_id = models.CharField(max_length=40, unique=True)
    mobile = models.CharField(max_length=20, null=False)
    joinned_year = models.DateField(default=timezone.now)
    role_no = models.IntegerField(unique=True)
    department = models.CharField(max_length=40)

    @property

    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/Teacher/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    role = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)
    department = models.CharField(max_length=40)
    salary = models.PositiveIntegerField(null=True)
    Annauni_num = models.CharField(max_length=40, default="0000000")

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'),
           ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

# Blog..................................


class blog(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, default='UnTitled')
    userid = models.IntegerField()
    description = models.CharField(
        max_length=200, default="Author not provied any description")
    content = models.CharField(
        max_length=2000, default="Author not provied any description")
    blog_profile_img = models.CharField(
        max_length=2000, default="https://www.equalityhumanrights.com/sites/default/files/styles/listing_image/public/default_images/blog-teaser-default-full_5.jpg?itok=YOsTg-7X")
    blog_type = models.CharField(
        max_length=2000, default="Blog")
    categories = models.CharField(max_length=200)
    reviewed_by = models.IntegerField()
    updated_date = models.DateField(default=timezone.now)

class Draft_blog(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    title = models.CharField(max_length=200, default='UnTitled')
    description = models.CharField(
        max_length=200, default="Author not provied any description")
    content = models.CharField(
        max_length=2000, default="Author not provied any description")
    blog_profile_img = models.CharField(
        max_length=2000, default="https://www.equalityhumanrights.com/sites/default/files/styles/listing_image/public/default_images/blog-teaser-default-full_5.jpg?itok=YOsTg-7X")
    blog_type = models.CharField(
        max_length=2000, default="Blog")
    categories = models.CharField(max_length=200)
    reviewed = models.BooleanField()
    Submitreview = models.BooleanField()
    updated_date = models.DateField(default=timezone.now)





# Gallery.............................

class Gallery(models.Model):
    G_id = models.IntegerField(primary_key=True)
    image = models.ImageField(
        upload_to='Gallery/%Y/%m/%d', default='images/user_image.png')
    categories = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

# Notes..............................


class NoteCourse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    course_id = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ebook(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    course = models.ForeignKey(NoteCourse, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ebooks')

    def __str__(self):
        return self.title


class EbookForClass(models.Model):
    id = models.IntegerField(primary_key=True)
    cover_image = models.CharField(max_length=100)
    Class_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    course = models.ForeignKey(NoteCourse, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ebooks')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class URLForClass(models.Model):
    id = models.IntegerField(primary_key=True)
    Class_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    course = models.ForeignKey(NoteCourse, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ebooks')

    def __str__(self):
        return self.title


class Attendees(models.Model):
    id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    subject_states = models.CharField(max_length=50)
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.class_id


class Sec_Daily_test_mark(models.Model):
    id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    mark = models.IntegerField()
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.class_id


class Internal_test_mark(models.Model):
    id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    mark = models.IntegerField()
    assesment_no = models.IntegerField()
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.class_id


class Daily_test_mark(models.Model):
    id = models.IntegerField(primary_key=True)
    class_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    mark = models.IntegerField()
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.class_id


class daily_test(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=100)
    student_id = models.IntegerField()
    Mark = models.CharField(max_length=50)
    Date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    cover_image = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    notes_title = models.CharField(max_length=100)
    regulation = models.CharField(max_length=100)
    subcode = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='notes/')

    def __str__(self):
        return self.notes_title


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    event_name = models.CharField(max_length=100)
    event_photo = models.URLField()
    event_description = models.TextField()
    poster_link = models.URLField()

    def __str__(self):
        return self.event_name


class Testimonials(models.Model):
    T_id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='Testimonials/%Y/%m/%d', default='images/user_image.png')
    description = models.CharField(max_length=200)
    categories = models.CharField(max_length=200)
    last_updated_date = models.DateField(default=timezone.now)


class logo(models.Model):
    L_id = models.IntegerField(primary_key=True)
    Reson = models.CharField(max_length=200,default='None...!')
    image = models.ImageField(
        upload_to='logo', default='images/user_image.png')
    last_updated_date = models.DateField(default=timezone.now)

    class Meta:
        get_latest_by = ['image']


class FooterEditPage(models.Model):
    id = models.IntegerField(primary_key=True)
    InstituteName = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    PhoneNumber = models.CharField(max_length=200)
    EXN = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    last_updated_date = models.DateField(default=timezone.now)


class SocialMediaLinks(models.Model):
    id = models.IntegerField(primary_key=True)
    website = models.CharField(max_length=200)
    Twitter = models.CharField(max_length=200)
    Facebook = models.CharField(max_length=200)
    Instagram = models.CharField(max_length=200)
    LinkedIn = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    last_updated_date = models.DateField(default=timezone.now)

# classRoom ........................

# class ClassRommNotification(models.Model):
#     id = models.IntegerField(primary_key=True)
#     from_ = course=models.ForeignKey(User,on_delete=models.CASCADE)
#     subject = models.CharField(max_length=50)
#     date = models.DateField(default=timezone.now)
#     file = models.FileField(upload_to='ebooks')

#     def __str__(self):
#         return self.from_

# class ClassRoomWorks(models.Model):
#     id = models.IntegerField(primary_key=True)
#     from_ = course=models.ForeignKey(User,on_delete=models.CASCADE)
#     work = models.CharField(max_length=50)
#     date = models.DateField(default=timezone.now)
#     file = models.FileField(upload_to='ebooks')

#     def __str__(self):
#         return self.from_

# class Notes(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=100)
#     subject = models.CharField(max_length=50)
#     course = models.ForeignKey(NoteCourse, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='Notes')

#     def __str__(self):
#         return self.title

class Pages(models.Model):
    id=models.IntegerField(primary_key=True)
    usr_id = models.IntegerField()
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    html = models.TextField()
    css = models.TextField()
    preview_link = models.TextField()


class Department(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    short_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class YouTubeLink(models.Model):
    class_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    link = models.URLField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50)
    class_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notifications(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.IntegerField()
    to_user = models.IntegerField()
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    redirect_location = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    read_receipt = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    update_by = models.IntegerField()
    class_id = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.title

class Assignment_mark(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    Assignment_id = models.IntegerField()
    mark = models.IntegerField()
    
    
class Upload_Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    update_by = models.IntegerField()
    File = models.FileField(upload_to='upload_assignments/')
    Assignment_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload_Assignment ID: {self.id}"


class SocialMedia(models.Model):
    id = models.IntegerField(primary_key=True)
    std_id = models.IntegerField(unique=True)
    portfolio = models.URLField(blank=True, null=True,default="Not Updated")
    twitter = models.URLField(blank=True, null=True ,default="Not Updated")
    linkedin = models.URLField(blank=True, null=True ,default="Not Updated")
    github = models.URLField(blank=True, null=True ,default="Not Updated")
    facebook = models.URLField(blank=True, null=True ,default="Not Updated")
    instagram = models.URLField(blank=True, null=True ,default="Not Updated")


class BotControl(models.Model):
    id = models.IntegerField(primary_key=True)
    usr_id = models.IntegerField()
    toggle = models.IntegerField(blank=True)
    
