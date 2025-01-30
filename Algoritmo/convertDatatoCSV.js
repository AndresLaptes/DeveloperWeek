const { MongoClient } = require("mongodb");
const fs = require("fs");
const { Parser } = require("json2csv");

// Configurar la conexión a MongoDB
const uri = "mongodb+srv://omar_user:123@developerweek.tl23p.mongodb.net/?retryWrites=true&w=majority&appName=DeveloperWeek";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function exportToCSV() {
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

        // Convertir los documentos a formato CSV
        const json2csvParser = new Parser();
        const csv = json2csvParser.parse(documents);

        // Guardar el CSV en un archivo
        fs.writeFileSync("output.csv", csv, "utf-8");
        console.log("✅ Datos exportados a output.csv correctamente.");
    } catch (error) {
        console.error("❌ Error exportando datos:", error);
    } finally {
        await client.close();
        console.log("🔌 Conexión cerrada.");
    }
}

exportToCSV();