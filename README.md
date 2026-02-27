# Link Security Checker

Link Security Checker es una herramienta diseñada para analizar URLs y detectar posibles amenazas de seguridad utilizando la API de VirusTotal. Ofrece una interfaz moderna y profesional con un estilo 'Glassmorphism' para una experiencia de usuario fluida.

## Tecnologías

Este proyecto utiliza las siguientes tecnologías:

- **Backend:** [Python](https://www.python.org/) con [Flask](https://flask.palletsprojects.com/)
- **Frontend:** HTML5, CSS3 (Custom Properties, Glassmorphism), JavaScript (Vanilla ES6+)
- **API de Terceros:** [VirusTotal API v3](https://developers.virustotal.com/reference/overview)

## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd link-security-checker
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python3 -m venv venv
   # En Windows:
   # venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   - Copia el archivo de ejemplo: `cp .env.example .env`
   - Edita el archivo `.env` y añade tu clave de API de VirusTotal:
     ```
     VT_API_KEY=tu_api_key_aqui
     ```

## Uso

Para iniciar el servidor de desarrollo, ejecuta:

```bash
python app.py
```

Por defecto, la aplicación estará disponible en `http://127.0.0.1:5000`.

## Nota Legal (Disclaimer)

Esta herramienta se proporciona únicamente con fines **educativos y de aprendizaje**. El desarrollador no se hace responsable del uso indebido de esta aplicación. Se recomienda no confiar exclusivamente en esta herramienta para la toma de decisiones críticas de seguridad y siempre utilizar múltiples fuentes de verificación.
