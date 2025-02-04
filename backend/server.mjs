import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import dotenv from 'dotenv';
import userRouter from "./routes/userRoutes.mjs";
import cookieParser from "cookie-parser";

dotenv.config();

const app = express();
const port = 3000;
//allow json data from http reqs
app.use(express.json());
app.use(cookieParser());

//allow cross origin resources  ( since front end and backend run in different servers )
app.use(cors({
    origin: 'http://localhost:5173',
    credentials: true,
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

mongoose.connect(process.env.MONGO_URI).then(console.log("Connected to mongoDb"));

app.get("/", (req, res) => {
    res.send("Didac");
});

app.use("/user",userRouter);

app.post("/save-data", (req, res) => {
    console.log("Received form data:", req.body);
    res.json({ message: "Data received successfully" }); //this shows up on the front end console
});

//we put it on to listen on the indicated port
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
