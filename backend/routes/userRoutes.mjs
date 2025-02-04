import express from "express";
import { UserRepository } from "../repositories/userRepository.mjs";
import jwt from 'jsonwebtoken'
import dotenv from 'dotenv';
import cookieParser from "cookie-parser";

dotenv.config();



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
        const token = jwt.sign({id: userLogged._id, email: userLogged.email}, process.env.SECRET_JWT_WORD, {
            expiresIn: '1h'
        });
        console.log(userLogged);
        console.log(token);
        res.cookie('access_token', token,  {
            httpOnly: true,
            secure: true,
            sameSite: 'lax',
        }).status(200).json({success: true, message: "Login correct"});
    }
    catch (error) {
        console.error("Login error: ", error)
        res.status(400).json({succes: false, message: "Error in login"});
    }
})

export default userRouter;