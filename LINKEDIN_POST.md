Acabo de publicar la v1.0 de mi proyecto personal: **RedSec Dashboard**. 🚀

Llevo unas semanas trabajando en esto porque quería ir más allá de los tutoriales y construir una herramienta de seguridad real, enfrentándome a problemas de arquitectura de verdad.

El objetivo era simple: una interfaz moderna para escanear redes, pero por debajo hay bastante ingeniería. 🛠️

Lo que he montado:
*   **Backend:** Python con **FastAPI**. He usado `async/await` para manejar las tareas de escaneo de Nmap sin bloquear el servidor, y una arquitectura modular para poder escalar en el futuro.
*   **Frontend:** **React + TypeScript** (con Vite). Nada de plantillas, he creado componentes reutilizables y gestionado el estado global para tener actualizaciones en tiempo real del escáner.
*   **DevOps:** Todo contenerizado con **Docker Compose**. Me he peleado bastante con las redes de Docker para comunicar el frontend y el backend de forma segura, pero ahora se despliega con un solo comando.

Ha sido un reto pasar de "funciona en mi local" a tener un entorno de producción robusto, pero he aprendido muchísimo sobre ciclo de vida de software y buenas prácticas.

Si buscáis a alguien con ganas de aprender y que no le tiene miedo al código, echad un ojo a mi repo. ¡Cualquier feedback técnico es bienvenido! 👇

🔗 https://github.com/gsan-dev/redsec-dashboard

#SoftwareEngineering #Python #React #Docker #CyberSecurity #JuniorDeveloper #OpenSource
