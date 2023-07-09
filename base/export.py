from import_export import resources
from import_export.fields import Field
from base.models import Attendees, Internal_test_mark

class AttendeesResource(resources.ModelResource):
    id = Field(attribute='id')
    class_id = Field(attribute='class_id')
    user_name = Field(attribute='user_name')
    roll_no = Field(attribute='roll_no')
    subject_states = Field(attribute='subject_states')
    Date = Field(attribute='Date')

    class Meta:
        model = Attendees
        
class Internal_test_markResource(resources.ModelResource):
    id = Field(attribute='id', column_name='ID')
    class_id = Field(attribute='class_id', column_name='Class Id')
    roll_no = Field(attribute='roll_no', column_name='Roll No')
    subject = Field(attribute='subject', column_name='Subject')
    mark = Field(attribute='mark', column_name='Mark')
    assesment_no = Field(attribute='assesment_no', column_name='Assesment No')
    Date = Field(attribute='Date', column_name='Date')

    class Meta:
        model = Internal_test_mark
