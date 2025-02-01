require('dotenv').config();
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME
});

console.log('Tentativo di connessione al database...');

connection.connect((err) => {
  if (err) {
    console.error('❌ Errore di connessione:', err);
    console.error('Dettagli connessione:');
    console.error(`Host: ${process.env.DB_HOST}`);
    console.error(`Porta: ${process.env.DB_PORT}`);
    console.error(`Database: ${process.env.DB_NAME}`);
    console.error(`Utente: ${process.env.DB_USER}`);
  } else {
    console.log('✅ Connessione al database riuscita!');
    console.log(`Server: ${connection.config.host}:${connection.config.port}`);
    console.log(`Database: ${connection.config.database}`);
  }
  
  connection.end();
});
