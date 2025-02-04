import { createContext, useContext, useState } from "react";



const AuthenticationContext = createContext(null);

export const AuthenticationProvider = ({children}) => {
    const [user, setUser] = useState(null);

    const login = (userData) => {
        setUser(userData);
    }

    const logout = () => {
        setUser(null);
    }

    return (
        <AuthenticationContext.Provider value={{user, login, logout}}>
            {children}
        </AuthenticationContext.Provider>
    );
};

export const useAuth = () => useContext(AuthenticationContext);