import { useEffect, useState } from "react";
import { animate, useMotionValue, motion, useTransform } from "framer-motion";
import FloatingCards from "../components/FloatingContainer";
import CustomButton from "../components/CustomButton";
import "../styles/Home.css";


const PreferencesForm = () => {
    return (<p>form</p>)
};
const FloatingInfo = () => {
    return (<p>info</p>)
};

//code from motion docs, example in counter section !!!!
//my idea is this to be changed only when page is reloaded -> we don't access that much the DB
const Counter = ({nTeams}) => {
    const count = useMotionValue(0);
    const rounded = useTransform(() => Math.round(count.get()));
    useEffect(() => {
        const controls = animate(count, nTeams, {duration: 4.5})
        return () => controls.stop();
    }, []);
    return <motion.pre className="teamCounter">{rounded}</motion.pre>
}

const Home = ({props}) => {
    const [displayForm, setDisplayForm] = useState(false); //false -> floating info, true -> form for searching team
    return (
        <>
            <div className="homeContainer">
                <div className="homeLeft">
                    <CustomButton
                        className="matchTeamButton"
                        text="Match with a team"
                        variant="primary"
                        size="xl"
                        onClick={setDisplayForm}
                        disabled = {false}
                     />
                    <p>or</p>
                    <CustomButton
                        className="createButton"
                        text="CREATE ONE"
                        variant="primary"
                        size="large"
                        onClick={setDisplayForm}
                        disabled = {false}
                        />
                    <div className= "teamCounterContainer">
                        <p>Current Teams in X Hackathon</p>
                        <Counter nTeams= {100}/>
                    </div>
                </div>
                <div className="homeRight">
                    {displayForm ? <PreferencesForm /> : <FloatingCards/>}
                </div>
            </div>
        </>
    )
}

export default Home;