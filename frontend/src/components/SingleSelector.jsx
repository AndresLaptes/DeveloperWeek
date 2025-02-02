import { useState } from "react";

const SingleSelector = ({ onChange, showSlider = true, values, selectorName }) => {
    const [selectedValue, setSelectedValue] = useState({ [selectorName]: '', level: 1 });

    const handleFieldChange = (updatedField, newInput) => {
        const updated = { ...selectedValue };
        updated[updatedField] = newInput;
        setSelectedValue(updated);
        onChange(updated);
    };

    return (
        <div>
            <div style={{ marginBottom: "10px" }}>
                <select
                    value={selectedValue[selectorName]}
                    onChange={(e) => handleFieldChange(selectorName, e.target.value)}
                >
                    <option value="">Select a {selectorName}</option>
                    {values.map((val) => (
                        <option key={val} value={val}>
                            {val}
                        </option>
                    ))}
                </select>

                {showSlider && selectedValue[selectorName] && (
                    <>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={selectedValue.level}
                            onChange={(e) => handleFieldChange("level", e.target.value)}
                        />
                        <span>{selectedValue.level}</span>
                    </>
                )}
            </div>
        </div>
    );
};

export default SingleSelector;