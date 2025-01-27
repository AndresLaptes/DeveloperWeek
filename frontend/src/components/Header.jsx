import { Link } from 'react-router-dom'; //used for react router
import '../styles/Header.css';
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
                        <Link to="/Teams">All Teams</Link>
                    </li>
                    <li>
                        <Link to="/Profile">Profile</Link>
                    </li>
                    <li>
                        <Link to="/About">About us</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;