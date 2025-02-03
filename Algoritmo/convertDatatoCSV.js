const { MongoClient } = require("mongodb");
const fs = require("fs");

// Configurar la conexión a MongoDB
const uri = "mongodb+srv://omar_user:123@developerweek.tl23p.mongodb.net/?retryWrites=true&w=majority&appName=DeveloperWeek";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function exportToJSON() {
    try {
        await client.connect();
        console.log("✅ Conectado a MongoDB");

        const database = client.db("example_db");  // Reemplaza con el nombre de tu BD
        const collection = database.collection("example_db");  // Reemplaza con el nombre de tu colección

        // Obtener todos los documentos excluyendo _id
        const documents = await collection.find({}, { projection: { _id: 0 } }).toArray();

        if (documents.length === 0) {
            console.log("⚠️ No hay documentos en la colección.");
            return;
        }

        // Guardar el JSON en un archivo
        fs.writeFileSync("output.json", JSON.stringify(documents, null, 2), "utf-8");
        console.log("✅ Datos exportados a output.json correctamente.");
    } catch (error) {
        console.error("❌ Error exportando datos:", error);
    } finally {
        await client.close();
        console.log("🔌 Conexión cerrada.");
    }
}

exportToJSON();
