import React from 'react';
import '../styles/LoginForm.css';
import { TiUser } from "react-icons/ti";
import { TiLockClosed } from "react-icons/ti";

const LoginForm = () => {
    return (  
        <div className="wrapper">
            <form action="">
                <h1>Login</h1>
                <div className="input-box">
                    <TiUser />
                    <input type="text" placeholder='Username' required/>
                </div>
                <div className="input-box">
                    <TiLockClosed />
                    <input type="text" placeholder='Password' required/>
                </div>
                <div className="remember-forgot">
                    <label><input type="checkbox"/>Remember me</label>
                    <a href="#">Forgot password?</a>
                </div>

                <button className="submit-button" type="submit">Login</button>

                <div className="register-link">
                    <p>Not a member? <a href="#">Register here!</a></p>
                </div>
            </form>
        </div>
    );
}
 
export default LoginForm;