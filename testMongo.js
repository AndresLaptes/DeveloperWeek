const { MongoClient } = require("mongodb");

// Replace with your actual username and password
const uri = "mongodb+srv://omar_user:123@developerweek.tl23p.mongodb.net/?retryWrites=true&w=majority&appName=DeveloperWeek";

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


testConnection();
fetchDocuments();
