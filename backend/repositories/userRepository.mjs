import mongoose, { model } from "mongoose";
import bcrypt from "bcrypt";

const userSchema = new mongoose.Schema({
    username: { type: String, required: true },
    password: { type: String, required: true },
    email: { type: String, required: true }
});

const userInfoSchema = new mongoose.Schema({
    user: {type: mongoose.Schema.Types.ObjectId, ref: 'User'},
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

const User = mongoose.model('User',userSchema);
const UserInfo = mongoose.model('UserInfo',userInfoSchema);

export class UserRepository {
    //This is for creating the user, without all of its info (academic and tech)
    static async createUser({username, email, password}) {
        Validation.validateUser(username);
        Validation.validateEmail(email);
        
        //check that user doesnt already exist by email
        const found = await User.findOne({email: email});
        console.log("Found user:", found); // Debug log

        if (found) throw new Error('email already in use');

        const hashedPassword = await bcrypt.hash(password,10);
        const user = new User({
            username,
            email,
            password: hashedPassword
        });

        await user.save();
        return email;
    }

    static async associateUserInfo({academic, tech}) {

    }
}

class Validation {
    static validateUser(username) {
        if (typeof username !== 'string') throw new Error ('username must be a string')
        if (username.length < 3) throw new Error ('username must be at least 3 characters long'); //implement in front too
    }

    static validateEmail(email) {
        if (typeof email !== 'string') throw new Error ('email must be a string');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //stack overflow
        if (!emailRegex.test(email)) throw new Error('Invalid email format');
    }

}