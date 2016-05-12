var aniWave = new wave({
			width: (window.innerWidth)/3,
			height: (window.innerHeight)/20,		
			speed: 0.1,
			container: document.getElementById('container9'),
		});
(function(){  
	var chat = {
		messageToSend: '',
		messageResponse: "main paragraph",
		messageResponse1: "Heading",
		messageResponse2: "Information taken from Wikipedia",
		messagetype: "wikipedia",
		init: function() {
			this.cacheDOM();
			this.bindEvents();
			this.messageToSend = "welcome";
			this.processMessage();
		},
		cacheDOM: function() {
			document.getElementById('wave').style.visibility = 'hidden';
			this.$chatHistory = $('.chat-history');
			this.$button = $('button');
			this.$textarea = $('#message-to-send');
			this.$chatHistoryList =  this.$chatHistory.find('ul');
		},
		bindEvents: function() {
			this.$button.on('click', this.addMessage.bind(this));
			this.$textarea.on('keyup', this.addMessageEnter.bind(this));
    	       },
		render_input: function() {
			this.scrollToBottom();
			var template = Handlebars.compile( $("#message-template").html());
			var context = { 
				messageOutput: this.messageToSend,
			};
			this.$chatHistoryList.append(template(context));
			this.scrollToBottom();
        		this.$textarea.val('');
        	},
    	    render_output: function() {
			this.scrollToBottom();
			var templateResponse = Handlebars.compile( $("#message-response-template").html());
			var contextResponse = { 
				response: this.messageResponse,
				response1: this.messageResponse1,
				response2: this.messageResponse2,
				type: this.messagetype,
       			};
			$('#classchange').removeClass('chat-history').addClass('chat-history1');
			setTimeout(function() {
       	  			this.$chatHistoryList.append(templateResponse(contextResponse));
       	  			this.scrollToBottom();
       			}.bind(this), 1500);
    	},
		addMessage: function() {
        		this.messageToSend = this.$textarea.val();
			    if (this.messageToSend.trim() !== '') {
					this.render_input();
					this.processMessage();
				}
    	},
    		processMessage: function() {
        			var data = this.messageToSend;
				$.ajax({
					type: 'POST',
					url: 'http://localhost/python/main.py',
					data: {message:data},
					success: function(response) {
						response = JSON.parse(response);
						chat.messagetype = response.type;						
						if(response.type == "wiki") {
							chat.messageResponse2 = 'Information taken from Wikipedia';
							chat.messageResponse = response.content;
							chat.messageResponse1 = response.title;
							chat.messageToSend = "continue_or_not";
						}
						else if(response.type == "calc") {
							chat.messageResponse = response.title;
							chat.messageResponse1 = response.content;
							chat.messageResponse2 = ' ';
							chat.messageToSend = "continue_or_not";
						}
						else if(response.type == "error") {
							chat.messageResponse = response.error;
							chat.messageResponse1 = '';
							chat.messageResponse2 = ' ';
							chat.messageToSend = "continue_or_not";
						}
						else if(response.type == "welcome") {
							chat.messageResponse = response.content;
							chat.messageResponse1 = '';
							chat.messageResponse2 = ' ';
						}
						else if(response.type == "continue_or_not") {
							chat.messageResponse = response.content;
							chat.messageResponse1 = '';
							chat.messageResponse2 = ' ';
							chat.messageToSend = "";
						}
						else if(response.type == "parting") {
							chat.messageResponse = response.content;
							chat.messageResponse1 = '';
							chat.messageResponse2 = '';
						}
						if(chat.messageToSend != "done") {
							chat.render_output();
							chat.messageResponse = '';
							chat.messageResponse1 = '';
							chat.messageResponse2 = '';
//							chat.messageToSend = "done";					
						}
						if(chat.messageToSend == "continue_or_not") {
							chat.processMessage();						
						}
					},
       		});
    	},
		addMessageEnter: function(event) {
			if (event.keyCode === 13) {
				this.addMessage();
        		}
		},
		scrollToBottom: function() {
			this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
		},
	};
	if (window.hasOwnProperty('webkitSpeechRecognition')) {
		var recognition = new webkitSpeechRecognition();
		recognition.continuous = true;
		recognition.interimResults = false;
		recognition.lang = "en-IN";
	}
	$( "#record" ).click(function() {
		if (window.hasOwnProperty('webkitSpeechRecognition')) {
				recognition = new webkitSpeechRecognition();
				recognition.continuous = true;
				recognition.interimResults = false;
				recognition.lang = "en-IN";
		}
		recognition.start();
		recognition.onresult = function(e) {
			chat.messageToSend = e.results[0][0].transcript;
			chat.render_input();
			chat.processMessage();
			recognition.stop();
			aniWave.stop()
			var elem = document.getElementById('wave');
			var tr = elem.parentNode;
            		tr.removeChild(elem);
			aniWave = new wave({
				width: (window.innerWidth)/3,
				height: (window.innerHeight)/20,		
				speed: 0.1,
				container: document.getElementById('container9'),
			});
			document.getElementById('wave').style.visibility = 'hidden';
			document.getElementById('send').style.visibility = 'visible';
			document.getElementById('message-to-send').style.visibility = 'visible';
			document.getElementById('record').style.visibility = 'visible';
		};
		recognition.onerror = function(e) {
			recognition.stop();
			aniWave.stop()
			var elem = document.getElementById('wave');
			var tr = elem.parentNode;
            		tr.removeChild(elem);
			aniWave = new wave({
				width: (window.innerWidth)/3,
				height: (window.innerHeight)/20,		
				speed: 0.1,
				container: document.getElementById('container9'),
			});
		}
		if (window.hasOwnProperty('webkitSpeechRecognition')) {
			document.getElementById('wave').style.visibility = 'visible';
			document.getElementById('send').style.visibility = 'hidden';
			document.getElementById('message-to-send').style.visibility = 'hidden';
			document.getElementById('record').style.visibility = 'hidden';
			aniWave.start();
		}
	});
  	chat.init();
})();
