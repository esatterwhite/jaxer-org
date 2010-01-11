/**
 * @author Eric Satterwhite
 *     - esatterwhite@wi.rr.com
 *     -webmaster@muskegohitmen.com
 *     
 */
var utils = {};
utils.toggleOnOff = function(el_is_on, el_is_off){
    if (el_is_on && el_is_off) {
        el_is_on.addClass('dn');
        el_is_off.removeClass('dn');
    }
    else 
        if (el_is_on && el_is_off === undefined) {
            el_is_on.toggleClass('dn');
        }
        else {
            return false;
        }
};
utils.Overlay = new Class({
    Implements: [Options, Events, Chain],
    options: {
        isMaskOn: false,
        loadClass: 'loader',
        closeable: true,
        _closeable: null, //object constant set at creation time. aims to 'remember' 
        //the option from creation time. exposed to client for use
        color: '#000',
        opacity: 0.6,
        onReveal: $empty,
        onHide: $empty,
        onWait: $empty
    },
    initialize: function(options){
        this.setOptions(options);
        this.options._closeable = this.options.closeable || null;
        var overlay = new Element('div', {
            'id': 'mask',
            styles: {
                'width': '100%',
                'height': $(document.body).getScrollSize().y,
                'background-color': this.options.color,
                'visibility': 'hidden',
                'position': 'absolute',
                'opacity': 0,
                'z-index': 500
            }
        });
        overlay.injectTop(document.body);
        overlay.addEvent('click', function(e){
            this.options.closeable ? this.hide() : false;
        }
.bind(this));
        
    },
    reveal: function(){
        if (!this.options.isMaskOn) {
            this.options.isMaskOn = true;
            $('mask').fade(this.options.opacity);
            this.fireEvent('reveal');
        }
    },
    hide: function(){
        var m = $('mask');
        if (this.options.isMaskOn) {
            m.fade('out');
        }
        this.options.isMaskOn = false;
        this.options.closeable = this.options._closeable;
        m.empty();
        m = null;
        this.fireEvent('hide');
    },
    wait: function(){
        /*
         * The wait function assumes that you do not want the client
         * to close the overlay and changes the closeable seting to
         * false automatically. The setting will be reverted to the
         * way it was set in the constructor when the hide() function
         * is called.
         */
        /**
         * @TODO:  change html property to the loader class or image for visual feedback
         */
        var dim, yScroll, pad, mask;
        
        this.options.closeable = false;
        dim = getScrollSize();
        //check for fuggin IE people...
        yScroll = self.pageYOffset ? self.pageYOffset : document.documentElement.scrollTop;
        pad = new Element('div', {
            id: 'tmp',
            html: '',// place holder for debug
            styles: {
                position: 'absolute',
                top: yScroll + dim.y / 3, //the users eys tend to reside about 1/3 of the way down.
                left: dim.x / 2
            }
        });
        pad.setStyle('top', yScroll + dim.y / 3);
        mask = $('mask');
        mask.addClass(this.options.loadClass || '');
        lpad.inject(ask);
        this.reveal();
        this.fireEvent('onWait');
    },
    kill: function(){
        $('mask').dispose();
    }
});

utils.LaunchPad = new Class({
    /*
     * Used to display modal windows/'pop-ups'
     * This is an extension of the general utils.Overlay class.
     * You can pass in all of the same options to customize the
     * functionaliy of the overlay as well as the modalbox.
     *
     * Creating a new ModalBox creates & controls a new Overlay.
     */
    Implements: [Options, Events],
    Extends: utils.Overlay,
    options: {
        closeable: false,
        modalBox: null, // element to inject into the 
        title: null,
        stage: null,
        titleBar: null,
        className: null,
        isMaskOn: false,
        onBoxopen: $empty,
        onBoxclose: $empty
    
    },
    initialize: function(options){
        this.setOptions(options);
        this.parent(options);
    },
    build: function(){
        var m, dim, yscroll, box, titleBar, closebutton, stagewrap, stagecontainer, stage;
        m = $('mask');
        dim = getScrollSize();
        //check for fuggin IE people...
        yScroll = self.pageYOffset ? self.pageYOffset : document.documentElement.scrollTop;
        //primary container	
        box = new Element('div', {
            id: 'modalBox',
            styles: {
                position: 'absolute',
                top: yScroll + 50, //the users eys tend to reside about 1/3 of the way down.
                padding: '5px',
                background: '#FF000',
                'z-index': 700,
                opacity: 0
            },
            events: {
                click: function(e){
                    if (this.options.closeable) {
                        this.hide();
                        this.hideBox();
                    }
                }
.bind(this)
            }
        
        });
        titleBar = new Element('h2', {
            html: this.options.titleBar || ''
        }).injectTop(box);
        titleBar.addClass('draggable');
        stagewrap = new Element('div', {
            id: "stagewrap"
        }).inject(box);
        stagecontainer = new Element('div', {
            id: 'stagecontainer'
        }).inject(stagewrap);
        stage = new Element('div', {
            id: 'stage'
        }).inject(stagecontainer);
        //inject everything into the 'box'
        
        // set the stage contents and save to object
        stage.set('html', this.options.stage || '');
        
        this.setOptions({
            stage: stage,
            titleBar: titleBar,
            modalBox: box,
            closebutton: closebutton
        });
        box.inject(document.body);
        box.setStyle('left', (dim.x / 2) - (box.getSize().x / 2));
        new Drag(box, {
            handle: titleBar
        });
    },
    showBox: function(options){
        if (options) {
            this.setOptions(options);
        }
        this.build();
        this.reveal();
        this.options.modalBox.fade('in');
    },
    hideBox: function(){
        this.options.modalBox.fade('out');
        this.hide();
        this.options.modalBox.dispose();
        this.kill.delay(1500);
    },
    show: function(){
        this.options.modalBox.fade('in');
    }
});

utils.TabToggler = new Class({

    /* 
     * NO AJAX - STRAIGHT DOM MANIPULATION
     *
     * DOM structurs should be a DIV with a collection of a tags who id
     * is in the format of tab-something, tab-somethingelse, tab-somethingmore
     * and apply or remove the class .on to the a tag.
     *
     * When clicked, it will toggle a class .dn(display: none) on a corresponding
     * div with ids of container-something, container-somethingelse, container-somethingmore
     */
    initialize: function(){
        $$('div a[id^="tab-"]').each(function(tab){
            tab.addEvent('click', function(e){
                this.tabClick(tab);
            }
.bind(this));
        }
.bind(this));
    },
    tabShow: function(currentTab, shouldShow){
        if (shouldShow === true) {
            currentTab.addClass('on');
            $("container-" + currentTab.id.split('-')[1]).removeClass('dn');
        }
        else {
            currentTab.removeClass('on');
            $("container-" + currentTab.id.split('-')[1]).addClass('dn');
        }
    },
    getAllTabs: function(tab){
        var tabParent, tabs;
        tabParent = tab.parentNode.tagName;
        if (tabParent === "DIV") {
            tabs = tab.parentNode.getElementsByTagName('a');
            return tabs;
        }
        tabParent = tabParent.parentNode;
        return;
    },
    tabClick: function(tab){
        var tabs = this.getAllTabs(tab);
        $each(tabs, function(id, index){
            this.tabShow(tabs[index], false);
        }
.bind(this));
        this.tabShow(tab, true);
    },
    getTabcontentID: function(tabID){
        return tabID.split('-')[1];
    }
});

utils.AjaxTabToggler = new Class({
    /*
     *  Finds <a> tags inside a <div> whose ID starts with 'ajaxtab-'
     *  The <a>'s href should be the url which will fetch the data
     *  link's view funtion should check for xhr and redirct to a page ( error )
     *        to provide feedback and not just do nothing
     *  @Stop link propigation
     *  @fetch the data
     *  @Store Results on tab
     *  @
     */
    Implements: [Events, Options, utils.TabToggler],
    //	Extends:HitmenTabToggler,
    options: {
        tabs: [], // Holder for the DOM Elements so we don't have to traverse the DOM on every click.
        container: 'stats-container' //a DOM element where the results will be placed
    },
    initialize: function(){
        var t = $$('div a[id^="ajaxtab-"]');
        this.setOptions({
            tabs: t
        });
        this.options.tabs.each(function(tab){
            tab.addEvent('click', function(e){
                var anE = e.stop();
                this.tabClick(tab);
            }.bind(this));
        }.bind(this));
        this.tabShow(this.options.tabs[0], true);
        this.tabClick(this.options.tabs[0]);
    },
    tabShow: function(currentTab, shouldShow){
        if (shouldShow === true) {
            currentTab.addClass('on');
        }
        else {
            currentTab.removeClass('on');
        }
    },
    getAllTabs: function(tab){
        var tabParent = tab.parentNode.tagName;
        if (tabParent == "DIV") {
            var tabs = tab.parentNode.getElementsByTagName('a');
            return tabs;
        }
        tabParent = tabParent.parentNode;
        return false;
    },
    tabClick: function(tab){
        /*
         * results of the ajax call can be stored in the tab so we dont' need
         * to re run the call on every time some click happy fool goes crazy with
         * the mouse
         *
         * http://mootools.net/blog/2008/01/22/whats-new-in-12-element-storage/
         */
        this.options.tabs.each(function(el){
            el.removeClass('on');
        });
        tab.addClass('on');
        var url = tab.href;
        
        // Proxy to the element which holds the data so we don't have to traverese the DOM so much.
        var tContainer = $(this.options.container);
        tContainer.empty();
        
        if (tab.retrieve('content') !== null) {
            // if the tab has content - get it and load it into the container
            tContainer.setProperty('html', tab.retrieve('content'));
        }
        else {
            // if the tab doesn't have any content, get it from the DB and load the results.
            var rhtml = new Request.HTML({
                'method': 'get',
                'url': url,
                'onRequest': function(){
                    var cel = new Element('center');
                    var loader = new Element('img', {
                        'src': 'http://media.muskegohitmen.com/css/img/ajax-loader.gif'
                    });
                    loader.inject(cel);
                    cel.inject(tContainer);
                },
                'onSuccess': function(Tree, Elements, HTML, JavaScript){
                    tContainer.empty();
                    //tContainer.setProperty('html', HTML);
                    tContainer.adopt(Elements);
                    tab.store('content', tContainer.getProperty('html'));
                    
                },
                'onFailure': function(xhrresp){
                    //	console.log('fail');
                }
            }).send();
            
            //tab.store('content')
        }
        /*
         var tabs = this.getAllTabs(tab);
         $each(tabs, function(id, index){
         this.tabShow(tabs[index], false)
         }.bind(this));
         this.tabShow(tab, true)
         */
    },
    getTabcontentID: function(tabID){
        return tabID.split('-')[1];
    }
});

//Namespace for common ui controlling classes
var UI = {};
UI.EditMode = new Class({
    Implements: [Options, Events],
    options: {
        isEditModeOn: false,
        editorScriptsLoaded: false,
        warningBlock: null,
        MEDIA_URL: 'http://media.jaxer.org/',
        formURL: null, //the url to retrive the editing form from
        editor_element: 'id_content', // the id of the textarea we are going to convert to the editor
        editorActions: "h2 h4 p | bold italic | insertunorderedlist indent outdent | undo redo | createlink urlsearch unlink | image | insertcode toggleview",
        wikiArea: 'js-wiki-',
        _RTE: null
    },
    initialize: function(options){
        if (options !== undefined) {
            this.setOptions(options);
        }
        this.build();
        
    },
    build: function(){
        var block, close_btn, title;
        block = new Element('div', {
            id: 'warningBlock',
            styles: {
                background: '#b30000',
                padding: '10px 0px',
                position: 'fixed',
                bottom: '0',
                'z-index': 10000,
                opacity: 0,
                visibility: 'hidden'
            }
        }).addClass('width100').inject(document.body);
        title = new Element('h1', {
            'text': "Edit Mode",
            styles: {
                'margin-right': '20px',
                'color': '#000'
            }
        });
        title.addClass('fr');
        close_btn = new Element('a', {
            'class': 'dark_button',
            text: 'cancel!',
            events: {
                'click': function(evt){
                    //console.log('click');
                    this.confirmExit();
                }.bind(this)
            }
        }).addClass('fr mt-8 mr-10').inject(block);
        
        title.inject(block);
        this.setOptions({
            warningBlock: block
        });
    },
    confirmExit: function(){
        if (confirm("Are you sure you want to exit with out saving??")) {
            this.options.warningBlock.fade('out');
            this.turnOff.delay(800, this);
        }
    },
    turnOn: function(){
        if (!this.options.isEditModeOn) {
            this.setOptions({
                isEditModeOn: true
            });
            this.options.warningBlock.fade('in');
        }
        else {
            return false;
        }
    },
    turnOff: function(){
        if (this.options.isEditModeOn) {
            this.setOptions({
                isEditModeOn: false
            });
            
            window.location.reload();
        }
        else {
            return false;
        }
    },
    buildEditor: function(){
        if (!this.options.isEditModeOn) {
            this.turnOn();
        }
        else {
            return false;
        }
        var send_btn, form_wrap, form, moo, form_set, controls;
        
        form = new Element('form', {
            method: 'post',
            action: this.options.formURL,
            id: 'document_form'
        });
        form_set = new Element('fieldset', {}).inject(form);
        form_wrap = new Element('ul').inject(form_set);
        if (this.options.form_url === null) {
            return false;
        }
        
        new Request.HTML({
            method: 'get',
            url: this.options.formURL,
            onFailure: function(){
            
            },
            onSuccess: function(rTree, rEls, rHTML, rScripts){
                var wikiContainer;
                wikiContainer = $$('div[id^={wikiArea}]'.substitute(this.options))[0];
                wikiContainer.empty();
                wikiContainer.adopt(form);
                form_wrap.set('html', rHTML);
                moo = $(this.options.editor_element).mooEditable({
                    externalCSS: "{MEDIA_URL}css/jaxerRTE.css".substitute(this.options),
                    actions: this.options.editorActions
                });
                this.options._RTE = moo;
            }.bind(this)
        }).send();
        
        controls = new Element('li').inject(form_set, 'bottom');
        send_btn = new Element('a', {
            text: "submit",
            href: "#",
            'class': 'dark_button p_all-6',
            events: {
                'click': function(evt){
                    this.options._RTE.saveContent();
                    form.submit();
                    //					new Request.JSON({
                    //						method:'post',
                    //						url:this.options.formURL,
                    //						onFailure:function(){},
                    //						onSuccess:function(json){
                    //							console.log(this)
                    //						}
                    //					}).send()	
                }.bind(this)
            }
        }).inject(controls);
        
    },
    insert: function(content){
        this.options._RTE.selection.insertContent(content);
    }
});
UI.ScollPanel = new Class({
    Implements: [Options, Events],
    options: {
        scrollPanel: 'scroll-panel',
        controlContainer: 'controls',
        buttonElement: 'li',
        controls: [],
        offset: 245,
        onSlide: $empty,
        onComplete: $empty
    },
    /**
     *
     * @param {Object} options
     */
    initialize: function(options){
        this.setOptions(options);
        //revieve and store the button elements
        this.options.controls = $$("#".concat(this.options.controlContainer, " ", this.options.buttonElement));
        this.options.controls.each(function(el){
            el.addEvent('click', function(e){
                var multiplier, moveTo, panel;
                this.buttonClick(el);
                //we want the first control mapped to 0
                multiplier = el.id.split('-')[1] - 1;
                panel = $(this.options.scrollPanel);
                moveTo = this.options.offset * multiplier;
                this.fireEvent('slide', "Sliding", 100);
                panel.tween('left', -moveTo);
                this.fireEvent('complete');
            }
.bind(this));
        }
.bind(this));
        
    },
    /**
     *
     * @param {HTML Element} button:  this is a reference to the button element that was clicked
     *
     */
    buttonClick: function(button){
        if (!button.hasClass('on')) {
            this.options.controls.removeClass('on');
            button.addClass('on');
        }
    }
});
/**
 * @classDescription: The ContentRevealer class's intended use is to hide additional object
 * 					  properties until the user wishes to see them.
 *
 *
 * @property{String} controller: 	the ID of controlling element used for interaction, words seperated
 * 					 				by a common seperator where the final word/number is a unique identifier
 *
 * @property{String} element: 		the ID of the corresponding element that will be hidden from veiw
 * 					 				The id should have the same prefix as the controller element's ID and end with
 *  				 				the same unique identifier.
 *  								Controller: 'js-reveal-control-1' Element:'js-reveal-content-'
 *
 *  								The class will look for an element whose id is the concatenation of
 *  				 				the element property followed by the unique idenifier of the controller.
 *
 *					  				controller = 'js-reveal-control-1'
 *  								element = 'my-content-
 *
 *					  				class finds 'my-content-1'
 *
 *  @property{String} splitter:  	the common seperator used to split the ID names of elements.
 *
 *  @property{String} container:	the DOM node type where the content lives defaults to 'div'
 *  @property{String} selector :	the class name used by the class to collect DOM nodes to hide
 *  								 defaults to '.slide'
 *
 *  								The class will join the container and selector to find all of the
 *  								you wish to controll
 *
 *  								the default would be 'div.slide'
 */
UI.ContentRevealer = new Class({
    Implements: [Events, Options, Chain],
    
    options: {
        controller: '',
        element: 'js-reveal-content-',
        _elements: [], // reverence to the collection of elements we are sliding to prevent repeated DOM traversal
        _controlers: [],
        container: 'div',
        selector: '.slide',
        splitter: '-',
        isClosed: false,
        onOpen: $empty,
        onClose: $empty,
        onOpenAll: $empty,
        onCloseAll: $empty
    },
    /**
     *
     * @param {String} The common prefix of the IDs of the elements used
     * 					as the button to interact
     * 					with the revealable content elements
     * 					   EX. if all of your button elements are named:
     * 							myButton-1
     * 							myButton-2
     * 							myButton-3
     *
     * 						You would pass myButton
     * 						with '-' for the options splitter
     *
     * 					The class will look for elements using IDs from the option element
     * 					with
     *
     * @param {Object} The setting options for this class
     */
    initialize: function(control, options){
        if (options) {
            this.setOptions(options);
        }
        this.options.controller = control;
        
        this.options._elements = $$(this.options.container + this.options.selector);
        this.options._elements.each(function(el){
            el.set('slide', {
                duration: 'long',
                transition: 'quad:out'
            });
            el.slide('hide');
            this.setOptions({
                isClosed: true
            });
        }.bind(this));
        this.options._controllers = $$('span[id^=' + this.options.controller + "]");
        this.options._controllers.each(function(el){
            el.addEvent('click', function(){
                var elementToToggle = $(this.options.element.concat(el.id.split(this.options.splitter).getLast()));
                this.toggle(elementToToggle);
            }.bind(this));   
        }.bind(this));
        
        //attach events to controller
    
    },
    toggle: function(el){
        if (!this.options.isClosed) {
            this.setOptions({
                isClosed: true
            });
            el.slide('out');
            this.fireEvent('close', el);
        }
        else {
            el.slide('in');
            this.setOptions({
                isClosed: false
            });
            this.fireEvent('open', el);
        }
    },
    openAll: function(){
        this.options._elements.each(function(el){
            el.slide('in');
            this.fireEvent('open', el);
        });
        this.options.isClosed = false;
        this.fireEvent('openall', this.options._elements);
    },
    closeAll: function(){
        this.options._elements.each(function(el){
            el.slide('out');
            this.fireEvent('close', el);
        });
        this.options.isClosed = true;
        this.fireEvent('closeall', this.options._elements);
    }
});
UI.JaxerAutoCompleter = new Class({
	Extends:Autocompleter.Request.JSON,
	Implements:[Options, Events],
	options:{
		onPick:$empty,
		elementID:null,
		_element:null,
		fxOptions:null,
		postVar:'q',
		url:null,
		method:'POST'
	},
	initialize:function(elementID, postURL, options){
		if(options){
			this.setOptions(options);
		}
		this.options.elementID = elementID;
		this.options.url = postURL;
		this.options_element = $('elementID');
		
		this.parent(elementID, postURL, this.options);
	},
	choiceSelect: function(choice) {
		if (choice) this.choiceOver(choice);
		//this.setSelection(true);
		this.queryValue = false;
		this.hideChoices();	
		this.fireEvent('pick', choice.retrieve('url'));	
	}
	
});
/**
 * MultiLineAutoComplete is an extension of Autocompleter.Request.JSON
 * It is a replication of the face book textbox / search bar
 * 
 *  The class replaces an input element with a div element which acts
 * contatins a transparent input box which serves as the autocompleter input
 * 
 * the selections are stored as selected options and the user is able to delete
 * options. 
 * 
 * The primary design purpose is for sending PM's to multiple users at once.
 *
 */
UI.MultiLineAutoComplete = new Class({
	Extends:Autocompleter.Request.JSON,
	Impliments:[Options, Events, Class.Occlude],
	options:{
		onRemove:$empty,
		onInsert:$empty,
		searchInput:null,
		mainInput:null,
		replaceInput:true,
		replaceID:'id_recipient', // the id of the input element we are taking out of the DOM and replacing with the autocomplete
		searchFieldID:'id_search', // the id of an input element we are going to use for the autocompleter
		formID:'messageForm',
		optionClass:'selectbox-option',
		closeLinkClass:'small red',
		closeLinkHref:'#',
		highlightColor:'#EF0E0E',
		_inputdata:null,
		//autocompleter options
		tokens:null,
		postVar:'q',
		url:null,
		method:'POST'
		
	},
	initialize:function(options){
		if (options) {
			this.setOptions(options);
		}
		this.options.mainInput = $(this.options.searchFieldID);	
		this.options._inputdata= $(this.options.replaceID)
		this.options._inputdata.setProperty('type', 'hidden');
		this.parent(this.options.searchFieldID, this.options.url, this.options);
		var container = new Element('div',{
			'class':'multi-input'
		}).inject(this.options._inputdata,'before').adopt(this.options.mainInput);
		this.options.mainInput.focus();
		new Element('br',{
			'class':'clearfloat'
		}).inject(container,'bottom');
		
	},
	
	choiceSelect: function(choice) {
		if (choice) this.choiceOver(choice);
		this.setSelection(true);
		this.queryValue = false;
		this.hideChoices();
		// if we can't find a similar element in the list
		// make the new element and add to list
		if (!this.checkOptions({obj_id:choice.retrieve('obj_id')})) {
			var opt = new Element('li', {
				html: choice.get('text'),
				'class':'multiline '+ this.options.optionClass,
				events:{
					mouseover:function(e){
						//clean up and mess from the .highlight() method
						e.target.removeProperty('style');
					}
				}
			});
			new Element('a',{
				text:' (x)',
				'class':this.options.closeLinkClass,
				href:"#",
				events:{
					'click':function(e){
						e.target.getParent('li').dispose();
						this.options.mainInput.focus();
						this.fireEvent('remove');
					}.bind(this)
				}
			}).inject(opt);
			new Element('input',{
				type:'hidden',
				id:'data-'+choice.retrieve('obj_id')
			}).setProperties({
				'content_type':choice.retrieve('ct'),
				'obj_id':choice.retrieve('obj_id'),
				'value':choice.get('text')
				}).inject(opt);
			opt.inject(this.options.mainInput, 'before');
			this.fireEvent('insert', opt);
		}
		//if we did find a similar element we don't do anything
		this.options.mainInput.value='';
	},
	checkOptions:function(opts){
		var options = $$('input[obj_id={obj_id}]'.substitute(opts)).getParent();
		if(options.length > 0){
			options[0].highlight(this.options.highlightColor);
			return true;
		}else{
			return false;
		}				 
	},
	setData:function(){
		data = $$('input[id^=data-]');
		var x = [];
		data.each(function(el){
			x.push(el.value);
		});
		this.options._inputdata.value = x.toString();
		x = null;
	}			
});
window.addEvent('domready', function(){
	new MenuMatic({
		id:"mainnav",
		physics: Fx.Transitions.Circ.easeOut,
		opacity: 90
	});
    var tips = new Tips('.tooltips', {
        className: 'bg-nearblack p_all-6 rounded w-200',
        offset: {
            'x': 40,
            'y': -20
        },
        styles: {
            opacity: 0.6
        }
    });
    tips.addEvent('show', function(tips, el){
        tips.fade('in');
    });
    try {
        $("js-objectsearch-link").addEvent('click', function(evt){
            evt.stop();
            var param = "js-" + evt.target.id.split('-')[1] + "-container";
            $(param).removeClass('dn');
            new OverText('object_search', {
                positionOptions: 'padding-left:30px'
            });
            new Autocompleter.Request.JSON('object_search', '/search/', {
                'minLength': 1,
                'selectMode': 'type-ahead',
                'postVar': 'searchVal',
                'tokens': null,
                'filterSubset': true,
                'injectChoice': function(token){
                    var choice = new Element('li');
                    new Element('div', {
                        'html': this.markQueryValue(token.name)
                    }).inject(choice);
                    new Element('span', {
                        'html': token.ct,
                        'class': 'small fl'
                    }).inject(choice);
                    new Element('span', {
                        'html': "<span class='{client}'>client</span>|<span class='{server}'>sever</span>".substitute(token),
                        'class': 'fr compact-text'
                    }).inject(choice);
                    new Element('br', {
                        'class': 'clearfloat'
                    }).inject(choice);
                    new Element('span', {
                        id: '',
                        'class': 'dn',
                        text: token.url,
                        ct_id: token.ct_id
                    }).inject(choice);
                    choice.addEvent('click', function(evt){
                        //console.log(token.url);
                        window.location.href = token.url;
                    });
                    this.addChoiceEvents(choice).inject(this.choices);
                }              
            });
        });
    } 
    catch (e) {
        Log.log(e);
    }
});
