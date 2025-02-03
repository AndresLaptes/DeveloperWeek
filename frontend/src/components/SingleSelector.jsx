import { useState } from "react";

const SingleSelector = ({ onChange, values, selectorName }) => {
    const handleChange = (e) => {
        const value = e.target.value;
        if (!value) return;
        onChange(value);
    };

    return (
        <div className="singleSelector-container">
            <select 
                className="selector-dropdown"
                onChange={handleChange}
                defaultValue=""
            >
                <option value="">Select {selectorName}</option>
                {values.map((value) => (
                    <option key={value} value={value}>
                        {value}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default SingleSelector;