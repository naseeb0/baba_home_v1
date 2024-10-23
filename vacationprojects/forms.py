# forms.py in your vacationprojects app
from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 80, 'rows': 30},
            mce_attrs={
                'elementpath': False,
                'contextmenu': 'link image table',
                'setup': '''function(editor) {
                    editor.on('change', function() {
                        editor.save();
                    });
                    // Fix for dark mode
                    editor.on('init', function() {
                        var doc = editor.getDoc();
                        var style = doc.createElement('style');
                        style.innerHTML = `
                            body.dark-mode {
                                background-color: #fff !important;
                                color: #333 !important;
                            }
                        `;
                        doc.head.appendChild(style);
                    });
                }'''
            }
        )
    )

    class Meta:
        model = BlogPost
        fields = '__all__'