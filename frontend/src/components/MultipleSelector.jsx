import { useState } from "react";

const MultipleSelector = ({ onChange, showSlider = true, values, selectorName }) => {
    const [selectedValues, setSelectedValues] = useState([]);
    const [selectableValues, setSelectableValues] = useState(values);

    const handleFieldSelected = (updatedField, newInput) => {
        setSelectableValues(prevValues => prevValues.filter(value => value != newInput));
        setSelectedValues([...selectedValues, newInput]);
        onChange([...selectedValues,newInput]);
    };
    
    const handleRemoveValue = (removedValue) => {
        setSelectedValues( prevSelected => {
            const updated = prevSelected.filter(value => value !== removedValue);
            onChange(updated);
            return updated;
        });

        setSelectableValues(prevValues => {
            const prevIndex = values.indexOf(removedValue);
            const updated = [...prevValues];
            updated.splice(prevIndex, 0, removedValue);
            return updated;
        });
    };
  
    return (
        <div>
            {selectedValues.map((value, index) => (
                <div key={index} style={{ marginBottom: "10px" }}>
                    <p>{value}</p>
                    <button type="button" onClick={() => handleRemoveValue(value)}>
                        ❌ Remove
                    </button>
                </div>
            ))}

            <select
                        value="test"
                        onChange={(e) => handleFieldSelected(selectorName, e.target.value)}
            >
                        <option value="">➕ Add {selectorName}</option>
                        {selectableValues.map((val) => (
                            <option key={val} value={val}>
                                {val}
                            </option>
                        ))}
            </select>
        </div>
    );
};

export default MultipleSelector;