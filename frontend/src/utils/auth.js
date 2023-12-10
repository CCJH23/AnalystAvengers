import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCOGOrr6vPU4O8MaHJUnjH3anGfDyrW7YM",
    authDomain: "analystavengers.firebaseapp.com",
    projectId: "analystavengers",
    storageBucket: "analystavengers.appspot.com",
    messagingSenderId: "496207571190",
    appId: "1:496207571190:web:f5766e0a6bd8d20db7a4d7",
    measurementId: "G-6F1MHJTJ19"
};

initializeApp(firebaseConfig);

class Auth {
    async register(email, password) {
        try {
            const auth = getAuth()
            const userCredential = await createUserWithEmailAndPassword(auth, email, password)
            return userCredential.user
        } catch (error) {
            throw error;
        }
    }
}

export default new Auth()