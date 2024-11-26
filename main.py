import imaplib
import getpass
from email.parser import BytesParser
from email.policy import default

def list_recent_emails():
    # Solicitar datos al usuario
    imap_host = input("Ingrese el servidor IMAP (por ejemplo, 'imap.gmail.com'): ")
    email_user = input("Ingrese su dirección de correo electrónico: ")
    email_pass = getpass.getpass("Ingrese su contraseña: ")

    try:
        # Conexión al servidor IMAP
        with imaplib.IMAP4_SSL(imap_host) as mail:
            # Iniciar sesión
            mail.login(email_user, email_pass)

            # Seleccionar la bandeja de entrada
            mail.select("inbox")

            # Buscar todos los correos electrónicos
            result, data = mail.search(None, "ALL")
            if result != "OK":
                print("Error al buscar correos.")
                return

            # Obtener los IDs de los correos electrónicos
            email_ids = data[0].split()

            # Tomar los últimos 5 correos (más recientes)
            latest_email_ids = email_ids[-5:]  # Últimos 5 IDs
            latest_email_ids.reverse()  # Opcional: Mostrar de más reciente a menos reciente

            print(f"\nSe encontraron {len(email_ids)} correos en total.")
            print(f"Mostrando los últimos {len(latest_email_ids)} correos más recientes:\n")

            # Recuperar y mostrar los encabezados de los últimos 5 correos
            for i, email_id in enumerate(latest_email_ids, start=1):
                result, msg_data = mail.fetch(email_id, "(RFC822.HEADER)")
                if result == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            headers = BytesParser(policy=default).parsebytes(response_part[1])
                            print(f"Correo {i}:")
                            print(f"  Fecha: {headers['Date']}")
                            print(f"  De: {headers['From']}")
                            print(f"  Asunto: {headers['Subject']}")
                            print("-" * 50)

    except imaplib.IMAP4.error as e:
        print(f"Error de conexión o autenticación: {e}")

if __name__ == "__main__":
    list_recent_emails()
