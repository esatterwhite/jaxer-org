from django import forms
from django.conf import settings
class MooEditor(forms.Textarea):
    class Media:
        js = ('js/editor/editor_r4.js','js/MooEditable.Extras.js', 'js/MooEditable.UI.MenuList.js')
        css = {'all':('css/editor_black.css','css/MooEditable.css',)}
    def __init__(self, attrs={}):
        return super(MooEditor, self).__init__(attrs)
    
    def render (self, name, value, attrs=None):

        rendered = super(MooEditor, self).render(name,value,attrs)
        return rendered + ('''<script type="text/javascript">
                                    var MEDIA_URL = '%s';
                                    window.addEvent('domready', function(){
                                        var moo = $('id_%s').mooEditable({
                                        actions:"h2 h4 p | bold italic | insertunorderedlist indent outdent | undo redo | createlink unlink | image | insertcode toggleview",
                                        externalCSS:MEDIA_URL + "css/jaxerRTE.css"
                                        });
                                        MooEditable.Actions.p = {
                                            title:'Paragragh',
                                            type:'button',
                                            options: {
                                                states: {
                                                    tags: ['p']
                                                },
                                                mode:'icon'
                                            },
                                            command: function(name){
                                                var argument = '<' + name.name + '>';
                                                this.focus();
                                                this.execute('formatBlock', false, argument);
                                            }
                                        };
                                        MooEditable.Actions.h2 = {
                                            title:'H2',
                                            type:'button',
                                            options:{
                                                mode:'icon'
                                            },
                                            command: function(name){
                                                var argument = '<' + name.name + '>';
                                                this.focus();
                                                this.execute('formatBlock', false, argument);
                                            }
                                        };
                        
                                        MooEditable.Actions.h4 = {
                                            title: 'H4',
                                            type: 'button',
                                            options: {
                                                mode: 'icon'
                                            },
                                            command: function(name){
                                                var argument = '<' + name.name + '>';
                                                this.focus();
                                                this.execute('formatBlock', false, argument);
                                            }
                                        };
                                        MooEditable.Actions.insertcode={
                                            title:"Insert Code",
                                            type:"button",
                                            options:{
                                                mode:'icon',
                                                shotcut:'q'
                                            },
                                            states:{
                                                tags:['pre']
                                            },
                                            command:function(button, e){
                                                var codeBox, form, control, submit_btn, wrap, result_obj, node;
                                                result_obj = {};
                                                codeBox = new utils.LaunchPad();
                                                form = new Request.HTML({
                                                    evalScripts: false,
                                                    url:'/core/editor/insert/code/',
                                                    'onFailure': function () {
                                                        codeBox.showBox({
                                                            titleBar:"Insert Code",
                                                            stage:'Problem retriving the insert code form<br />Let someone know!',
                                                            closeable:true
                                                        });
                                                        
                                                    },
                                                    'onSuccess': function (responseTree, responseElements, responseHTML) {
                                                        codeBox.showBox({
                                                            titleBar:"Insert Code",
                                                            stage:'',
                                                            closeable:false
                                                        });
                                                        var fset = new Element('fieldset');
                                                        fset.inject('stage');    
                                                        fset.set('html', responseHTML);
                                                        control = new Element('li');
                                                        wrap = new Element('span').addClass('button_wrap');
                                                        submit_btn = new Element('a', {
                                                            href: "#",
                                                            text: "Insert Code",
                                                            events: {
                                                                click: function () {
                                                                    var raw_code, safe_code;
                                                                    raw_code = $('id_code').value;
                                                                    safe_code = raw_code;
                                                                    
                                                                    safe_code = safe_code.replace(/</g,'&lt;')
                                                                    safe_code = safe_code.replace(">", "&gt;");
                                                                    safe_code = safe_code.replace("<", "\&lt;");
                                                                    //safe_code = safe_code.replace("&amp;lt", "&lt;")
                                                                    result_obj = {
                                                                        language:$('id_language').value,
                                                                        syntax: safe_code
                                                                    }
                                                                    if (safe_code !== "") {
                                                                        node = "<pre class='"+ result_obj.language+":twilight'>"+result_obj.syntax+"</pre>";                                    
                                                                        em.insert(node);                                                
                                                                    }
                                                                    codeBox.hideBox();
                                                                    result_obj = raw_code = safe_code = '';
                                                                }
                                                            }
                                                        }).addClass('dark_button');
                                                        submit_btn.inject(wrap);
                                                        wrap.inject(control);
                                                        control.inject(fset);
                                                        codeBox.show();
                                                    }
                                                }).send();
                                            }
                                        };                                    
                                    });
                            </script> ''') % ( settings.MEDIA_URL, name )
