#blog/forms.py
from django import forms
from .models import Post
from django.forms import ValidationError

class PostForm(forms.Form):
    title = forms.CharField()
    #title = forms.CharField(required=True, label='글 제목',placeholder="tte")
    #위처럼 하면 cleand검사 안함
    content = forms.CharField(widget=forms.Textarea)
    def clean_title(self):
        title = self.cleand_data.get('title','')
        if '바보' in title:
            raise ValidationError('바보스러운 기운이 난다.')
        return title.strip()
    def clean(self):
        super(PostEditForm,self).clean()
        title = self.cleand_data.get('title','')
        content = self.cleand_data.get('content','')
        if '안녕' in title:
            self.add_error('title', '안녕' )
        if '안녕' in content:
            self.add_error('content', '안녕' )

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'tags',)
        #fields = '__all__'
