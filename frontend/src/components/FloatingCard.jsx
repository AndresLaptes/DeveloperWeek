import { animate, color, motion } from "framer-motion"
import "../styles/FloatingCard.css"
const FloatingCard = ({text, style, animate}) => {
    return (
        <motion.div className="floatingCard"
            animate = {animate}
            transition={{ duration: 0.8, ease: "easeInOut", delay: 0.1}}
            style={style}
            initial={{ opacity: 0, scale: 0 }}>
            <p>
                {text}
            </p>
            <span>OMG</span>
        </motion.div>
    )
}

export default FloatingCard;