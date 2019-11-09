function initialize(){
	var socket = io.connect();
	
	socket.on("position", function(data){
		document.getElementById("label").innerHTML = `Position: x=${data.x}, y=${data.y}`;
	});

}