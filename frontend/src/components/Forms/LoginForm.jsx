import React from 'react';
import '../../styles/LoginForm.css';
import { TiUser } from "react-icons/ti";
import { TiLockClosed } from "react-icons/ti";

const LoginForm = () => {
    
    const handleSubmit = () => {
        
    }

    
    return (  
        <div className="wrapper">
            <h1>Login</h1>
            <form action="">
                <div className="input-box">
                    <input type="text" placeholder='Username' required/>
                    <TiUser className="icon"/>
                </div>
                <div className="input-box">
                    <input type="text" placeholder='Password' required/>
                    <TiLockClosed className="icon"/>
                </div>
                <div className="remember-forgot">
                    <label><input type="checkbox"/>Remember me</label>
                    <a href="#">Forgot password?</a>
                </div>

                <button className="submit-button" type="submit" onClick={handleSubmit()}>Login</button>

                <div className="register-link">
                    <p>Not a member? <a href="#">Register here!</a></p>
                </div>
            </form>
        </div>
    );
}
 
export default LoginForm;