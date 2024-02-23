const nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
    host: 'dirección-de-tu-servidor-smtp', // Reemplaza con tu dirección de host SMTP
    port: 587, // Ajusta según tu configuración de puerto
    secure: false, // true para 465, false para otros puertos
    auth: {
        user: 'tu-usuario', // Tu nombre de usuario SMTP
        pass: 'tu-contraseña' // Tu contraseña SMTP
    },
    tls: {
        rejectUnauthorized: false // Solo para desarrollo. En producción, debes tener una configuración TLS/SSL adecuada
    }
});

let mailOptions = {
    from: 'noreply@tu-dominio.com', // Tu dirección de correo 'De'
    to: 'destinatario@example.com', // El destinatario del correo
    subject: 'Asunto del correo',
    text: 'Contenido del correo...'
};

transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
        return console.log(error);
    }
    console.log('Mensaje enviado: %s', info.messageId);
});