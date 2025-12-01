# Mirror for Instagram

Una herramienta de línea de comandos para analizar cuentas de Instagram, ver listas de seguidores/siguiendo, encontrar mutuals y descubrir conexiones comunes entre usuarios.

## Funcionalidad

- 📊 Ver información de usuarios
- 👥 Obtener listas de seguidores y seguidos
- 🔍 Descubrir cuentas que no te siguen de vuelta
- 💾 Guarda tu sesión

## Primeros Pasos

### Requisitos Previos

- Python 3.7 o superior
- Una cuenta de Instagram

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/he4tw4ve/MirrorForInstagram.git
cd MirrorForInstagram
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Primera Ejecución

Ejecuta la aplicación:
```bash
python main.py
```

En la primer ejecución necesitas iniciar sesión en una cuenta de instagram con tu usuario y contraseña. La sesión se guardará localmente en `session.json` para uso futuro.

Si quieres iniciar sesión con otra cuenta, elimina `session.json` y vuelve a ejecutar la aplicación.

## Uso Básico

Una vez iniciada sesión, puedes usar los siguientes comandos:

### Comandos

- **`info <username>`** - Ver información detallada de un usuario
  ```
  mirror> info diegoo_ghz
  ```

- **`followers <username>`** - Listar todos los seguidores de un usuario
  ```
  mirror> followers diegoo_ghz
  ```

- **`following <username>`** - Listar todas las cuentas que sigue un usuario
  ```
  mirror> following diegoo_ghz
  ```

- **`mutuals <username>`** - Mostrar cuentas que siguen y son seguidas por el usuario
  ```
  mirror> mutuals diegoo_ghz
  ```

- **`notfollowed <username>`** - Mostrar cuentas que el usuario sigue pero no le siguen de vuelta
  ```
  mirror> notfollowed diegoo_ghz
  ```

- **`notfollowing <username>`** - Mostrar seguidores que el usuario no sigue de vuelta
  ```
  mirror> notfollowing diegoo_ghz
  ```

- **`exit`** - Salir de la aplicación

### Consejos

- La primera vez que obtengas seguidores/siguiendo de una cuenta grande, puede tomar tiempo debido a los límites de Instagram
- Los datos de sesión se guardan localmente - no necesitarás iniciar sesión nuevamente a menos que la sesión expire
- Todos los resultados incluyen enlaces clickeables a fotos de perfil (en terminales compatibles)

## Notas

⚠️ **Importante**: Esta herramienta usa la API privada de Instagram a través de la librería `instagrapi`. Evita solicitudes excesivas para prevenir que tu cuenta sea marcada.

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.