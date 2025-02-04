import React, { useState } from 'react';
import '../styles/LoginForm.css';
import { TiUser } from "react-icons/ti";
import { TiLockClosed } from "react-icons/ti";
import axios from 'axios';

const LoginForm = () => {
    const [email, setemail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            console.log(email, password);
            const response = await axios.post("http://localhost:3000/user/login", {
                email,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.data.success) {
                console.log("Login successfully:", response.data);
            }
        } catch (error) {
            console.error("Error sending data:", error);
        }
    };

    return (
        <div className="wrapper">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div className="input-box">
                    <input
                        type="text"
                        placeholder='email'
                        value={email}
                        onChange={(e) => setemail(e.target.value)}
                        required
                    />
                    <TiUser className="icon" />
                </div>
                <div className="input-box">
                    <input
                        type="password"
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <TiLockClosed className="icon" />
                </div>
                <div className="remember-forgot">
                    <label><input type="checkbox" />Remember me</label>
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