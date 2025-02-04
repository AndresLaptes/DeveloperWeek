import "../../styles/Forms.css"
import { useState } from "react";
import PropTypes from 'prop-types';
import ToggleButton from '../UI/ToggleButton';

const MIN_AGE = 18;
const MAX_AGE = 100;

const MINIMIZE = -1;
const MAXIMIZE = 1;

const POSITION = {
    studyYear: '1',
    uni: '2',
    expLvl: '5',
    hackathons: '6',
    languages: '10',
    friends: '11'
};


const PreferencesForm = ({handleSubmit}) => {

    const [preferenceVector, setPreferenceVector] = useState(
        [1,-1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1]);
    

    const onToggleValue = (toggledValue, newValue) => {
        const newVector = [...preferenceVector]
        newVector[POSITION[toggledValue]] = ( newValue ? MAXIMIZE : MINIMIZE);
        setPreferenceVector(newVector);
    }

    return ( 
    <div className="form-container">
        <h1>About your team</h1>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
                STUDY YEAR
            </label>
            <ToggleButton
                id={"studyYear"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
                UNI
            </label>
            <ToggleButton
                id={"uni"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
               EXP LEVEL
            </label>
            <ToggleButton
                id={"expLvl"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
                SIMILAR NUMBER OF HACKATHONS
            </label>
            <ToggleButton
                id={"hackathons"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
                INTERNATIONAL
            </label>
            <ToggleButton   
                id={"languages"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <div className={`formGroup ${'horizontal'}`}>
            <label>
                FRIENDS
            </label>
            <ToggleButton
                id={"friends"}
                onToggleCallback={onToggleValue}
                initialIsToggled={false}
            >
            </ToggleButton>
        </div>

        <button
            onClick={handleSubmit}
        >
            Match!
        </button>


    </div> );
}

PreferencesForm.propTypes = {
    handleSubmit: PropTypes.func.isRequired,
}


export default PreferencesForm;