from django import forms

from adminx.helpers import datbase


class CDBForm(forms.Form):
    sql = forms.CharField(help_text="结尾不必跟分号（;）")
    def clean_sql(self):
        sql = self.cleaned_data.get("sql")
        re = datbase.editor_cdb(sql)
        if re != 0:
            raise forms.ValidationError("%s" % re)
        return re
