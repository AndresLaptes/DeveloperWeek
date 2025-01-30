import { useState } from "react";
import PersonalInfoForm from "../components/PersonalInfoForm";
import ParticipantInfoFormAcademic from "../components/ParticipantInfoFormAcademic";
import ParticipantInfoFormTech from "../components/ParticipantInfoFormTech";
const TOTAL_PAGES = 3;

const Signup = () => {
    const [currentPage, setPage] = useState(1);
    const [formData, setFormData] = useState({
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
            {currentPage === 1 ? (
                <PersonalInfoForm  //TODO
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
            <div className="preferences">
            </div>
            <div className="FormButtons">
                    <button className="formBtn" onClick={() => setPage(currentPage - 1)}>go back</button>
                    <button className="formBtn" onClick={ () => setPage(currentPage + 1)}>go next</button>
            </div>
            <button type="submit" onClick={handleSubmit}>Submit</button>
            <p>{currentPage} / {TOTAL_PAGES}</p>
        </div>
    );
};

export default Signup;