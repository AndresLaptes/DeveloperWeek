import PropTypes from 'prop-types';
import React, { useState } from 'react';
import "../../styles/ToggleButton.css"
import { TiTick, TiTimes } from "react-icons/ti";


const ToggleButton = ({onToggleCallback, initialIsToggled, showIcons = true, id = ''}) => {
    const [isToggled, setIsToggled] = useState(initialIsToggled);

    const onToggle = (id)  => {
        setIsToggled(!isToggled);
        onToggleCallback(id,!isToggled);
    }

    return ( 
        <button
            id = {id}
            className={`toggle-btn ${ isToggled ? 'toggled' : ''}`}
            onClick={()  => {onToggle(id)}}
        >
          <div className="thumb"></div>
          {
            showIcons &&
            <div className="icon">
              { isToggled 
                ? <TiTick></TiTick>
                : <TiTimes></TiTimes>
              }
          </div>
          }
        </button>
     );
}


ToggleButton.propTypes = {
    onToggleCallback: PropTypes.func.isRequired,
    initialIsToggled: PropTypes.bool,
    showIcons: PropTypes.bool,
    id: PropTypes.string,
};


export default ToggleButton;

