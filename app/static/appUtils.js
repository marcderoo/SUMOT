/**
 * Utility class to provide various functionalities, including dynamic CSS rules management, event handling, and caching via localStorage. Implements the Singleton design pattern.
 */
class AppUtils {
    /**
     * The unique instance of the class.
     * @type {AppUtils}
     */
    static instance;

    /**
     * Private constructor to ensure Singleton pattern.
     */
    constructor() {
        if (AppUtils.instance) {
            return AppUtils.instance; // Returns the existing instance
        }
        AppUtils.instance = this;

        /**
         * Detects if the user is on a mobile device.
         * @type {boolean}
         */
        this.isMobileDevice = navigator.userAgent.match(/iPhone/i)
        || navigator.userAgent.match(/webOS/i)
        || navigator.userAgent.match(/Android/i)
        || navigator.userAgent.match(/iPad/i)
        || navigator.userAgent.match(/iPod/i)
        || navigator.userAgent.match(/BlackBerry/i)
        || navigator.userAgent.match(/Windows Phone/i);

        /**
         * A style element for managing dynamic CSS rules.
         * @type {HTMLStyleElement}
         */
        this.style = document.createElement('style');
        document.head.appendChild(this.style);

        /**
         * List of CSS rule IDs.
         * @type {string[]}
         */
        this.idsRules = [];

        /**
         * Mapping of rule IDs to event associations and callbacks.
         * @type {Object.<string, {eventName: string, callback: Function}>}
         */
        this.idsRulesFunc = {};

        /**
         * Deferred or conditional event handlers.
         * @type {Object.<string, Function[]>}
         */
        this.doIfOrWhenEvents = {};

        /**
         * Mapping of event names to their listeners.
         * @type {Object.<string, Function[]>}
         */
        this.events = {};

        /**
         * Set of past events.
         * @type {Set<string>}
         */
        this.pastEvents = new Set();
    }

    /**
     * Asynchronously loads an object, with optional caching in localStorage.
     * @param {string} url - The URL of the resource to load.
     * @param {boolean} [base64=false] - Whether to convert the response to Base64 format.
     * @returns {Promise<string>} The loaded data.
     * @throws {Error} If the fetch request fails.
     */
    async loadObj(url, base64 = false) {
        // Checks if object is in localStorage
        const obj = localStorage.getItem(url);
        if (obj) {
            return obj; // Returns directly if found
        } else {
            // Download object via fetch
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Erreur lors du téléchargement : ${response.statusText}`);
            }

            // Handles base64 formats if specified
            if(base64){
                const blob = await response.blob();
    
                // Converts blob to Base64
                return await new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = function () {
                        const base64Data = reader.result;
                        localStorage.setItem(url, base64Data); // Save item in localStorage
                        resolve(base64Data); // Returns encoded data
                    };
                    reader.onerror = reject; // Handles errors
                    reader.readAsDataURL(blob); // Reading the blob
                });
            } else {
                // Returns text data and stores it in cache
                const res =  await response.text();
                localStorage.setItem(url, res);
                return res;
            }
        }
    }

    /**
     * Loads a value from localStorage or initializes it with a default value.
     * @param {string} key - The key to load.
     * @param {string} [default_=null] - The default value to set if the key does not exist.
     * @returns {string} The loaded or default value.
     */
    loadKey(key, default_ = null) {
        let val = localStorage.getItem(key);
        if(val){
            return val;
        } else {
            localStorage.setItem(key, default_);
            return default_;
        }
    }

    /**
     * Updates a value in localStorage.
     * @param {string} key - The key to update.
     * @param {string} val - The new value to set.
     */
    updateKey(key, val) {
        localStorage.setItem(key, val);
    } 

    /**
     * Adds or updates a dynamic CSS rule.
     * @param {string} id - The unique ID of the rule.
     * @param {string} rule - The CSS rule to add.
     */
    addRule(id, rule) {
        let idx = this.idsRules.indexOf(id);
        if(idx >= 0){
            this.style.sheet.deleteRule(idx);
        } else {
            idx = this.idsRules.length;
            this.idsRules.push(id);
        }
        this.style.sheet.insertRule(rule, idx);
    }

    /**
     * Removes a dynamic CSS rule and its associated events.
     * @param {string} id - The ID of the rule to remove.
     */
    removeRule(id) {
        let idx = this.idsRules.indexOf(id);
        if(idx >= 0){
            this.style.sheet.deleteRule(idx);
            this.idsRules.splice(idx, 1);
        }

        if(this.idsRulesFunc[id]){
            this.unsubscribe(this.idsRulesFunc[id]["eventName"], this.idsRulesFunc[id]["callback"]);
            delete this.idsRulesFunc[id];
        }
    }

    /**
     * Links a dynamic CSS rule to an event with a function generating the rule.
     * @param {string} id - The unique ID of the rule.
     * @param {string} eventName - The name of the event to link.
     * @param {Function} func - A function generating the CSS rule.
     */
    linkRuleTo(id, eventName, func){
        this.addRule(id, func());
        
        const callback = () => {
            this.addRule(id, func());
        }
        this.subscribe(eventName, callback);
        this.idsRulesFunc[id] = {"eventName" : eventName, "callback" : callback};
    }

    /**
     * Executes a function immediately if an event has already occurred or when it occurs.
     * @param {string} eventName - The name of the event.
     * @param {Function} callback - The function to execute.
     */
    doIfOrWhen(eventName, callback) {
        if(this.pastEvents.has(eventName)){
            callback();
        } else {
            if (!this.doIfOrWhenEvents[eventName]) {
                this.doIfOrWhenEvents[eventName] = [];
            }
            this.doIfOrWhenEvents[eventName].push(callback);
        }
    }

    /**
     * Subscribes a callback to an event.
     * @param {string} eventName - The name of the event.
     * @param {Function} callback - The callback to subscribe.
     */
    subscribe(eventName, callback) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(callback);
    }

    /**
     * Unsubscribes a callback from an event.
     * @param {string} eventName - The name of the event.
     * @param {Function} callback - The callback to unsubscribe.
     */
    unsubscribe(eventName, callback) {
        if (!this.events[eventName]) return;

        this.events[eventName] = this.events[eventName].filter(
            (listener) => listener !== callback
        );

        // Deletes the event if it no longer has subscribers
        if (this.events[eventName].length === 0) {
            delete this.events[eventName];
        }
    }

    /**
     * Emits an event, notifying all its subscribers.
     * @param {string} eventName - The name of the event.
     * @param {any} [data] - Optional data to pass to subscribers.
     */
    emit(eventName, data) {
        this.pastEvents.add(eventName);

        if(this.events[eventName]) this.events[eventName].forEach((callback) => callback(data));
        if(this.doIfOrWhenEvents[eventName]){
            this.doIfOrWhenEvents[eventName].forEach((callback) => callback());
            delete this.doIfOrWhenEvents[eventName];
        } 
    }

    /**
     * Redirects to a URL with a transition animation.
     * @param {string} url - The destination URL.
     */
    goToLocation(url){
      this.addRule("reAddBackGround", `        html {
            background-color: #FBA999;
        }`)
      this.addRule("goToLocationAnimation", `
        body {
            animation-name: revverseOpacityAnimation;
            animation-duration: 0.1s;
            opacity  : 0%;
        }
        `);
      setTimeout(()  => window.location = url, 100);
    }

    /**
     * Get user ip adress.
     * @returns {string} Id adress or null.
     */
    getIp(){
        return new Promise(resolve => fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
                resolve(data.ip);
            })
            .catch(error => {
                resolve();
            })
        )
    }
}

/**
 * Instance of the utility class to provide various functionalities, including dynamic CSS rules management,
 * event handling, and caching via localStorage.
 */
const appUtils = new AppUtils();

/* Add Classical Events */
document.addEventListener('DOMContentLoaded', () => {
    appUtils.emit("DOMContentLoaded");
});

appUtils.doIfOrWhen("DOMContentLoaded", () => {
    document.addEventListener('keydown', (event) => {
        appUtils.emit("keydown", event.key.toUpperCase());
    });

    document.addEventListener('keyup', (event) => {
        appUtils.emit("keyup", event.key.toUpperCase());
    });
});

window.addEventListener('resize', (event) => {
    appUtils.emit("windowResize", event);
});

/* Set Font Size*/
appUtils.linkRuleTo("HTMLFontSize", 'windowResize', () => 
    `html {
        font-size : ${(appUtils.isMobileDevice ? 0.03 : 0.02) *  Math.min(window.innerHeight, window.innerWidth)}px;
    }`
);

/* Manage Body Height */
appUtils.doIfOrWhen("DOMContentLoaded", () => {
    // Recovering calculated styles
    const computedStyle = getComputedStyle(document.body);

    appUtils.addRule("ManageBodyHeight", `
        body {
            height : calc(100% - 1.5rem -${computedStyle.marginTop + computedStyle.marginBottom}px);
        }
    `)
})