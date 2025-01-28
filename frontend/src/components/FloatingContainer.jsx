import { useState } from "react";
import { useEffect } from "react";
import FloatingCard from "./FloatingCard";

import "../styles/FloatingCards.css";

const cards = [
    {text: "Trending Hackathons", color: "black"},
    {text: "Partners", color: "wheat"},
    {text: "This Hackathon", color: "lightblue"}
];

const FloatingContainer = () => {
    useEffect(() => {
        const interval = setInterval(() => {
            setPositions((prev) => [prev[2], prev[0], prev[1]]);
        }, 3000); //each 2 seconds, we alterate the positions moving 1 pos to the right

        return () => clearInterval(interval);
    }, []);

    const [positions, setPositions] = useState([0,1,2]); //Initial: card 0 in pos 0, card 1 in 1, card 2 in 2
  

    const getXfromIndex = (index) => {
        switch (positions[index]) {
            case 0:
                return 0; //card has to go to pos 0 -> x: 0
            case 1:
                return 250;
            case 2:
                return -250;
            default:
                break;
        }
    }

    const getYfromIndex = (index) => {
        switch (positions[index]) {
            case 0:
                return -250; //card has to go to pos 0 -> y -> -200 (from figma img and didac verison !!)
            case 1:
                return  150;
            case 2:
                return 0;
            default:
                break;
        }
    }
  
    return (
        <div className="floatingContainer">
            {cards.map((value, index) => (
                <FloatingCard
                    key={value.text}
                    text={value.text}
                    style={{backgroundColor : value.color}}
                    animate={{
                        x : getXfromIndex(index),
                        y : getYfromIndex(index),
                        rotate: positions[index] === 1 ? 6 : positions[index] === 2 ? -6 : 0,  // Slight rotation
                        scale: positions[index] === 1 ? 1.2 : 1, //this should be changed, maybe top one bigger
                        zIndex: positions[index] === 1 ? 10 : 5,
                        opacity: 1 //needed since when it is initialized it starts from 0
                    }}
                />
                ))}
        </div>
    )
}

export default FloatingContainer;