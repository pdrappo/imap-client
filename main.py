import argparse
import imaplib
import email
from email.policy import default
from pathlib import Path
from getpass import getpass  # Para pedir la contraseña de forma segura


def connect_to_imap(server, username, password, folder="INBOX"):
    """Establece conexión con el servidor IMAP."""
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select(folder)
    return mail


def fetch_emails(mail, count=10, order="D"):
    """Obtiene los correos del servidor IMAP."""
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        raise Exception("No se pudieron obtener los mensajes.")

    message_ids = messages[0].split()
    if order == "D":  # Descendente
        message_ids = message_ids[::-1]

    selected_ids = message_ids[:count]
    emails = []
    for msg_id in selected_ids:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        if status == "OK":
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email, policy=default)
            emails.append((msg_id.decode(), msg))
    return emails


def display_email(msg, full=False, summary=False):
    """Muestra un mensaje con opciones de visualización."""
    if full:
        print(msg)
    elif summary:
        print(f"Fecha: {msg['Date']}\nRemitente: {msg['From']}\nAsunto: {msg['Subject']}\n")
    else:
        print(f"ID: {msg['Message-ID']}\nFecha: {msg['Date']}\nRemitente: {msg['From']}\nAsunto: {msg['Subject']}\n")


def export_email(msg, output_dir, msg_id):
    """Exporta un mensaje como archivo .eml."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    file_name = output_dir / f"message_{msg_id}.eml"
    with open(file_name, "w", encoding="utf-8") as eml_file:
        eml_file.write(msg.as_string())
    print(f"Mensaje exportado: {file_name}")


def main():
    parser = argparse.ArgumentParser(description="Cliente IMAP para correos.")
    parser.add_argument("server", help="Servidor IMAP (e.g., imap.gmail.com).")
    parser.add_argument("username", help="Usuario de correo.")
    parser.add_argument("-f", action="store_true", help="Muestra el mensaje completo.")
    parser.add_argument("-m", type=int, default=10, help="Cantidad de mensajes a mostrar.")
    parser.add_argument("-o", choices=["A", "D"], default="D", help="Orden de mensajes por fecha (A: ascendente, D: descendente).")
    parser.add_argument("-s", action="store_true", help="Muestra solo fecha, remitente y asunto.")
    parser.add_argument("-e", action="store", metavar="DIR", help="Exporta mensajes como .eml en el directorio especificado.")
    parser.add_argument("--folder", default="INBOX", help="Carpeta del correo a explorar (por defecto INBOX).")
    args = parser.parse_args()

    # Pedir la contraseña de forma segura
    password = getpass(prompt="Contraseña: ")

    try:
        mail = connect_to_imap(args.server, args.username, password, args.folder)
        emails = fetch_emails(mail, count=args.m, order=args.o)

        for msg_id, msg in emails:
            if args.e:
                export_email(msg, args.e, msg_id)
            else:
                display_email(msg, full=args.f, summary=args.s)

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
