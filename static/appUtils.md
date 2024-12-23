## Classes

<dl>
<dt><a href="#AppUtils">AppUtils</a></dt>
<dd><p>Utility class to provide various functionalities, including dynamic CSS rules management,
event handling, and caching via localStorage. Implements the Singleton design pattern.</p>
</dd>
</dl>

## Constants

<dl>
<dt><a href="#appUtils">appUtils</a></dt>
<dd><p>Instance of the utility class to provide various functionalities, including dynamic CSS rules management,
event handling, and caching via localStorage.</p>
</dd>
</dl>

<a name="AppUtils"></a>

## AppUtils
Utility class to provide various functionalities, including dynamic CSS rules management,event handling, and caching via localStorage. Implements the Singleton design pattern.

**Kind**: global class  

* [AppUtils](#AppUtils)
    * [new AppUtils()](#new_AppUtils_new)
    * [.instance](#AppUtils+instance) : [<code>AppUtils</code>](#AppUtils)
    * [.isMobileDevice](#AppUtils+isMobileDevice) : <code>boolean</code>
    * [.style](#AppUtils+style) : <code>HTMLStyleElement</code>
    * [.idsRules](#AppUtils+idsRules) : <code>Array.&lt;string&gt;</code>
    * [.idsRulesFunc](#AppUtils+idsRulesFunc) : <code>Object.&lt;string, {eventName: string, callback: function()}&gt;</code>
    * [.doIfOrWhenEvents](#AppUtils+doIfOrWhenEvents) : <code>Object.&lt;string, Array.&lt;function()&gt;&gt;</code>
    * [.events](#AppUtils+events) : <code>Object.&lt;string, Array.&lt;function()&gt;&gt;</code>
    * [.pastEvents](#AppUtils+pastEvents) : <code>Set.&lt;string&gt;</code>
    * [.loadObj(url, [base64])](#AppUtils+loadObj) ⇒ <code>Promise.&lt;string&gt;</code>
    * [.loadKey(key, [default_])](#AppUtils+loadKey) ⇒ <code>string</code>
    * [.updateKey(key, val)](#AppUtils+updateKey)
    * [.addRule(id, rule)](#AppUtils+addRule)
    * [.removeRule(id)](#AppUtils+removeRule)
    * [.linkRuleTo(id, eventName, func)](#AppUtils+linkRuleTo)
    * [.doIfOrWhen(eventName, callback)](#AppUtils+doIfOrWhen)
    * [.subscribe(eventName, callback)](#AppUtils+subscribe)
    * [.unsubscribe(eventName, callback)](#AppUtils+unsubscribe)
    * [.emit(eventName, [data])](#AppUtils+emit)
    * [.goToLocation(url)](#AppUtils+goToLocation)

<a name="new_AppUtils_new"></a>

### new AppUtils()
Private constructor to ensure Singleton pattern.

<a name="AppUtils+instance"></a>

### appUtils.instance : [<code>AppUtils</code>](#AppUtils)
The unique instance of the class.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+isMobileDevice"></a>

### appUtils.isMobileDevice : <code>boolean</code>
Detects if the user is on a mobile device.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+style"></a>

### appUtils.style : <code>HTMLStyleElement</code>
A style element for managing dynamic CSS rules.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+idsRules"></a>

### appUtils.idsRules : <code>Array.&lt;string&gt;</code>
List of CSS rule IDs.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+idsRulesFunc"></a>

### appUtils.idsRulesFunc : <code>Object.&lt;string, {eventName: string, callback: function()}&gt;</code>
Mapping of rule IDs to event associations and callbacks.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+doIfOrWhenEvents"></a>

### appUtils.doIfOrWhenEvents : <code>Object.&lt;string, Array.&lt;function()&gt;&gt;</code>
Deferred or conditional event handlers.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+events"></a>

### appUtils.events : <code>Object.&lt;string, Array.&lt;function()&gt;&gt;</code>
Mapping of event names to their listeners.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+pastEvents"></a>

### appUtils.pastEvents : <code>Set.&lt;string&gt;</code>
Set of past events.

**Kind**: instance property of [<code>AppUtils</code>](#AppUtils)  
<a name="AppUtils+loadObj"></a>

### appUtils.loadObj(url, [base64]) ⇒ <code>Promise.&lt;string&gt;</code>
Asynchronously loads an object, with optional caching in localStorage.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  
**Returns**: <code>Promise.&lt;string&gt;</code> - The loaded data.  
**Throws**:

- <code>Error</code> If the fetch request fails.


| Param | Type | Default | Description |
| --- | --- | --- | --- |
| url | <code>string</code> |  | The URL of the resource to load. |
| [base64] | <code>boolean</code> | <code>false</code> | Whether to convert the response to Base64 format. |

<a name="AppUtils+loadKey"></a>

### appUtils.loadKey(key, [default_]) ⇒ <code>string</code>
Loads a value from localStorage or initializes it with a default value.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  
**Returns**: <code>string</code> - The loaded or default value.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| key | <code>string</code> |  | The key to load. |
| [default_] | <code>string</code> | <code>null</code> | The default value to set if the key does not exist. |

<a name="AppUtils+updateKey"></a>

### appUtils.updateKey(key, val)
Updates a value in localStorage.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| key | <code>string</code> | The key to update. |
| val | <code>string</code> | The new value to set. |

<a name="AppUtils+addRule"></a>

### appUtils.addRule(id, rule)
Adds or updates a dynamic CSS rule.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| id | <code>string</code> | The unique ID of the rule. |
| rule | <code>string</code> | The CSS rule to add. |

<a name="AppUtils+removeRule"></a>

### appUtils.removeRule(id)
Removes a dynamic CSS rule and its associated events.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| id | <code>string</code> | The ID of the rule to remove. |

<a name="AppUtils+linkRuleTo"></a>

### appUtils.linkRuleTo(id, eventName, func)
Links a dynamic CSS rule to an event with a function generating the rule.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| id | <code>string</code> | The unique ID of the rule. |
| eventName | <code>string</code> | The name of the event to link. |
| func | <code>function</code> | A function generating the CSS rule. |

<a name="AppUtils+doIfOrWhen"></a>

### appUtils.doIfOrWhen(eventName, callback)
Executes a function immediately if an event has already occurred or when it occurs.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| eventName | <code>string</code> | The name of the event. |
| callback | <code>function</code> | The function to execute. |

<a name="AppUtils+subscribe"></a>

### appUtils.subscribe(eventName, callback)
Subscribes a callback to an event.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| eventName | <code>string</code> | The name of the event. |
| callback | <code>function</code> | The callback to subscribe. |

<a name="AppUtils+unsubscribe"></a>

### appUtils.unsubscribe(eventName, callback)
Unsubscribes a callback from an event.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| eventName | <code>string</code> | The name of the event. |
| callback | <code>function</code> | The callback to unsubscribe. |

<a name="AppUtils+emit"></a>

### appUtils.emit(eventName, [data])
Emits an event, notifying all its subscribers.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| eventName | <code>string</code> | The name of the event. |
| [data] | <code>any</code> | Optional data to pass to subscribers. |

<a name="AppUtils+goToLocation"></a>

### appUtils.goToLocation(url)
Redirects to a URL with a transition animation.

**Kind**: instance method of [<code>AppUtils</code>](#AppUtils)  

| Param | Type | Description |
| --- | --- | --- |
| url | <code>string</code> | The destination URL. |

<a name="appUtils"></a>

## appUtils
Instance of the utility class to provide various functionalities, including dynamic CSS rules management,event handling, and caching via localStorage.

**Kind**: global constant  
