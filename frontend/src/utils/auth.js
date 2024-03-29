import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, signOut } from "firebase/auth";

const firebaseConfig = {
    apiKey: import.meta.env.VITE_APP_API_KEY,
    authDomain: import.meta.env.VITE_APP_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_APP_PROJECT_ID,
    storageBucket: import.meta.env.VITE_APP_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_APP_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_APP_ID,
    measurementId: import.meta.env.VITE_APP_MEASUREMENT_ID
};

initializeApp(firebaseConfig);

class Auth {
    async register(email, password) {
        try {
            const auth = getAuth();
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const idToken = await userCredential.user.getIdToken();
            document.cookie = `token=${idToken}; expires=Wed, 8 Dec 2024 12:00:00 UTC`;
            return idToken;
        } catch (error) {
            throw error;
        }
    }

    async login(email, password) {
        try {
            const auth = getAuth();
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const idToken = await userCredential.user.getIdToken();
            document.cookie = `token=${idToken}; expires=Wed, 8 Dec 2024 12:00:00 UTC`;
            return idToken;
        } catch (error) {
            throw error;
        }
    }

    async checkState() {
        return new Promise((resolve) => {
            const auth = getAuth();
            const unsubscribe = onAuthStateChanged(auth, (user) => {
                unsubscribe();
                resolve(user);
            });
        });
    }

    async signout(){
        try {
            const auth = getAuth()
            signOut(auth).then(() => {
                return "Sign out successful"
            })
        } catch (error) {
            return error
        }
    }
}

export default new Auth();
