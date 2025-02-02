import { useState } from "react";
import "../styles/MultipleSelector.css"
//value = {optionName, level of skill} -> level of skill by default is 1, but it can be modified for those with showSlider on true
const MultipleSelector = ({ onChange, showSlider = true, values, selectorName }) => {
    const [selectedValues, setSelectedValues] = useState([]);
    const [selectableValues, setSelectableValues] = useState(
        values.map(value => ({optionName: value}))
    );

    const handleFieldSelected = (newInput) => {
        if (!newInput) return; 
        
        setSelectableValues(prevValues => prevValues.filter(value => value.optionName !== newInput));
        const added = { optionName: newInput, level: 1 };
        setSelectedValues(prev => [...prev, added]);
        onChange([...selectedValues, added]);
    };
    
    const handleLevelChange = (index, newLevel) => {
        const updated = selectedValues.map((value, i) => {
            if (index === i) return {...value, level: parseInt(newLevel)};
            return value;
        });
        setSelectedValues(updated);
        onChange(updated);
    }

    const handleRemoveValue = (removedValue) => { //TODO FIX -> CONSOLE ERROR 
        setSelectedValues( prevSelected => {
            const updated = prevSelected.filter(value => value.optionName !== removedValue.optionName); //since now we have 2 keys
            onChange(updated);
            return updated;
        });

        setSelectableValues(prevValues => {
            const valueToAdd = { optionName: removedValue.optionName };
            const sortedValues = [...prevValues, valueToAdd]
                .sort((a, b) => values.indexOf(a.optionName) - values.indexOf(b.optionName));
            return sortedValues;
        });
    };
  
    return (
        <div className="multipleSelector-container">
            <div className="selectedItems">
                {selectedValues.map((value, index) => (
                    <div key={index} className="selected-item">
                        <div>
                            <p>{value.optionName}</p>
                            {showSlider && (
                                <div className="slider-container">
                                    <input
                                        type="range"
                                        min="1"
                                        max="10"
                                        value={value.level}
                                        onChange={(e) => handleLevelChange(index, e.target.value)}
                                    />
                                    <span>{value.level}</span>
                                </div>
                            )}
                        </div>
                        <button className="remove-btn" type="button" onClick={() => handleRemoveValue(value)}>
                            ❌ Remove
                        </button>
                    </div>
                ))}
            </div>
            <select     className="selector-dropdown"
                        value=""
                        onChange={(e) => handleFieldSelected(e.target.value)}
            >
                        <option value="">➕ Add {selectorName}</option>
                        {selectableValues.map((val) => (
                            <option key={val.optionName} value={val.optionName}>
                                {val.optionName}
                            </option>
                        ))}
            </select>
        </div>
    );
};

export default MultipleSelector;