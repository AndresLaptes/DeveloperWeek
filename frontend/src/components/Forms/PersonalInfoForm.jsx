import React from 'react';
import "../../styles/Forms.css"

const PersonalInfoForm = ({formData, setFormData}) => {
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            [name]: value
        });
    };

    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    return (
        <div className="form-container">
            <h2>Personal Information</h2>
            <div className='formGroupContainer'>
                <div className="formGroup">
                    <label htmlFor="fname">First Name:</label>
                    <input
                        type="text"
                        id="fname"
                        name="fname"
                        value={formData.fname || ''}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="formGroup">
                    <label htmlFor="lname">Last Name:</label>
                    <input
                        type="text"
                        id="lname"
                        name="lname"
                        value={formData.lname || ''}
                        onChange={handleChange}
                        required
                    />
                </div>


                <div className="formGroup">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email || ''}
                        onChange={handleChange}
                        required
                        pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$" //regex from StackOverflow
                        className={formData.email && !isValidEmail(formData.email) ? 'invalid' : ''}
                    />
                    {formData.email && !isValidEmail(formData.email) && 
                        <span className="error-message">Please enter a valid email address</span>
                    }
                </div>

                <div className="formGroup">
                    <label htmlFor="password">Password:</label>
                    <div className="password-input-container">
                        <input
                            type={"password"}
                            id="password"
                            name="password"
                            value={formData.password || ''}
                            onChange={handleChange}
                            required
                            
                        />
                    </div>
                </div>

                <div className="formGroup">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username || ''}
                        onChange={handleChange}
                        required
                    />
                </div>
            </div>
        </div>
    );
};

export default PersonalInfoForm;