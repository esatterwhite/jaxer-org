/**
 * @author Eric
 */
var utils = {};
utils.Overlay = new Class({
	Implements: [Options, Events, Chain],
	options: {
		isMaskOn: false,
		loadClass: 'loader',
		closeable: true,
		_closeable: null, //object constant set at creation time. aims to 'remember' the option from creation time. exposed to client for use
		color: '#000',
		opacity: 0.6,
		onReveal: $empty,
		onHide: $empty,
		onWait: $empty
	},
	initialize: function (options) {
		this.setOptions(options);
		this.options._closeable = this.options.closeable || null;
		var overlay = new Element('div', {
			'id': 'mask',
			styles: {
	            'width':  '100%',
				'height':  $(document.body).getScrollSize().y,
				'background-color': this.options.color,
				'visibility': 'hidden',
				'position': 'absolute',
				'opacity': 0,
				'z-index': 500
			}
		});
		overlay.injectTop(document.body);		
		overlay.addEvent('click', function (e) {
			this.options.closeable ? this.hide(): false;	
		}.bind(this));

	},
	reveal: function () {
		if (!this.options.isMaskOn) {
			this.options.isMaskOn = true;
			$('mask').fade(this.options.opacity);
			this.fireEvent('reveal');
		}
	},
	hide: function () {
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
	wait: function () {
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
		var dim, yScroll, l, m;
		
		this.options.closeable = false;
		dim = getScrollSize();
		//check for fuggin IE people...
		yScroll = self.pageYOffset ? self.pageYOffset: document.documentElement.scrollTop;
		l = new Element('div', {
		    id: 'tmp',
			html: '<div style="background-color: #fff;">Hello World</div>',// place holder for debug
		    styles: {
		        position: 'absolute',
		        top: yScroll + dim.y / 3, //the users eys tend to reside about 1/3 of the way down.
		        left: dim.x / 2
		    }		    
		});
		l.setStyle('top', yScroll + dim.y / 3);
		m = $('mask');
		m.addClass(this.options.loadClass || '');
		l.inject(m);
		this.reveal();
		this.fireEvent('onWait');
	},
	kill: function () {
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
	initialize: function (options) {
		this.setOptions(options);
		this.parent(options);
	},
	build: function () {
		var m, dim, yscroll, box, titleBar, closebutton, stagewrap, stagecontainer, stage;
		m = $('mask');
		dim = getScrollSize();
		//check for fuggin IE people...
		yScroll = self.pageYOffset ? self.pageYOffset: document.documentElement.scrollTop;
		//primary container	
		box = new Element('div', {
			id: 'modalBox',
			styles: {
		        position: 'absolute',
		        top: yScroll + dim.y / 3, //the users eys tend to reside about 1/3 of the way down.
				padding: '5px',
				background: '#FF000',
				'z-index': 700,
				opacity: 0
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
			handle:titleBar
		});
	},
	showBox: function (options) {
		if (options) {
			this.setOptions(options);
		}
		this.build();
		this.reveal();	
		this.options.modalBox.fade('in');
	},
	hideBox: function () {
		this.options.modalBox.fade('out');
		this.hide();
		this.options.modalBox.dispose();
	},
	show: function () {
		this.optionx.modalBox.fade('in');
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
	
    initialize:  function () {
        $$('div a[id^="tab-"]').each(function (tab) {
            tab.addEvent('click',
            function (e) {
                this.tabClick(tab);
            }.bind(this));
        }.bind(this));
    },
    tabShow:  function (currentTab, shouldShow) {
        if (shouldShow === true) {
            currentTab.addClass('on');
            $("container-" + currentTab.id.split('-')[1]).removeClass('dn');
        } else {
            currentTab.removeClass('on');
            $("container-" + currentTab.id.split('-')[1]).addClass('dn');
        }
    },
    getAllTabs:  function (tab) {
		var tabParent, tabs;
        tabParent = tab.parentNode.tagName;
        if (tabParent === "DIV") {
            tabs = tab.parentNode.getElementsByTagName('a');
            return tabs;
        }
        tabParent = tabParent.parentNode;
        return;
    },
    tabClick:  function (tab) {
        var tabs = this.getAllTabs(tab);
        $each(tabs,
        function (id, index) {
            this.tabShow(tabs[index], false);
        }.bind(this));
        this.tabShow(tab, true);
    },
    getTabcontentID:  function (tabID) {
        return tabID.split('-')[1];
    }
});

utils.AjaxTabToggler = new Class({});

//Namespace for common ui controlling classes
var UI = {};
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
	initialize: function (options) {
		this.setOptions(options);
		//revieve and store the button elements
		this.options.controls = $$("#".concat(this.options.controlContainer, " ", this.options.buttonElement));
		this.options.controls.each(function (el) {
				el.addEvent('click', function (e) {
					var multiplier, moveTo, panel;
					this.buttonClick(el);
					//we want the first control mapped to 0
					multiplier = el.id.split('-')[1] - 1;
					panel = $(this.options.scrollPanel);
					moveTo = this.options.offset * multiplier;
					this.fireEvent('slide', "Sliding", 100);
					panel.tween('left', -moveTo);
					this.fireEvent('complete');
				}.bind(this));
			}.bind(this)
		);
			
	},
	/**
	 * 
	 * @param {HTML Element} button:  this is a reference to the button element that was clicked
	 * 
	 */
	buttonClick: function (button) {		
		if (!button.hasClass('on')) {
			this.options.controls.removeClass('on');
			button.addClass('on');		
		}
	}
});

window.addEvent('domready', function () {
	//set up code for elements found on most every page.
	
});
