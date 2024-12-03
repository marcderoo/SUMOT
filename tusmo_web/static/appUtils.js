class AppUtils {
    // Instance unique pour le Singleton
    static instance;

    // Constructeur privé pour éviter une instanciation multiple
    constructor() {
        if (AppUtils.instance) {
            return AppUtils.instance;
        }

        this.events = {}; // Stockage des événements et de leurs abonnés
        AppUtils.instance = this;
    }

    // Charge des fichiers en utilisant le cache
    async loadObj(url) {
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
        if (!this.events[eventName]) return;

        this.events[eventName].forEach((callback) => callback(data));
    }
}

//Managing events
const appUtils = new AppUtils();

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