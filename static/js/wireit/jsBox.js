/**
 * Update wireit json dragable objects with available services in /modules/

 var value = ''
 getModulesAjax()

 function getModulesAjax() {

 $.get("/applications/getmodules/", function(data){
 obj = JSON.parse(data)
 value = obj
 });

 //return obj
 };

 function setValues(data){
 obj = JSON.parse(data)
 value = obj
 window.alert(value)
 };

 function getValue(){
 return value
 };
 */

function runApp(values) {
	project_id = $('#project_id').val()
	$.post("/applications/run/" + project_id + "/", {
		params : values
	}, function(data) {
		if ((data['error'] != '') && (data['error'] != null)) {
			output = "<p>" + data['error'] + "</p>"
			$('#output').html(output)
		} else {
			objJSON = $.parseJSON(data)
			output = ''

			for (var i = 0, len = objJSON.length; i < len; ++i) {
				var element = objJSON[i];
				output += "<p>Module:" + element.module + "</p>"
				response = "<table>"
				for (var k in element.response) {
					if ( {}.hasOwnProperty.call(element.response, k)) {
						
						if (element.response[k] instanceof Object){
							response += "<tr><td><b>" + k + "</b> : </td></tr>"
							for (key in element.response[k]){
								
								response += "<tr><td> " + key + "</td><td>"+ element.response[k][key] +"</td></tr>"
							}
						} else {
							response += "<tr><td><b>" + k + "</b> | </td>"
							response += "<td> " + element.response[k] + "</td></tr>"
						}
						//response += element.response[k]['ruleid'])
						// just print bonitinho
					}
					//output += "<p>Response:</p><br /><small>"+element.response+"</small>"
				}
				response += "</table>"
				output += "<p>Response:</p>" + response +"<br />"

			}

			$('#output').html(output)
		}

	});

	//return false
};




function getModules() {
	return [{
		"name" : "Start",
		"container" : {
			"xtype" : "WireIt.ImageContainer",
			"image" : "/static/images/bpmn/images/start.png",
			"icon" : "/static/images/bpmn/icons/startevent/none.png",
			"terminals": [
				{"name": "_OUTPUT", "direction": [1,0], "offsetPosition": {"left": -9, "top": -15 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}}
			]
		}
	},{
		"name" : "Terminate",
		"container" : {
			"xtype" : "WireIt.ImageContainer",
			"image" : "/static/images/bpmn/images/terminate.png",
			"icon" : "/static/images/bpmn/icons/endevent/terminate.png",
			"terminals": [
				{"name": "_INPUT", "direction": [-1,0], "offsetPosition": {"left": -40, "top": -15 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}
				}
		  ]
	}
	}, {
		"name" : "Firewall-Control",
		"service_id" : "2",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "WireIt.FormContainer demo",
			"icon" : "/static/images/icons/firewall-s.png",
			"collapsible" : true,
			"fields" : [{
				"type" : "select",
				"inputParams" : { "label" : "Action",	"name" : "title",
					"selectValues" : ["Enable", "Disable", "Status", "storageRules", "subnet-mask"]
				}
			}],
			"terminals": [
			{"name" : "_INPUT1",	"direction" : [-1, 0], "offsetPosition" : {"left" : -17,	"bottom" : 29 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_INPUT2",	"direction" : [0, -1], "offsetPosition" : {"left" : 52,	"bottom" : 63 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_OUTPUT1",	"direction" : [1, 0], "offsetPosition" : {"right" : -17, "bottom" : 29 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			},
			{"name" : "_OUTPUT2",	"direction" : [0, 1], "offsetPosition" : {"right" : 52, "bottom" : -7 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			}],
			"legend" : ""
		}
	}, {
		"name" : "Firewall-GetRules",
		"service_id" : "2",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "WireIt.FormContainer demo",
			"icon" : "/static/images/icons/firewall-s.png",
			"collapsible" : false,
			"fields" : [],
			"terminals": [
			{"name" : "_INPUT1",	"direction" : [-1, 0], "offsetPosition" : {"left" : -17,	"bottom" : 29 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_INPUT2",	"direction" : [0, -1], "offsetPosition" : {"left" : 52,	"bottom" : 63 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_OUTPUT1",	"direction" : [1, 0], "offsetPosition" : {"right" : -17, "bottom" : 29 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			},
			{"name" : "_OUTPUT2",	"direction" : [0, 1], "offsetPosition" : {"right" : 52, "bottom" : -7 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			}],
			"legend" : ""
		}
	}, {
		"name" : "Firewall-SetRules",
		"service_id" : "2",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "WireIt.FormContainer demo",
			"icon" : "/static/images/icons/firewall-s.png",
			"collapsible" : true,
			"fields" : [
				{	"type" : "select", "inputParams" : { "label" : "Action",	"name" : "action",
					"selectValues" : ["ALLOW", "DENY"]}},
				{ "type" : "type", "inputParams" : {"label" : "switchId", "name" : "switch_id", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input switch id"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "src-inport", "name" : "src-inport", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input src inport"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "src-mac", "name" : "src-mac", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input src MAC"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "dst-mac", "name" : "dst-mac", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input dst MAC"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "dl-type", "name" : "dl-type", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input DL type"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "src-ip", "name" : "src-ip", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input src IP"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "dst-ip", "name" : "dst-ip", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input dst IP"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "nw-proto", "name" : "nw-proto", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input NW proto"	}	}	}},
				{ "type" : "type", "inputParams" : {"label" : "Priority", "name" : "priority", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input priority"	}	}	}}
			],
			"terminals": [
			{"name" : "_INPUT1",	"direction" : [-1, 0], "offsetPosition" : {"left" : -17,	"bottom" : 29 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_INPUT2",	"direction" : [0, -1], "offsetPosition" : {"left" : 52,	"bottom" : 63 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_OUTPUT1",	"direction" : [1, 0], "offsetPosition" : {"right" : -17, "bottom" : 29 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			},
			{"name" : "_OUTPUT2",	"direction" : [0, 1], "offsetPosition" : {"right" : 52, "bottom" : -7 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			}],
			"legend" : ""
		}
	},
	{
		"name" : "Firewall-DelRules",
		"service_id" : "2",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "WireIt.FormContainer demo",
			"icon" : "/static/images/icons/firewall-s.png",
			"collapsible" : true,
			"fields" : [
				{ "type" : "type", "inputParams" : {"label" : "RuleID", "name" : "rule_id", "wirable" : false,	
				"value" : {	"type" : "string",	"inputParams" : {	"typeInvite" : "input rule id"	}	}	}},
			],
			"terminals": [
			{"name" : "_INPUT1",	"direction" : [-1, 0], "offsetPosition" : {"left" : -17,	"bottom" : 29 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_INPUT2",	"direction" : [0, -1], "offsetPosition" : {"left" : 52,	"bottom" : 63 },
				"ddConfig" : {"type" : "input", "allowedTypes" : ["output"]}},
			{"name" : "_OUTPUT1",	"direction" : [1, 0], "offsetPosition" : {"right" : -17, "bottom" : 29 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			},
			{"name" : "_OUTPUT2",	"direction" : [0, 1], "offsetPosition" : {"right" : 52, "bottom" : -7 },
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			}],
			"legend" : ""
		}
	},{
		"name" : "List-Switches",
		"container" : {
			"xtype" : "WireIt.InOutContainer",
			"icon" : "/static/res/icons/arrow_right.png",
			"inputs" : ["none"],
			"outputs" : ["harole", "dpid", "inetAddress"]
		}
	}, {
		"name" : "Twitter-create",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "input",
			"fields" : [{
				"type" : "select",
				"inputParams" : {
					"label" : "Condition",
					"name" : "title",
					"selectValues" : ["==", "!=", ">", "<", ">=", "<="]
				}
			}],
			"terminals" : [{
				"name" : "_INPUT1",	"direction" : [0, 1],	"offsetPosition" : {"left" : 25, "top" : -15}
			}, {
				"name" : "_INPUT2",	"direction" : [-1, 0], "offsetPosition" : {"right" : 25,	"top" : -15}
			}, {
				"name" : "_OUTPUT",	"direction" : [-1, 0], "offsetPosition" : {"left" : 86,"bottom" : -15},
				"ddConfig" : {"type" : "output", "allowedTypes" : ["input"]}
			}]
		}
	}, {
		"name" : "Gmail-send-email",
		"container" : {
			"xtype" : "WireIt.FormContainer",
			"title" : "Comment",
			"fields" : [{
				"type" : "text",
				"inputParams" : {
					"label" : "",
					"name" : "comment",
					"wirable" : false
				}
			}]
		},
		"value" : {
			"input" : {
				"type" : "url",
				"inputParams" : {}
			}
		}
	}]
};

/**
 * jsBox
 */
var jsBox = {

	language : {

		languageName : "ProViNet Composer",
	
		modules : getModules()
	},

	/**
	 * @method init
	 * @static
	 */
	init : function() {
		this.editor = new jsBox.WiringEditor(this.language);

		// Open the infos panel
		editor.accordionView.openPanel(2);
	},

	/**
	 * Execute the module in the "ExecutionFrame" virtual machine
	 * @method run
	 * @static
	 */
	run : function() {
		runApp(YAHOO.lang.JSON.stringify(this.editor.getValue()));
		//var ef = new ExecutionFrame(this.editor.getValue());
		//ef.run();
	}
};

/**
 * The wiring editor is overriden to add a button "RUN" to the control bar
 */
jsBox.WiringEditor = function(options) {
	jsBox.WiringEditor.superclass.constructor.call(this, options);
};

YAHOO.lang.extend(jsBox.WiringEditor, WireIt.WiringEditor, {

	/**
	 * Add the "run" button
	 */
	renderButtons : function() {
		jsBox.WiringEditor.superclass.renderButtons.call(this);

		// Add the run button
		var toolbar = YAHOO.util.Dom.get('toolbar');
		var runButton = new YAHOO.widget.Button({
			label : "Run",
			id : "WiringEditor-runButton",
			container : toolbar
		});
		runButton.on("click", jsBox.run, jsBox, true);
	},

	/**
	 * Customize the load success handler for the composed module list
	 */
	onLoadSuccess : function(wirings) {
		jsBox.WiringEditor.superclass.onLoadSuccess.call(this, wirings);

		//  Customize to display composed module in the left list
		this.updateComposedModuleList();
	},

	/**
	 * All the saved wirings are reusable modules :
	 */
	updateComposedModuleList : function() {

		// to optimize:

		// Remove all previous module with the ComposedModule class
		var l = YAHOO.util.Dom.getElementsByClassName("ComposedModule", "div", this.leftEl);
		for (var i = 0; i < l.length; i++) {
			this.leftEl.removeChild(l[i]);
		}

		if (YAHOO.lang.isArray(this.pipes)) {
			for ( i = 0; i < this.pipes.length; i++) {
				var module = this.pipes[i];
				this.pipesByName[module.name] = module;

				// Add the module to the list
				var div = WireIt.cn('div', {
					className : "WiringEditor-module ComposedModule"
				});
				div.appendChild(WireIt.cn('span', null, null, module.name));
				var ddProxy = new WireIt.ModuleProxy(div, this);
				ddProxy._module = {
					name : module.name,
					container : {
						"xtype" : "jsBox.ComposedContainer",
						"title" : module.name
					}
				};
				this.leftEl.appendChild(div);

			}
		}
	}
});

/**
 * Container class used by the "jsBox" module (automatically sets terminals depending on the number of arguments)
 * @class Container
 * @namespace jsBox
 * @constructor
 */
jsBox.Container = function(options, layer) {

	jsBox.Container.superclass.constructor.call(this, options, layer);

	this.buildTextArea(options.codeText || "function(e) {\n\n  return 0;\n}");

	this.createTerminals();

	// Reposition the terminals when the jsBox is being resized
	this.ddResize.eventResize.subscribe(function(e, args) {
		this.positionTerminals();
		YAHOO.util.Dom.setStyle(this.textarea, "height", (args[0][1] - 70) + "px");
	}, this, true);
};

YAHOO.extend(jsBox.Container, WireIt.Container, {

	/**
	 * Create the textarea for the javascript code
	 * @method buildTextArea
	 * @param {String} codeText
	 */
	buildTextArea : function(codeText) {

		this.textarea = WireIt.cn('textarea', null, {
			width : "90%",
			height : "70px",
			border : "0",
			padding : "5px"
		}, codeText);
		this.setBody(this.textarea);

		YAHOO.util.Event.addListener(this.textarea, 'change', this.createTerminals, this, true);

	},

	/**
	 * Create (and re-create) the terminals with this.nParams input terminals
	 * @method createTerminals
	 */
	createTerminals : function() {

		// Output Terminal
		if (!this.outputTerminal) {
			this.outputTerminal = this.addTerminal({
				xtype : "WireIt.util.TerminalOutput",
				"name" : "out"
			});
			this.outputTerminal.jsBox = this;
		}

		// Input terminals :
		var match = (this.textarea.value).match((/^[ ]*function[ ]*\((.*)\)[ ]*\{/));
		var sParamList = match ? match[1] : "";
		var params = sParamList.split(',');
		var nParams = (sParamList == "") ? 0 : params.length;

		var curTerminalN = this.nParams || 0;
		if (curTerminalN < nParams) {
			// add terminals
			for (var i = curTerminalN; i < nParams; i++) {
				var term = this.addTerminal({
					xtype : "WireIt.util.TerminalInput",
					"name" : "param" + i
				});
				//term.jsBox = this;
				WireIt.sn(term.el, null, {
					position : "absolute",
					top : "-15px"
				});
			}
		} else if (curTerminalN > nParams) {
			// remove terminals
			for (var i = this.terminals.length - (curTerminalN - nParams); i < this.terminals.length; i++) {
				this.terminals[i].remove();
				this.terminals[i] = null;
			}
			this.terminals = WireIt.compact(this.terminals);
		}
		this.nParams = nParams;

		this.positionTerminals();

		// Declare the new terminals to the drag'n drop handler (so the wires are moved around with the container)
		this.dd.setTerminals(this.terminals);
	},

	/**
	 * Reposition the terminals
	 * @method positionTerminals
	 */
	positionTerminals : function() {
		var width = WireIt.getIntStyle(this.el, "width");

		var inputsIntervall = Math.floor(width / (this.nParams + 1));

		for (var i = 1; i < this.terminals.length; i++) {
			var term = this.terminals[i];
			YAHOO.util.Dom.setStyle(term.el, "left", (inputsIntervall * (i)) - 15 + "px");
			for (var j = 0; j < term.wires.length; j++) {
				term.wires[j].redraw();
			}
		}

		// Output terminal
		WireIt.sn(this.outputTerminal.el, null, {
			position : "absolute",
			bottom : "-15px",
			left : (Math.floor(width / 2) - 15) + "px"
		});
		for (var j = 0; j < this.outputTerminal.wires.length; j++) {
			this.outputTerminal.wires[j].redraw();
		}
	},

	/**
	 * Extend the getConfig to add the "codeText" property
	 * @method getConfig
	 */
	getConfig : function() {
		var obj = jsBox.Container.superclass.getConfig.call(this);
		obj.codeText = this.textarea.value;
		return obj;
	}
});

/**
 * ComposedContainer is a class for Container representing Pipes.
 * It automatically generates the inputEx Form from the input Params.
 * @class ComposedContainer
 * @extends WireIt.FormContainer
 * @constructor
 */
jsBox.ComposedContainer = function(options, layer) {

	if (!options.fields) {

		options.fields = [];
		options.terminals = [];

		var pipe = jsBox.editor.getPipeByName(options.title);
		for (var i = 0; i < pipe.modules.length; i++) {
			var m = pipe.modules[i];
			if (m.name == "input") {
				m.value.input.inputParams.wirable = true;
				options.fields.push(m.value.input);
			} else if (m.name == "output") {
				options.terminals.push({
					name : m.value.name,
					"direction" : [0, 1],
					"offsetPosition" : {
						"left" : options.terminals.length * 40,
						"bottom" : -15
					},
					"ddConfig" : {
						"type" : "output",
						"allowedTypes" : ["input"]
					}
				});
			}
		}
	}

	jsBox.ComposedContainer.superclass.constructor.call(this, options, layer);
};
YAHOO.extend(jsBox.ComposedContainer, WireIt.FormContainer);
