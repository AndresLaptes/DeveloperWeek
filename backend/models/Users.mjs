import mongoose, { model } from "mongoose";
const userSchema = new mongoose.Schema({
    personal: {
        fname: { type: String, required: true },
        lname: { type: String, required: true },
        username: { type: String, required: true },
        email: { type: String, required: true },
        password: { type: String, required: true }
    },
    academic: {
        age: Number,
        studyYear: String,
        university: String,
        introduction: String,
        futurePlans: String,
        friendsRegistered: String,
        preferredLanguages: [{ //array of objects -> level should be deleted (in the react implementation)
            optionName: String,
            level: Number
        }],
        availability: [{ //array of objects -> level should be deleted (in the react implementation)
            optionName: String,
            level: Number
        }]
    },
    tech: {
        interests: [{ 
            optionName: String,
            level: Number
        }],
        preferredRole: String,
        experienceLevel: String,
        hackathonsDone: String,
        objectives: [String],
        favoriteLanguage: String,
        programmingSkills: [{
            optionName: String,
            level: Number
        }]
    }
});

export default mongoose.model("User", userSchema);