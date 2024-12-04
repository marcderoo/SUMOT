class AppUtils {
    // Instance unique pour le Singleton
    static instance;

    // Constructeur privé pour éviter une instanciation multiple
    constructor() {
        if (AppUtils.instance) {
            return AppUtils.instance;
        }
        AppUtils.instance = this;

        this.style = document.createElement('style');
        document.head.appendChild(this.style);
        this.idsRules = [];
        this.idsRulesFunc = {};

        this.doIfOrWhenEvents = {};
        this.events = {}; // Stockage des événements et de leurs abonnés
        this.pastEvents = new Set();
    }

    // Charge des fichiers en utilisant le cache
    async loadObj(url, base64 = false) {
        // Vérifie si l'objet est dans le localStorage
        const obj = localStorage.getItem(url);
        if (obj) {
            return obj; // Retourne directement si trouvé
        } else {
            // Télécharge l'objet via fetch
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Erreur lors du téléchargement : ${response.statusText}`);
            }

            if(base64){
                const blob = await response.blob();
    
                // Convertit le blob en Base64
                return await new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = function () {
                        const base64Data = reader.result;
                        localStorage.setItem(url, base64Data); // Stocke en localStorage
                        resolve(base64Data); // Retourne les données encodées
                    };
                    reader.onerror = reject; // Gère les erreurs
                    reader.readAsDataURL(blob); // Lecture du blob
                });
            } else {
                const res =  await response.text();
                localStorage.setItem(url, res);
                return res;
            }
        }
    }

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

    linkRuleTo(id, eventName, func){
        this.addRule(id, func());
        
        const callback = () => {
            this.addRule(id, func());
        }
        this.subscribe(eventName, callback);
        this.idsRulesFunc[id] = {"eventName" : eventName, "callback" : callback};
    }

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

    // Méthode pour s'abonner à un événement
    subscribe(eventName, callback) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(callback);
    }

    // Méthode pour se désabonner d'un événement
    unsubscribe(eventName, callback) {
        if (!this.events[eventName]) return;

        this.events[eventName] = this.events[eventName].filter(
            (listener) => listener !== callback
        );

        // Supprime l'événement s'il n'a plus d'abonnés
        if (this.events[eventName].length === 0) {
            delete this.events[eventName];
        }
    }

    // Méthode pour émettre un événement
    emit(eventName, data) {
        this.pastEvents.add(eventName);

        if(this.events[eventName]) this.events[eventName].forEach((callback) => callback(data));
        if(this.doIfOrWhenEvents[eventName]){
            this.doIfOrWhenEvents[eventName].forEach((callback) => callback());
            delete this.doIfOrWhenEvents[eventName];
        } 
    }
}

//Managing events
const appUtils = new AppUtils();

//classical events
document.addEventListener('DOMContentLoaded', () => {
    appUtils.emit("DOMContentLoaded");
});

appUtils.subscribe("DOMContentLoaded", () => {
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

/**Set Font Size*/
appUtils.linkRuleTo("HTMLFontSize", 'windowResize', () => 
    `html {
        font-size : ${0.02 *  window.innerHeight}px;
    }`
);