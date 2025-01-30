import React from 'react';
import MultipleSelector from './MultipleSelector';
import SingleSelector from './SingleSelector';

const languagesList = [
    "Python", "JavaScript", "Java", "C", "C++", "C#", "Ruby",
    "PHP", "Swift", "Kotlin", "TypeScript", "Go", "Rust"
];

const interestsList = ["health", "devops", "AR"];

const objectivesList = [] //TODO, multiple selector


const ParticipantInfoFormTech = ({ formData, setFormData }) => {
    const handleInputChange = (name, value) => {
        setFormData({
            [name]: value
        });
    };

    const handleProgrammingSkillsChange = (skills) => {
        setFormData({
            programmingSkills: skills
        });
    };

    const handleInterestsChange = (interests) => {
        setFormData({
            interests: interests
        });
    };
      
    return (
        <div>
            <div>
                <label>Interests:</label>
                <MultipleSelector
                    onChange={handleInterestsChange}
                    values={interestsList}
                    showSlider={false}
                    selectorName="Interest"
                />
            </div>
            <div>
                <label>Programming Skills:</label>
                <MultipleSelector
                    onChange={handleProgrammingSkillsChange}
                    values={languagesList}
                    showSlider={true}
                    selectorName="Programming Skill"
                />
            </div>
            <div>
                <label>Preferred Role in a Team:</label>
                <input 
                    type="text" 
                    value={formData.preferredRole || ''}
                    onChange={(e) => handleInputChange('preferredRole', e.target.value)}
                />
            </div>
            <div>
                <label>Experience Level:</label>
                <input 
                    type="number" 
                    value={formData.experienceLevel || ''}
                    onChange={(e) => handleInputChange('experienceLevel', e.target.value)}
                />
            </div>
            <div>
                <label>Hackathons Done:</label>
                <input 
                    type="number" 
                    value={formData.hackathonsDone || ''}
                    onChange={(e) => handleInputChange('hackathonsDone', e.target.value)}
                />
            </div>
            <div>
                <label>Objectives:</label>
                <input 
                    type="text"  //TODO -> CHANGE TO MUTLIPLE SELECTOR
                    value={formData.objectives || ''}
                    onChange={(e) => handleInputChange('objectives', e.target.value)}
                />
            </div>
            <div>
                <label>Favorite Language:</label>
                <input 
                    type="text"  //TODO -> CHANGE TO SINGLE SELECTOR WITH THE SAMES AS THE PROGRAMMING SKILLS
                    value={formData.favoriteLanguage || ''}
                    onChange={(e) => handleInputChange('favoriteLanguage', e.target.value)}
                />
            </div>
        </div>
    );
};

export default ParticipantInfoFormTech;