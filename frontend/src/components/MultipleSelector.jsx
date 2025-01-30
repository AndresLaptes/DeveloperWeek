import { useState } from "react";

const MultipleSelector = ({ onChange, showSlider = true, values, selectorName }) => {
    const [selectedValues, setSelectedValues] = useState([]);
  
    const handleAddValue = () => {
        setSelectedValues([...selectedValues, { [selectorName]: '', level: 1 }]);
    };

    const handleFieldChange = (index, updatedField, newInput) => {
        if (updatedField === selectorName) {
            if (selectedValues.some((item, i) => i !== index && item[selectorName] === newInput)) {
                alert(`"${newInput}" already selected`); //should be done using a state of those not added already
                return;
            }
        }
        const updated = [...selectedValues];
        updated[index][updatedField] = newInput;
        setSelectedValues(updated);
        onChange(updated);
    };
    
    const handleRemoveValue = (removeIndex) => {
        const updated = selectedValues.filter((_, index) => index !== removeIndex);
        setSelectedValues(updated);
        onChange(updated);
    };
  
    return (
        <div>
            {selectedValues.map((value, index) => (
                <div key={index} style={{ marginBottom: "10px" }}>
                    <select
                        value={value[selectorName]}
                        onChange={(e) => handleFieldChange(index, selectorName, e.target.value)}
                    >
                        <option value="">Select a {selectorName}</option>
                        {values.map((val) => (
                            <option key={val} value={val}>
                                {val}
                            </option>
                        ))}
                    </select>
    
                    {showSlider && value[selectorName] && (
                        <>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={value.level}
                                onChange={(e) => handleFieldChange(index, "level", e.target.value)}
                            />
                            <span>{value.level}</span>
                        </>
                    )}
    
                    <button type="button" onClick={() => handleRemoveValue(index)}>
                        ❌ Remove
                    </button>
                </div>
            ))}
    
            <button type="button" onClick={handleAddValue}>
                ➕ Add {selectorName}
            </button>
        </div>
    );
};

export default MultipleSelector;