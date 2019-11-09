
var context = new AudioContext(),
oscillator,
mousedown = false,
gainNode = context.createGain();

gainNode.connect(context.destination);

document.addEventListener("mousedown", function(e) {


oscillator = context.createOscillator();
oscillator.connect(gainNode);

calculateFrequencyAndGain(e);

oscillator.start(context.currentTime);
});

document.body.addEventListener("mousemove", function(e) {
    calculateFrequencyAndGain(e);

});


function calculateFrequencyAndGain(e) {
var maxFrequency = 2000,
    minFrequency = 20,
    maxGain = 1,
    minGain = 0;


oscillator.frequency.setTargetAtTime(
    ((e.clientX / window.innerWidth) * maxFrequency)
    + minFrequency, context.currentTime, 0.01);
gainNode.gain.setTargetAtTime(
    1 - ((e.clientY / window.innerHeight) * maxGain)
    + minGain, context.currentTime, 0.01);
}

