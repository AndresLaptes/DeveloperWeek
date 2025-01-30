import React, { useState } from 'react';
import MultipleSelector from './MultipleSelector';
import SingleSelector from './SingleSelector';

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
        <form>
            <div>
                <label>Age:</label>
                <input type="number" name="age" value={formData.age} onChange={handleChange} />
            </div>
            <div>
                <label>Study Year:</label>
                <SingleSelector
                    onChange={(value) => setFormData({ ...formData, studyYear: value })}
                    values={yearList}
                    showSlider={false}
                    selectorName={"Year of Study"}
                />
            </div>
            <div>
                <label>University:</label>
                <SingleSelector
                    onChange={(value) => setFormData({ ...formData, university: value })}
                    values={universitiesList}
                    showSlider={false}
                    selectorName={"University"}
                />
            </div>
            <div>
                <label>Introduction:</label>
                <textarea name="introduction" value={formData.introduction} onChange={handleChange}></textarea>
            </div>
            <div>
                <label>About Your Future:</label>
                <textarea name="futurePlans" value={formData.futurePlans} onChange={handleChange}></textarea>
            </div>
            <div>
                <label>Friends Registered:</label>
                <input type="text" name="friendsRegistered" value={formData.friendsRegistered} onChange={handleChange} />
            </div>
            <div>
                <label>Preferred Language:</label> //TODO
            </div>
            <div>
                <label>Preferred Team Size:</label>
                <input type="number" name="preferredTeamSize" value={formData.preferredTeamSize} onChange={handleChange} />
            </div>
            <div>
                <label>Availability (1, 2 or 3 days):</label>
                <MultipleSelector
                    onChange={(newAvailabilities) => setFormData({ ...formData, availability: newAvailabilities })}
                    showSlider={false}
                    values={availabilityList}
                    selectorName={"Availability"}
                />
            </div>
        </form>
    );
};

export default ParticipantInfoFormAcademic;