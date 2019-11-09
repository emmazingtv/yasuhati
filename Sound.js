var context = new AudioContext(),
    oscillator,
    gainNode = context.createGain();

gainNode.connect(context.destination);

document.getElementById("myButton").addEventListener("mousedown", function (e) {
    oscillator.stop(context.currentTime);
    oscillator.disconnect();
    
});

document.getElementById("myButton").addEventListener("mouseup", function (e) {

    oscillator = context.createOscillator();
    oscillator.connect(gainNode);
   
    var frequencyInput = document.getElementById("frequencyInput").value;
    var volumeInput = document.getElementById("volumeInput").value;

    oscillator.frequency.setTargetAtTime(frequencyInput, context.currentTime, 0.01);
    gainNode.gain.setTargetAtTime(volumeInput, context.currentTime, 0.01);

    oscillator.start(context.currentTime);
    
});




