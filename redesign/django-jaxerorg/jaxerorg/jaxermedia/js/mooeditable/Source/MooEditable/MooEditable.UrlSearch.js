/**
 * @author Eric
 */
MooEditable.UI.UrlsearchDialog = function(editor){
	var html = 'url <input id="url" class="dialog-url" value="" size="15"/> '
			+ '<span class="small bold">or</span> search <input type="text" id="url_search" size="15" value="" class="dialog-url"/> '	
			+ '<button class="dialog-button dialog-ok-button">OK</button> '
			+ '<button class="dialog-button dialog-cancel-button">Cancel</button> ';
	var urlsearch, urlinput, input;
	return new MooEditable.UI.Dialog(html,{
		'class':'mooeditable-prompt-dialog',
		onOpen:function(){
			input = $('url_search');
			urlinput = $('url');
			urlsearch = new UI.JaxerAutoCompleter(input,'/search/',{
				postVar:'searchVal',
				injectChoice:function(token){
					var choice = new Element('li');
					choice.store('url', token.url);
		            new Element('div', {
		                'html': this.markQueryValue(token.name),
						'class':'compact-text'
		            }).inject(choice);
					new Element('div',{
						'html':token.ct,
						'class':'small'
					}).inject(choice);
					this.addChoiceEvents(choice).inject(this.choices)
				},
				onPick:function(url){
					urlinput.value=url;
				}
			});
			Log.log("OPEN!", input);
		},
		onClose:function(e){
			urlsearch.destroy();
		},
		onClick:function(e){
			if (e.target.tagName.toLowerCase() == 'button') e.preventDefault();
			var button = document.id(e.target);
			if (button.hasClass('dialog-cancel-button')) {
				this.close();
				Log.log("cancel");
				urlinput='';
				input.value = "";
			}
			else 
				if (button.hasClass('dialog-ok-button')) {
					var urlRegex = /^(https?|ftp|rmtp|mms):\/\/(([A-Z0-9][A-Z0-9_-]*)(\.[A-Z0-9][A-Z0-9_-]*)+)(:(\d+))?\/?/i;
					var relUrlRegex = /^\/(([A-Z0-9_-]*)+)(:(\d+))?\/?/i;
					
					var text = editor.selection.getText();
					if (urlinput.value !== ""){
						var u = urlinput.value.trim();
						if (urlRegex.test(u) || relUrlRegex.test(u))
						{
							var wrap = new Element('div');
							new Element('a', {
								href:u,
								text:text
							}).inject(wrap);						
						editor.selection.insertContent(wrap.get('html'));
						this.close();
						}else{
							alert('Enter a fully qualified URL or reletive URL');
							urlinput.focus();
						}
					}
					urlinput.value="";
					input.value = "";
				}
			
		}
	});
};
MooEditable.Actions.urlsearch={
	title:'Search For Url',
	type:'button',
	options:{
		mode:'icon',
		shortcut:'l'
	},
	dialogs:{
		alert: MooEditable.UI.AlertDialog.pass('Please select the text you wish to hyperlink.'),
		prompt:function(editor){
			return MooEditable.UI.UrlsearchDialog(editor);
		}
	},
	command:function(){
		if (this.selection.isCollapsed()) {
			this.dialogs.createlink.alert.open();
		}
		else {
			this.dialogs.urlsearch.prompt.open();
		}
	}
	
};
