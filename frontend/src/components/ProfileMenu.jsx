import { Link } from 'react-router-dom'; 
import { TiUser } from "react-icons/ti";
import { useState, useEffect, useRef } from "react";
import '../styles/ProfileMenu.css';
import defaultUser from "../assets/unlogged-profile.svg";

const ProfileMenu = ({children, initialIsLogged}) => {
    const [profileDropdown, setProfileDropdown] = useState(false);
    const [isLogged, setIsLogged] = useState(initialIsLogged);
    
    const dropdownRef = useRef(null);
    const userPhoto = ""; //TODO UPDATE ACCORDING TO PROFILE PICTURE PATH

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
         <div ref={dropdownRef}>
            <div className="profile-container" onClick={() => setProfileDropdown(!profileDropdown)}> 
                {
                    ( isLogged 
                    ? <img 
                        src= "userPhoto" //TODO UPDATE ACCORDING TO PROFILE PICTURE PATH
                        alt="user" 
                        className="profile-image logged" 
                      />
                    : <TiUser className="profile-image unlogged"/> 
                    )
                }
            </div>
            <div className={`profile-dropdown ${profileDropdown ? 'active' : ''}`}>
                
                <div className={`profile-dropdown-arrow ${profileDropdown ? 'active' : ''}`}></div>
                {
                    (isLogged 
                    ? <ul className={`profile-menu-list $ logged`}>
                        <li className="menu-item">
                            <Link to="/Profile">Profile</Link>
                        </li>
                        <li className="menu-item">
                            <Link to="/Settings">Settings</Link>
                        </li>
                        <li className="menu-item" onClick={() => setIsLogged(!isLogged)}>Logout</li>
                      </ul>
                    : <ul className={`profile-menu-list $ 'unlogged'`}>
                        <li className="menu-item">
                            <Link to="/Login">Log In</Link>
                        </li>
                        <li className="menu-item">
                            <Link to="/Signup">Sign Up</Link>
                        </li>
                        <li className="menu-item" onClick={() => setIsLogged(!isLogged)}>Click to simulate login</li>
                      </ul>
                    )
                }   
            </div>
         </div>
    )
}

export default ProfileMenu