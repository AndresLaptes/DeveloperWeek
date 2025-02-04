import { Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext'

//the idea of this component is to only allow the user to navigate
//to certain pages / renders if he is logged in
const ProtectedRoute = ({children}) => {
    const { user } = useAuth;
    if (!user) return <Navigate to = "/login"/>;
    else return children;
}

export default ProtectedRoute;