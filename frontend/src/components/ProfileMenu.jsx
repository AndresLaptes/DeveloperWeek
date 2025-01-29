import { Link } from 'react-router-dom'; 
import { useState, useEffect, useRef } from "react";
import '../styles/ProfileMenu.css';
import defaultUser from "../assets/unlogged-profile.svg";

const ProfileMenu = ({children, initialIsLogged}) => {
    const [profileDropdown, setProfileDropdown] = useState(false);
    const [isLogged, setIsLogged] = useState(initialIsLogged);
    
    const dropdownRef = useRef(null);
    const userPhoto = "";

    useEffect(() => {

        const handleClickOutside = () => {
            if(dropdownRef.current && !dropdownRef.current.contains(event.target)){
                setProfileDropdown(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    
    }, []);




    return (
         <div>
            <div className="profile-container"> 
                <img 
                    src= {isLogged ? userPhoto : defaultUser}
                    alt="user" 
                    className={`profile-image ${isLogged ? 'logged' : 'unlogged'}`}
                    onClick={() => setProfileDropdown(!profileDropdown)}
                />
            </div>
            <div className={`profile-dropdown ${profileDropdown ? 'active' : ''}`} ref={dropdownRef}>
                
                <div className={`profile-dropdown-arrow ${profileDropdown ? 'active' : ''}`}></div>
                    {
                        isLogged &&
                        <ul className={`profile-menu-list $ logged`}>
                        <li className="menu-item">
                            <Link to="/Profile">Profile</Link>
                        </li>
                        <li className="menu-item">
                            <Link to="/Settings">Settings</Link>
                        </li>
                        <li className="menu-item" onClick={() => setIsLogged(!isLogged)}>Logout</li>
                        </ul>
                    }
                    
                    {
                        !isLogged &&
                        <ul className={`profile-menu-list $ 'unlogged'`}>
                            <li className="menu-item">
                                <Link to="/Login">Log In</Link>
                            </li>
                            <li className="menu-item">
                                <Link to="/Signup">Sign Up</Link>
                            </li>
                            <li className="menu-item" onClick={() => setIsLogged(!isLogged)}>Click to simulate login</li>
                        </ul>
                    }
                    
                
            </div>
         </div>
    )
}

export default ProfileMenu