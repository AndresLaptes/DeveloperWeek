import "../../styles/Forms.css"
import { useState } from "react";
import Slider from 'react-slider';

const MIN_AGE = 18;
const MAX_AGE = 100;

const PreferencesForm = () => {

    const [ageRange,setAgeRange] = useState([MIN_AGE,MAX_AGE]);

    
    console.log(ageRange);
    return ( 
    <div className="form-container">
        <h1>Shape your team!</h1>
        <div className="formGroup">
            <label>Which age should your teammates be?</label>
            <label>From {ageRange[0]} to {ageRange[1]}</label>
            <Slider className={"slider"}
                    onChange={setAgeRange}
                    value={ageRange}
                    min={MIN_AGE}
                    max={MAX_AGE}
            />
        </div>


    </div> );
}
 
export default PreferencesForm;