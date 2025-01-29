import { Link } from 'react-router-dom'; //used for react router
import '../styles/Header.css';
import ProfileMenu from "./ProfileMenu"; 
const Header = () => {
    return (
        <header className="header">
            <nav>
                <div className="brand">
                    <Link to="/">LOGO</Link>
                </div>
                <ul className="nav-links">
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/Teams">My Team</Link>
                    </li>
                    <li>
                        <Link to="/About">About us</Link>
                    </li>
                    <li>
                        <ProfileMenu initialIsLogged={false}></ProfileMenu>
                    </li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;