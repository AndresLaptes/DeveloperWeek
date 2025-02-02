import express from "express";
import cors from "cors";

const app = express();
const port = 3000;

//allow json data from http reqs
app.use(express.json());

//allow cross origin resources  ( since front end and backend run in different servers )
app.use(cors());

app.get("/", (req, res) => {
    res.send("Didac");
});


app.post("/save-data", (req, res) => {
    console.log("Received form data:", req.body);
    res.json({ message: "Data received successfully" }); //this shows up on the front end console
});

//we put it on to listen on the indicated port
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
