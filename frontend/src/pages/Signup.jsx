import { useState } from "react";
import PersonalInfoForm from "../components/Forms/PersonalInfoForm";
import ParticipantInfoFormAcademic from "../components/Forms/ParticipantInfoFormAcademic";
import ParticipantInfoFormTech from "../components/Forms/ParticipantInfoFormTech";

import "../styles/SignUp.css"

const TOTAL_PAGES = 3;

//TODO -> MAKE SUBMIT BUTTON APPEAR ONLY WHEN ALL FIELDS FROM ALL FORMS ARE FILLED OR VALIDATED 
//TODO -> MAKE PROGRESS BAR (EACH 1/3 IS WHEN ONE FORM GETS COMPLETED)
const Signup = () => {
    const [currentPage, setPage] = useState(0);
    const [formData, setFormData] = useState({
        personal: {
            fname: '',
            lname: '',
            username: '',
            email: '',
            password: ''
        },
        academic: {
            age: '',
            studyYear: '',
            university: '',
            introduction: '',
            futurePlans: '',
            friendsRegistered: '',
            preferredLanguages: [],
            availability: [],
        },
        tech: {
            interests: [],
            preferredRole: '',
            experienceLevel: '',
            hackathonsDone: '',
            objectives: [],
            favoriteLanguage: '',
            programmingSkills: []
        }
    });

    console.log(formData);

    const updateAcademicForm = (academicData) => {
        setFormData(prev => ({
            ...prev,
            academic: { ...prev.academic, ...academicData }
        }));
    };

    const updateTechForm = (techData) => {
        setFormData(prev => ({
            ...prev,
            tech: { ...prev.tech, ...techData }
        }));
    };

    const updatePersonalForm = (personalData) => {
        setFormData(prev => ({
            ...prev,
            personal: {...prev.personal, ...personalData}
        }));
    }

    const handleSubmit = () => {
        console.log('Combined form data:', formData);
        //backend code to send to BD
    };

    return (
        <div className="signUpPage">
            <div className="signUpContainer">
                {currentPage + 1 === 1 ? (
                    <PersonalInfoForm  
                        formData={formData.personal} 
                        setFormData={updatePersonalForm} 
                    />
                ) : currentPage === 2 ? (
                    <ParticipantInfoFormAcademic 
                        formData={formData.academic} 
                        setFormData={updateAcademicForm} 
                    />
                ) : (
                    <ParticipantInfoFormTech 
                        formData={formData.tech} 
                        setFormData={updateTechForm} 
                    />
                )}
                <div className="FormButtons">
                        <button className="formBtn"  disabled = {currentPage === 0} onClick={() => setPage((currentPage - 1) % 3)}>Go Back</button>
                        <button className="formBtn"onClick={ () => setPage((currentPage + 1) % 3)}>Go Next</button>
                </div>
                <button type="submit" onClick={handleSubmit}>Submit</button>
                <p>{currentPage + 1} / {TOTAL_PAGES}</p>
            </div>
        </div>
    );
};

export default Signup;