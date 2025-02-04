import PropTypes from 'prop-types';
import React, { useState } from 'react';
import "../../styles/ToggleButton.css"
import { TiTick, TiTimes } from "react-icons/ti";


const ToggleButton = ({onToggleCallback, initialIsToggled, showIcons}) => {
    const [isToggled, setIsToggled] = useState(initialIsToggled);

    const onToggle = ()  => {
        setIsToggled(!isToggled);
        onToggleCallback(!isToggled);
    }

    return ( 
        <button
            className={`toggle-btn ${ isToggled ? 'toggled' : ''}`}
            onClick={onToggle}
        >
          <div className="thumb"></div>
          <div className="icon">
              { isToggled 
                ? <TiTick></TiTick>
                : <TiTimes></TiTimes>
              }
          </div>
        </button>
     );
}


ToggleButton.propTypes = {
    onToggleCallback: PropTypes.func.isRequired,
    initialIsToggled: PropTypes.bool,
    showIcons: PropTypes.bool,
};


export default ToggleButton;

