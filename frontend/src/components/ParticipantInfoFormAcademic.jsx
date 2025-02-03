import React, { useState } from 'react';
import MultipleSelector from './MultipleSelector';
import SingleSelector from './SingleSelector';

import "../styles/Forms.css"

const languagesList = ["Spanish", "English"];



const availabilityList = ["saturday morning", "saturday afternoon", "saturday night", "sunday morning", "sunday afternoon"];

const universitiesList = ["UPC", "UAB"];

const yearList = ["first year", "second year", "third year", "fourth year", "master", "phD"];

const ParticipantInfoFormAcademic = ({formData, setFormData}) => {

    console.log(formData);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };
      
    return (
        <div className='form-container'>
            <h2>Your academic information</h2>
                <div className='formGroupContainer'>
                    <div className="formGroup">
                        <label>Age:</label>
                        <input type="number" name="age" value={formData.age} onChange={handleChange} />
                    </div>
                    <div className="formGroup">
                        <label>Introduction:</label>
                        <textarea name="introduction" value={formData.introduction} onChange={handleChange}></textarea>
                    </div>
                    <div className="formGroup">
                        <label>About Your Future:</label>
                        <textarea name="futurePlans" value={formData.futurePlans} onChange={handleChange}></textarea>
                    </div>
                    <div className="formGroup">
                        <label>Friends Registered:</label>
                        <input type="text" name="friendsRegistered" value={formData.friendsRegistered} onChange={handleChange} />
                    </div>
                    <div className="formGroup">
                        <label>Preferred Team Size:</label>
                        <input type="number" name="preferredTeamSize" value={formData.preferredTeamSize} onChange={handleChange} />
                    </div>
                    <div className="formGroup">
                        <label>Preferred Language:</label>
                        <MultipleSelector
                            onChange={(newLanguages) => setFormData({ ...formData, preferredLanguages: newLanguages })}
                            showSlider={false}
                            values={languagesList}
                            selectorName={"Preferred Languages"}
                        />
                    </div>
                    <div className="formGroup">
                        <label>Study Year:</label>
                        <SingleSelector
                            onChange={(value) => setFormData({ ...formData, studyYear: value })}
                            values={yearList}
                            selectorName={"Year of Study"}
                        />
                    </div>
                    <div className="formGroup">
                        <label>University:</label>
                        <SingleSelector
                            onChange={(value) => setFormData({ ...formData, university: value })}
                            values={universitiesList}
                            selectorName={"University"}
                        />
                    </div>
                    <div className="formGroup">
                        <label>Availability (1, 2 or 3 days):</label>
                        <MultipleSelector
                            onChange={(newAvailabilities) => setFormData({ ...formData, availability: newAvailabilities })}
                            showSlider={false}
                            values={availabilityList}
                            selectorName={"Availability"}
                        />
                    </div>
                </div>
        </div>
    );
};

export default ParticipantInfoFormAcademic;