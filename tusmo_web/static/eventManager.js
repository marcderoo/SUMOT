class EventManager {
    // Instance unique pour le Singleton
    static instance;

    // Constructeur privé pour éviter une instanciation multiple
    constructor() {
        if (EventManager.instance) {
            return EventManager.instance;
        }

        this.events = {}; // Stockage des événements et de leurs abonnés
        EventManager.instance = this;
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