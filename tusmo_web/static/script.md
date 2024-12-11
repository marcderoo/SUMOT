## Members

<dl>
<dt><a href="#score">score</a></dt>
<dd><p>Use saved score</p>
</dd>
<dt><a href="#lastTouchEnd">lastTouchEnd</a></dt>
<dd><p>Prevent zoom by double tap on iPhone</p>
</dd>
<dt><a href="#NBLETTERS">NBLETTERS</a></dt>
<dd><p>Defines the game parameters, including the number of letters in the word to be guessed, the number of attempts, etc.</p>
</dd>
</dl>

## Constants

<dl>
<dt><a href="#confetti">confetti</a></dt>
<dd><p>Creates a Confetti object for visual effects.</p>
</dd>
<dt><a href="#anecdotes">anecdotes</a></dt>
<dd><p>Definition of randomly selected anecdotes related to the “Motus” game.</p>
</dd>
</dl>

## Functions

<dl>
<dt><a href="#addLetter">addLetter(letter, state, pos, countRes)</a></dt>
<dd><p>Adds information on each letter (number of occurrences and correct positions).</p>
</dd>
<dt><a href="#verify">verify(written_word)</a> ⇒ <code>Array</code></dt>
<dd><p>Checks the correspondence between the written word and the real word.
Returns a table with results (2 = correct position, 1 = letter present but misplaced, 0 = letter absent).</p>
</dd>
<dt><a href="#showDialog">showDialog(showWord)</a></dt>
<dd><p>Show the final dialog (winner or looser screen)</p>
</dd>
<dt><a href="#processKeys">processKeys(data, [player], [aiDifficulty])</a> ⇒ <code>Promise.&lt;void&gt;</code></dt>
<dd><p>Processes a sequence of key presses to simulate typing and backspace actions.
It will type each character in the given string <code>data</code>, and simulate the key press behavior, including pauses between key presses.
If the operation is cancelled during execution, it will stop typing.</p>
</dd>
<dt><a href="#enterKey">enterKey(key, [player], [aiDifficulty])</a></dt>
<dd><p>Simulates pressing a key for a player in a grid-based interface.
This function handles key presses for characters (letters), BACKSPACE, and ENTER.
It manages the state of the cells, including adding/removing classes and content, 
and updates the UI to reflect the player&#39;s actions.</p>
</dd>
</dl>

<a name="score"></a>

## score
Use saved score

**Kind**: global variable  
<a name="lastTouchEnd"></a>

## lastTouchEnd
Prevent zoom by double tap on iPhone

**Kind**: global variable  
<a name="NBLETTERS"></a>

## NBLETTERS
Defines the game parameters, including the number of letters in the word to be guessed, the number of attempts, etc.

**Kind**: global variable  
<a name="confetti"></a>

## confetti
Creates a Confetti object for visual effects.

**Kind**: global constant  
<a name="anecdotes"></a>

## anecdotes
Definition of randomly selected anecdotes related to the “Motus” game.

**Kind**: global constant  
<a name="addLetter"></a>

## addLetter(letter, state, pos, countRes)
Adds information on each letter (number of occurrences and correct positions).

**Kind**: global function  

| Param | Type | Description |
| --- | --- | --- |
| letter | <code>string</code> | The letter to add. |
| state | <code>number</code> | Letter status (2 for well placed, 1 for elsewhere present, 0 for absent). |
| pos | <code>number</code> | The position of the letter in the word. |
| countRes | <code>number</code> | The number of times the letter has been encountered. |

<a name="verify"></a>

## verify(written_word) ⇒ <code>Array</code>
Checks the correspondence between the written word and the real word.
Returns a table with results (2 = correct position, 1 = letter present but misplaced, 0 = letter absent).

**Kind**: global function  
**Returns**: <code>Array</code> - An array of verification results.  

| Param | Type | Description |
| --- | --- | --- |
| written_word | <code>string</code> | The written word to check. |

<a name="showDialog"></a>

## showDialog(showWord)
Show the final dialog (winner or looser screen)

**Kind**: global function  

| Param | Type | Description |
| --- | --- | --- |
| showWord | <code>boolean</code> | Show the word in the dialog |

<a name="processKeys"></a>

## processKeys(data, [player], [aiDifficulty]) ⇒ <code>Promise.&lt;void&gt;</code>
Processes a sequence of key presses to simulate typing and backspace actions.
It will type each character in the given string `data`, and simulate the key press behavior, including pauses between key presses.
If the operation is cancelled during execution, it will stop typing.

**Kind**: global function  
**Returns**: <code>Promise.&lt;void&gt;</code> - A promise that resolves when the function completes.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| data | <code>string</code> |  | The string of data to be typed. |
| [player] | <code>number</code> | <code>1</code> | The player number (1 for AI, 0 for human, -1 for solo mode). |
| [aiDifficulty] | <code>number</code> | <code>-1</code> | The difficulty level for AI (used only if it's AI turn). |


* [processKeys(data, [player], [aiDifficulty])](#processKeys) ⇒ <code>Promise.&lt;void&gt;</code>
    * [~func(x)](#processKeys..func) ⇒ <code>number</code>
    * [~norm(i)](#processKeys..norm) ⇒ <code>number</code>

<a name="processKeys..func"></a>

### processKeys~func(x) ⇒ <code>number</code>
A helper function for transforming the value of x based on the data length.

**Kind**: inner method of [<code>processKeys</code>](#processKeys)  
**Returns**: <code>number</code> - The transformed value of x.  

| Param | Type | Description |
| --- | --- | --- |
| x | <code>number</code> | The input value. |

<a name="processKeys..norm"></a>

### processKeys~norm(i) ⇒ <code>number</code>
Normalizes the index for the key press delay.

**Kind**: inner method of [<code>processKeys</code>](#processKeys)  
**Returns**: <code>number</code> - The delay time in milliseconds.  

| Param | Type | Description |
| --- | --- | --- |
| i | <code>number</code> | The index of the character in the data string. |

<a name="enterKey"></a>

## enterKey(key, [player], [aiDifficulty])
Simulates pressing a key for a player in a grid-based interface.
This function handles key presses for characters (letters), BACKSPACE, and ENTER.
It manages the state of the cells, including adding/removing classes and content, 
and updates the UI to reflect the player's actions.

**Kind**: global function  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| key | <code>string</code> |  | The key to be pressed (e.g., 'A', 'BACKSPACE', 'ENTER'). |
| [player] | <code>number</code> | <code>-1</code> | The player number (1 for AI, 0 for human, -1 for solo mode). |
| [aiDifficulty] | <code>number</code> | <code>-1</code> | The difficulty level for AI (used only if it's IA turn). |

