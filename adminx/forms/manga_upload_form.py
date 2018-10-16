from django import forms


class MangaUploadForm(forms.Form):
    file = forms.FileField(label="漫画zip文件", help_text="上传漫画资源文件")
