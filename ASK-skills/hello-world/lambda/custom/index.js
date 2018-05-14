
'use strict';
var Alexa = require("alexa-sdk");
var http = require("http");

// For detailed tutorial on how to making a Alexa skill,
// please visit us at http://alexa.design/build


exports.handler = function(event, context) {
    var alexa = Alexa.handler(event, context);
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var handlers = {
    'LaunchRequest': function () {
        this.emit('SayHello');
    },
    'HelloWorldIntent': function () {
        this.emit('SayHello');
    },
    'MyNameIsIntent': function () {
        this.emit('SayHelloName');
    },
    'SayHello': function () {
        //http://api.open-notify.org/astros.json
		
		
        var options = {//temperature
          host: 'api.thingspeak.com',
          port: 80,
          method: 'GET',
          path: '/channels/495134/feeds/last.json?api_key=T2G0DMCVYRCMNUZS&results=2'
        }

        var req = http.request(options, res => {//speech
            res.setEncoding('utf8');
            var returnData = "";

            res.on('data', chunk => {
                returnData = returnData + chunk;
            });

            res.on('end', () => {
              var result = JSON.parse(returnData);
				
			  if (result.field4 >= 110000)
						var qualspeech=(`the air quality is Excellent. Sensor reads ${result.field4} Ohms.`);
				
              if (result.field4 >= 90000 && result.field4 < 110000)
                        var qualspeech=(`the air quality is Great. Sensor reads ${result.field4} Ohms.`);
						
              if (result.field4 >= 70000 && result.field4 < 90000)
                        var qualspeech=(`the air quality is OK. Sensor reads ${result.field4} Ohms.`);
						
              if (result.field4 >= 50000 && result.field4 < 70000)
                        var qualspeech=(`the air quality is Poor, sensitive persons may suffer. Sensor reads ${result.field4} Ohms.`);
						
              if (result.field4 >= 30000 && result.field4 < 50000)
                        var qualspeech=(`the air quality is Really bad, protection is advised or moving to fresh air. Sensor reads ${result.field4} Ohms.`); 
						
              if (result.field4 < 30000)
                        var qualspeech=(`the air quality is dangerous, wear heavy protection or move to the outdoors. Sensor reads ${result.field4} Ohms.`);
              
              this.response.speak(`This is what I found, the current temperature reading from the Raspberry Pi sensor is ${result.field1} Degrees Fahrenheit, the humidity is ${result.field2}%RH, the air pressure is ${result.field3}hPa, and `+ qualspeech);

             this.emit(':responseReady');
            });

        });
        req.end();
		/*
		var options = {//humidity
          host: 'api.thingspeak.com',
          port: 80,
          method: 'GET',
          path: '/channels/495134/fields/2/last'
        }

        var req = http.request(options, res => {//speech
            res.setEncoding('utf8');
            var returnData = "";

            res.on('data', chunk => {
                returnData = returnData + chunk;
            });

            res.on('end', () => {
              var result = JSON.parse(returnData);

              //callback(result);
              this.response.speak(`The humidity is ${result}%RH`);

             this.emit(':responseReady');
            });

        });
        req.end();
		
		var options = {//pressure
          host: 'api.thingspeak.com',
          port: 80,
          method: 'GET',
          path: '/channels/495134/fields/3/last'
        }

        var req = http.request(options, res => {//speech
            res.setEncoding('utf8');
            var returnData = "";

            res.on('data', chunk => {
                returnData = returnData + chunk;
            });

            res.on('end', () => {
              var result = JSON.parse(returnData);

              //callback(result);
              this.response.speak(`The air pressure is ${result}hPa`);

             this.emit(':responseReady');
            });

        });
        req.end();
		
		var options = {//quality
          host: 'api.thingspeak.com',
          port: 80,
          method: 'GET',
          path: '/channels/495134/fields/4/last'
        }

        var req = http.request(options, res => {//speech
            res.setEncoding('utf8');
            var returnData = "";

            res.on('data', chunk => {
                returnData = returnData + chunk;
            });

            res.on('end', () => {
              var result = JSON.parse(returnData);

              
			  
			  if (result >= 110000)
                        this.response.speak(`The air quality is Excellent. Sensor reads ${result}`);
				
              if (result >= 90000 && result < 110000)
                        this.response.speak(`The air quality is Great. Sensor reads ${result} Ohms.`);
						
              if (result >= 70000 && result < 90000)
                        this.response.speak(`The air quality is OK. Sensor reads ${result} Ohms.`);
						
              if (result >= 50000 && result < 70000)
                        this.response.speak(`The air quality is Poor, sensitive persons may suffer. Sensor reads ${result} Ohms.`);
						
              if (result >= 30000 && result < 50000)
                        this.response.speak(`The air quality is Really bad, protection is advised or moving to fresh air. Sensor reads ${result} Ohms.`); 
						
              if (result < 30000)
                        this.response.speak(`Dangerous air quality, wear heavy protection or move to the outdoors. Sensor reads ${result} Ohms.`);


			  
				
             this.emit(':responseReady');
            });

        });
        req.end();
*/
    },
    'SayHelloName': function () {
        var name = this.event.request.intent.slots.name.value;
        this.response.speak('My Boi ' + name)
            .cardRenderer('Sensor_Reading', 'BME680 ' + name);
        this.emit(':responseReady');
    },
    'SessionEndedRequest' : function() {
        console.log('Session ended with reason: ' + this.event.request.reason);
    },
    'AMAZON.StopIntent' : function() {
        this.response.speak('Bye');
        this.emit(':responseReady');
    },
    'AMAZON.HelpIntent' : function() {
        this.response.speak("You can try: 'alexa, what is my sensor reading' or 'alexa,'Something irrelevant like what's up with Ken Kaneki'");
        this.emit(':responseReady');
    },
    'AMAZON.CancelIntent' : function() {
        this.response.speak('Bye');
        this.emit(':responseReady');
    },
    'Unhandled' : function() {
        this.response.speak("Sorry, I didn't get that. Can try again?");
    }
};
