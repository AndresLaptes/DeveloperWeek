import express from "express";
/**
 * @typedef {import("../models/User.js").default} UserModel
 */
import { UserRepository } from "../repositories/userRepository.mjs";

const userRouter = express.Router();


userRouter.post("/register", async (req, res) => {
    const {username, email, password} = req.body.personal;
    console.log({username, email, password});
    try {
        const emailOfCreated = await UserRepository.createUser({username,email,password});
        res.send(emailOfCreated);
    }
    catch (error) {
        console.error("Registration error:", error);
        return res.status(500).json({ 
            success: false,
            message: "Error registering user",
        });}
})

export default userRouter;