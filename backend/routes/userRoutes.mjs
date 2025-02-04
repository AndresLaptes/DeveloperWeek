import express from "express";
/**
 * @typedef {import("../models/User.js").default} UserModel
 */
import { UserRepository } from "../repositories/userRepository.mjs";

const userRouter = express.Router();


userRouter.post("/register", async (req, res) => {
    const {username, email, password} = req.body.personal;
    const {academic, tech} = req.body;
    console.log({username, email, password});
    try {
        const idOfCreated = await UserRepository.createUser({username,email,password});
        const linkedWithInfo = await UserRepository.associateUserInfo(idOfCreated,{academic, tech});
        res.send(idOfCreated);
    }
    catch (error) {
        console.error("Registration error:", error);
        return res.status(500).json({ 
            success: false,
            message: "Error registering user",
        });}
});

userRouter.post("/login", async (req, res) => {
    const {email, password} = req.body;
    try {
        const userLogged = await UserRepository.loginUser({email,password});
        console.log(userLogged);
        res.status(200).json({succes: true, message: "Login correct"});
    }
    catch (error) {
        console.error("Login error: ", error)
        res.status(400).json({succes: false, message: "Error in login"});
    }
})

export default userRouter;