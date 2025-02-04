import "../../styles/Forms.css"
import { useState } from "react";
import Slider from 'react-slider';
import ToggleButton from '../UI/ToggleButton';

const MIN_AGE = 18;
const MAX_AGE = 100;

const PreferencesForm = () => {



    const [ageRange,setAgeRange] = useState([MIN_AGE,MAX_AGE]);
    const [sameYear, setSameYear] = useState(false);
    
    const onToggleSameYear = (newSameYear) => {
        setSameYear(newSameYear);
        console.log(newSameYear);
    }

    return ( 
    <div className="form-container">
        <h1>About your team</h1>
        <div className="formGroup">
            <label>Your teammates age should be between...</label>
            <label>From {ageRange[0]} to {ageRange[1]}</label>
            <Slider className={"slider"}
                    onChange={setAgeRange}
                    value={ageRange}
                    min={MIN_AGE}
                    max={MAX_AGE}
            />
        </div>

        <div className="formGroup">
            <label>
                Would you like to be paired with people 
                of your same study year or close?
            </label>
            <ToggleButton
                onToggleCallback={onToggleSameYear}
                initialIsToggled={sameYear}
            >
            </ToggleButton>
        </div>


    </div> );
}
 
export default PreferencesForm;