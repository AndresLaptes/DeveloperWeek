import { div, ul } from 'framer-motion/client'
import React from 'react'
import { Link } from 'react-router-dom'; 
import { useState, useEffect, useRef } from "react";
import '../styles/ProfileMenu.css';
import user from "../assets/user.png";

const ProfileMenu = ({children}) => {
    const [profileDropdown, setProfileDropdown] = useState(false);
    const dropdownRef = useRef(null);

    useEffect( () => {

        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
              setProfileDropdown(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    
    }, []);




    return (
         <div>
            <div className="profile-container"> 
                <img 
                    src={user} 
                    alt="user" 
                    className="profile-image"
                    onClick={() => setProfileDropdown((prev) => !prev)}
                />
            </div>
            
            <div className={`profile-dropdown ${profileDropdown ? 'active' : ''}`}>
                
                <div className={`profile-dropdown-arrow ${profileDropdown ? 'active' : ''}`}></div>

                <ul className="profile-menu-list">
                    <li className="menu-item">
                        <Link to="/Profile">Profile</Link>
                    </li>
                    <li className="menu-item">Settings</li>
                    <li className="menu-item">Logout</li>
                    {
                        children &&
                        <li className="menu-item">{children}</li>
                    }
                </ul>
            </div>
         </div>
    )
}

export default ProfileMenu