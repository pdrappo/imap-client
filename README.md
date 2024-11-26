# Proyecto IMAP Client

Este es un script en Python que permite conectarse a un servidor de correo a través del protocolo IMAP. El script solicita al usuario el nombre de usuario y la contraseña de la cuenta de correo, y ofrece varias funcionalidades, como listar los correos más recientes, mostrar información detallada de los mensajes, exportar los correos en formato `.eml`, entre otras.

## Requisitos

- Python 3.x
- Librería `imaplib` (viene preinstalada con Python)
- Librería `getpass` (viene preinstalada con Python)
- Librería `email` (viene preinstalada con Python)

## Instalación

1. Clona este repositorio o descarga el archivo `main.py` a tu máquina local.

2. (Opcional) Crea un entorno virtual para manejar las dependencias:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3. No es necesario instalar dependencias adicionales ya que el script usa librerías estándar de Python.

## Uso

1. Ejecuta el script con el siguiente comando:

    ```bash
    python main.py
    ```

2. El script te pedirá que ingreses tu nombre de usuario y contraseña del correo electrónico. **Nota**: La contraseña no se mostrará mientras la escribes.

3. Usa los siguientes flags para personalizar la salida:

    - `-f`: Muestra el contenido completo del correo (por defecto solo se muestran los encabezados).
    - `-m N`: Muestra los primeros `N` correos. Ejemplo: `-m 5` para los 5 correos más recientes.
    - `-o A`: Ordena los correos de forma ascendente según la fecha de recepción (por defecto es descendente). Usa `-o D` para orden descendente.
    - `-s`: Muestra solo la fecha, remitente y asunto de los correos.
    - `-e`: Exporta cada correo en formato `.eml`.

### Ejemplos de uso

1. Para listar los 5 correos más recientes con detalles completos:

    ```bash
    python main.py -m 5 -f
    ```

2. Para mostrar solo la fecha, el remitente y el asunto de los 10 correos más recientes:

    ```bash
    python main.py -m 10 -s
    ```

3. Para ordenar los correos de forma ascendente y exportarlos como archivos `.eml`:

    ```bash
    python main.py -o A -e
    ```

## Notas

- El script utiliza el protocolo IMAP para conectarse a un servidor de correo y obtener los correos.
- Los mensajes se muestran en orden cronológico inverso por defecto (más recientes primero).
- Los correos pueden ser exportados como archivos `.eml` si se utiliza la opción `-e`.
  
## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
