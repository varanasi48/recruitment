const { MongoClient } = require('mongodb');

let cachedDb = null;

async function connectToDatabase(uri) {
    if (cachedDb) {
        return cachedDb;
    }

    const client = await MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    const db = client.db('your-database-name');
    cachedDb = db;
    return db;
}

module.exports = async function (context, req) {
    const db = await connectToDatabase(process.env.MONGODB_URI);
    const collection = db.collection('your-collection-name');

    // Example operation: find all documents
    const documents = await collection.find({}).toArray();

    context.res = {
        status: 200,
        body: documents
    };
};