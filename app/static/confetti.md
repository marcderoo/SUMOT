<a name="Confetti"></a>

## Confetti
A class that manages confetti animations on the page.Implements the singleton pattern to ensure only one instance exists.

**Kind**: global class  
**Linkcode**: https://codepen.io/bananascript/pen/EyZeWm  
**Author**: Michael Beckius  

* [Confetti](#Confetti)
    * [new Confetti()](#new_Confetti_new)
    * [.container](#Confetti+container) : <code>HTMLDivElement</code>
    * [.timer](#Confetti+timer) : <code>number</code> \| <code>undefined</code>
    * [.launch()](#Confetti+launch)
    * [.stop()](#Confetti+stop)

<a name="new_Confetti_new"></a>

### new Confetti()
Creates a new Confetti instance or returns the existing one.

<a name="Confetti+container"></a>

### confetti.container : <code>HTMLDivElement</code>
The container element for the confetti.

**Kind**: instance property of [<code>Confetti</code>](#Confetti)  
<a name="Confetti+timer"></a>

### confetti.timer : <code>number</code> \| <code>undefined</code>
Timer for adding new confetti particles.

**Kind**: instance property of [<code>Confetti</code>](#Confetti)  
<a name="Confetti+launch"></a>

### confetti.launch()
Launches the confetti animation.

**Kind**: instance method of [<code>Confetti</code>](#Confetti)  
<a name="Confetti+stop"></a>

### confetti.stop()
Stops the confetti animation.

**Kind**: instance method of [<code>Confetti</code>](#Confetti)  
