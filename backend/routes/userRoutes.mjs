import express from "express";
/**
 * @typedef {import("../models/User.js").default} UserModel
 */
import User from "../models/Users.mjs"; // Import User model

const userRouter = express.Router();


userRouter.post("/register", async (req, res) => {
    try {
        const {personal, academic, tech} = req.body;

        const userExists = await User.findOne({ "personal.email": personal.email });
        if (userExists) {
            return res.status(400).json({message: "Email already in use"});
        }

        const newUser = User({personal, academic, tech});
        await newUser.save();        
        return res.status(200).json({succes: true, message: "User saved"});
    }
    catch (error) {
        console.error("Registration error:", error);
        return res.status(500).json({ 
            success: false,
            message: "Error registering user",
            error: error.message 
        });    }
})

export default userRouter;