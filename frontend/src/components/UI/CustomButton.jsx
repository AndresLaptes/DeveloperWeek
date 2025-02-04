import React from 'react';
import PropTypes from 'prop-types';
import "../../styles/CustomButton.css"
const CustomButton = ({text, onClick, variant = 'primary', size = 'medium', disabled = false, className = '',}) => {
    const baseClass = `custom-button ${variant} ${size} ${className}`; //used to change styles based on it
    return (
        <button 
            className={baseClass}
            onClick={onClick}
            disabled={disabled}>
            {text}
        </button>
    );
};

CustomButton.propTypes = { // check restrictions of the props
    text: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary']),
    size: PropTypes.oneOf(['small', 'medium', 'large' , 'xl']), 
    disabled: PropTypes.bool,
    className: PropTypes.string,
};

export default CustomButton;