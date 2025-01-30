const { MongoClient } = require("mongodb");
const { exec } = require("child_process");
const fs = require('fs');

// Replace with your actual username and password
const uri = "mongodb+srv://omar_user:123@developerweek.tl23p.mongodb.net/?retryWrites=true&w=majority&appName=DeveloperWeek";

// Function to run the Python script and perform model inference
async function runModel(inputText) {
    try {
        return new Promise((resolve, reject) => {
            exec(`python3 tokenizer.py "${inputText}"`, (error, stdout, stderr) => {
                if (error) {
                    reject(`❌ Error: ${error.message}`);
                    return;
                }
                if (stderr) {
                    reject(`❌ stderr: ${stderr}`);
                    return;
                }

                const output = JSON.parse(stdout);  // Parse the model result
                resolve(output.result);
            });
        });
    } catch (error) {
        console.error("❌ Error running model:", error);
        return null;
    }
}


// Fetch documents from MongoDB and update them
async function updateDocuments() {
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        await client.connect();
        console.log("✅ Successfully connected to MongoDB!");

        const database = client.db("example_db");
        const collection = database.collection("example_db");

        const documents = await collection.find().limit(10).toArray();

        for (const doc of documents) {
            console.log(`Processing document ${doc._id}...`);
            if (doc.objective) {
                
                const modelResult = await runModel(doc.objective);

                if (modelResult !== null) {
                    await collection.updateOne(
                        { _id: doc._id },
                        { $set: { ember_obj: modelResult } }
                    );
                    console.log(`✅ Updated document ${doc._id} with ember_obj`);
                } else {
                    console.log(`⚠️ Skipped document ${doc._id} due to model error.`);
                }
            }

            if(doc.introduction) {
                const modelResult = await runModel(doc.introduction);
                if (modelResult !== null) {
                    await collection.updateOne(
                        { _id: doc._id },
                        { $set: { ember_intr: modelResult } }
                    );
                    console.log(`✅ Updated document ${doc._id} with ember_intr`);
                } else {
                    console.log(`⚠️ Skipped document ${doc._id} due to model error.`);
                }
            }

            if(doc.future_excitement) {
                const modelResult = await runModel(doc.future_excitement);
                if (modelResult !== null) {
                    await collection.updateOne(
                        { _id: doc._id },
                        { $set: { ember_excitement: modelResult } }
                    );
                    console.log(`✅ Updated document ${doc._id} with ember_excitement`);
                } else {
                    console.log(`⚠️ Skipped document ${doc._id} due to model error.`);
                }
            }

            if(doc.fun_fact) {
                const modelResult = await runModel(doc.fun_fact);
                if (modelResult !== null) {
                    await collection.updateOne(
                        { _id: doc._id },
                        { $set: { ember_fact: modelResult } }
                    );
                    console.log(`✅ Updated document ${doc._id} with ember_fact`);
                } else {
                    console.log(`⚠️ Skipped document ${doc._id} due to model error.`);
                }
            }
        }
    } catch (error) {
        console.error("❌ Error updating documents:", error);
    } finally {
        await client.close();
    }
}

async function testConnection() {
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        // Connect to the MongoDB cluster
        await client.connect();

        // Check connection
        await client.db("admin").command({ ping: 1 });
        console.log("✅ Successfully connected to MongoDB!");
    } catch (error) {
        console.error("❌ Connection failed:", error);
    } finally {
        await client.close();
    }
}


async function fetchDocuments() {
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        await client.connect();
        console.log("✅ Successfully connected to MongoDB!");

        // Select the database and collection
        const database = client.db("example_db");  // Replace with your actual DB name
        const collection = database.collection("example_db");  // Replace with your collection name

        // Fetch documents (limit 10 for testing)
        const documents = await collection.find().limit(10).toArray();

        console.log("📜 Retrieved Documents:");
        console.log(documents);
    } catch (error) {
        console.error("❌ Error retrieving documents:", error);
    } finally {
        await client.close();
    }
}


async function addParticipants(jsonFile, mongoUri, dbName, collectionName) {
    const client = new MongoClient(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true });
    try {
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection(collectionName);

        // Leer JSON
        const data = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
        const participants = Array.isArray(data) ? data : []; 

        for (const participant of participants) {
            if (!participant.id) continue;  

            const existingParticipant = await collection.findOne({ id: participant.id });
            if (!existingParticipant) {
                participant.ember_obj = participant.objective ? await runModel(participant.objective) || 0 : 0;
                participant.ember_intr = participant.introduction ? await runModel(participant.introduction) || 0 : 0;
                participant.ember_fact = participant.fun_fact ? await runModel(participant.fun_fact) || 0 : 0;
                participant.ember_excitement = participant.future_excitement ? await runModel(participant.future_excitement) || 0 : 0;

                await collection.insertOne(participant);
                console.log(`✅ Added participant: ${participant.name}`);
            } else {
                console.log(`⚠️ Participant ${participant.name} already exists.`);
            }
        }
    } catch (error) {
        console.error("❌ Error processing participants:", error);
    } finally {
        await client.close();
        console.log("✅ Done.");
    }
}



// testConnection();
// fetchDocuments();
//updateDocuments();
//addParticipants("datathon_participants.json", uri, "example_db", "example_db");