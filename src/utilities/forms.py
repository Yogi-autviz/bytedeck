from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


from utilities.models import VideoResource

class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoResource
        fields = ["title", "video_file"]



# http://koensblog.eu/blog/7/multiple-file-upload-django/
from django.utils.translation import ugettext_lazy as _


class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        # attrs['class'] += 'btn'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size': u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    # def validate(self, data):
    #     super(MultiFileField, self).validate(data)
    #     num_files = len(data)
    #     if len(data) and not data[0]:
    #         num_files = 0
    #     if num_files < self.min_num:
    #         raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
    #         return
    #     elif self.max_num and  num_files > self.max_num:
    #         raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
    #     for uploaded_file in data:
    #         if uploaded_file.size > self.maximum_file_size:
    #             raise ValidationError(self.error_messages['file_size'] % { 'uploaded_file_name': uploaded_file.name})

    def clean(self, data, initial=None):
        super(MultiFileField, self).clean(data, initial=None)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return
        elif self.max_num and num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
        if num_files > 0:
            for uploaded_file in data:
                if uploaded_file.size > self.maximum_file_size:
                    raise ValidationError(self.error_messages['file_size'] % {'uploaded_file_name': uploaded_file.name})
        return data

        # def clean(self, data, initial=None):
        #     super(MultiFileField, self).clean(data, initial)
        #     try:
        #         # content_type = file.content_type
        #         # if content_type in self.content_types:
        #         if file._size > self.max_upload_size:
        #             raise ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
        #                 filesizeformat(self.max_upload_size), filesizeformat(file._size)))
        #         # else:
        #             # raise ValidationError(_('Filetype not supported.'))
        #     except AttributeError:
        #         pass

# http://k
