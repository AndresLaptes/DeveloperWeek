const { MongoClient } = require("mongodb");
const fs = require("fs");

// Configurar la conexión a MongoDB
const uri = "mongodb+srv://omar_user:123@developerweek.tl23p.mongodb.net/?retryWrites=true&w=majority&appName=DeveloperWeek";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function exportToJSON() {
    try {

        const database = client.db("example_db");  // Reemplaza con el nombre de tu BD
        let collection = database.collection("example_db");  // Reemplaza con el nombre de tu colección

        // Obtener todos los documentos excluyendo _id
        let documents = await collection.find({}, { projection: { _id: 0 } }).toArray();

        if (documents.length === 0) {
            console.log("⚠️ No hay documentos en la colección.");
            return;
        }

        // Guardar el JSON en un archivo
        fs.writeFileSync("output.json", JSON.stringify(documents, null, 2), "utf-8");
        console.log("✅ Datos exportados a output.json correctamente.");


        collection = database.collection("team_looking_for_people");
        documents = await collection.find({}, { projection: { _id: 0 } }).toArray();

        if (documents.length === 0) {
            console.log("⚠️ No hay documentos en la colección.");
            return;
        }
        fs.writeFileSync("team_looking_for_people.json", JSON.stringify(documents, null, 2), "utf-8");
        console.log("✅ Datos exportados a output.json correctamente.");


        collection = database.collection("people_looking_for_teams");
        documents = await collection.find({}, { projection: { _id: 0 } }).toArray();

        if (documents.length === 0) {
            console.log("⚠️ No hay documentos en la colección.");
            return;
        }

        fs.writeFileSync("people_looking_for_teams.json", JSON.stringify(documents, null, 2), "utf-8");
        console.log("✅ Datos exportados a output.json correctamente.");

    } catch (error) {
        console.error("❌ Error exportando datos:", error);
    } finally {
        await client.close();
        console.log("🔌 Conexión cerrada.");
    }
}

async function deleteCollections(database) {
    try {
        console.log("✅ Eliminando colecciones...");

        const collectionsToDelete = [
            "people_with_friends",
            "solo_participants",
            "grouped_teams",
            "people_looking_for_teams",
            "team_looking_for_people",
            "teams_definitly"
        ];

        for (const collectionName of collectionsToDelete) {
            const collectionExists = (await database.listCollections({ name: collectionName }).toArray()).length > 0;

            if (collectionExists) {
                await database.collection(collectionName).drop();
                console.log(`🗑️ ${collectionName} eliminada por completo`);
            } else {
                console.log(`⚠️ La colección ${collectionName} no existía.`);
            }
        }

        console.log("✅ Todas las colecciones han sido eliminadas.");
    } catch (error) {
        console.error("❌ Error eliminando colecciones:", error);
    }
}

async function processCollections(database) {
    try {
        console.log("✅ Procesando nuevas colecciones...");

        const collection = database.collection("example_db");

        const documents = await collection.find({}, { projection: { _id: 0 } }).toArray();

        if (documents.length === 0) {
            console.log("⚠️ No hay documentos en la colección.");
            return;
        }

        // Separate people into different categories
        const peopleWithFriends = documents.filter(doc => doc.friend_registration.length > 0);
        const soloParticipants = documents.filter(doc => doc.preferred_team_size === 1);
        const peopleLookingForTeams = documents.filter(doc => doc.friend_registration.length === 0 && doc.preferred_team_size > 1);

        const groupedTeams = [];
        const processedIds = new Set(); // Keep track of already grouped people
        let teamCounter = 1; // Counter to create unique team IDs

        // Grouping logic for people with friends
        peopleWithFriends.forEach(person => {
            if (processedIds.has(person.id)) return; // Skip if already in a team

            let team = [person];
            processedIds.add(person.id);

            // Find their friends in the dataset
            person.friend_registration.forEach(friendId => {
                const friend = documents.find(doc => doc.id === friendId);
                if (friend && !processedIds.has(friend.id)) {
                    team.push(friend);
                    processedIds.add(friend.id);
                }
            });

            groupedTeams.push({
                team_id: `team_${teamCounter++}`, // Assign unique team ID
                members: team,
                team_size: team.length
            });
        });

        // ✅ Create teams for people looking for teams (solo teams)
        const soloTeamsForLookingForTeams = peopleLookingForTeams.map(p => ({
            team_id: `team_${teamCounter++}`, // Assign unique team ID for solo teams
            members: [{
                id: p.id,
                preferred_team_size: p.preferred_team_size,
                team_size: 1, // Add the team size directly here
                ...p // Spread all person details into the member
            }],
            team_size: 1
        }));

        // ✅ Calculate `teamsDefinitly` based on the same logic as before
        const teamsDefinitly = [
            ...soloParticipants.map(p => ({
                team_id: `team_${teamCounter++}`,
                members: [{
                    id: p.id,
                    preferred_team_size: p.preferred_team_size,
                    team_size: 1,
                    ...p // Spread all person details into the member
                }],
                team_size: 1
            })),
            ...groupedTeams.filter(team => {
                // Get all preferred team sizes from members
                const preferredSizes = team.members.map(m => m.preferred_team_size || team.team_size);
                const avgPreferredSize = preferredSizes.reduce((sum, val) => sum + val, 0) / preferredSizes.length;

                // Keep teams where preferred size is close to actual team size
                return Math.abs(avgPreferredSize - team.team_size) <= 1;
            })
        ];

        // ✅ Create `teamLookingForPeople` for teams where preferred size doesn't match actual team size
        const teamLookingForPeople = groupedTeams.filter(team => {
            const preferredSizes = team.members.map(m => m.preferred_team_size || team.team_size);
            const avgPreferredSize = preferredSizes.reduce((sum, val) => sum + val, 0) / preferredSizes.length;

            // Teams where the preferred size differs significantly from the actual team size
            return Math.abs(avgPreferredSize - team.team_size) > 1;
        }).map(team => ({
            team_id: team.team_id,
            members: team.members,
            team_size: team.team_size
        }));

        // MongoDB Collections
        const peopleWithFriendsCollection = database.collection("people_with_friends");
        const soloParticipantsCollection = database.collection("solo_participants");
        const groupedTeamsCollection = database.collection("grouped_teams");
        const peopleLookingForTeamsCollection = database.collection("people_looking_for_teams");
        const teamsDefinitlyCollection = database.collection("teams_definitly");
        const teamLookingForPeopleCollection = database.collection("team_looking_for_people");

        // Insert Data
        if (peopleWithFriends.length > 0) await peopleWithFriendsCollection.insertMany(peopleWithFriends);
        if (soloParticipants.length > 0) await soloParticipantsCollection.insertMany(soloParticipants);
        if (groupedTeams.length > 0) await groupedTeamsCollection.insertMany(groupedTeams);
        if (peopleLookingForTeams.length > 0) await peopleLookingForTeamsCollection.insertMany(soloTeamsForLookingForTeams); // Insert individual teams for people looking for teams
        if (teamsDefinitly.length > 0) await teamsDefinitlyCollection.insertMany(teamsDefinitly); // Insert `teamsDefinitly`
        if (teamLookingForPeople.length > 0) await teamLookingForPeopleCollection.insertMany(teamLookingForPeople); // Insert `teamLookingForPeople`

        console.log("✅ Datos procesados y guardados en nuevas colecciones.");
    } catch (error) {
        console.error("❌ Error exportando datos:", error);
    }
}











async function main() {
    try {
        await client.connect();
        console.log("✅ Conectado a MongoDB");

        const database = client.db("example_db");

        //await deleteCollections(database);
        //await processCollections(database);
        await exportToJSON();

    } catch (error) {
        console.error("❌ Error en la ejecución:", error);
    } finally {
        await client.close();
        console.log("🔌 Conexión cerrada.");
    }
}

main();

