# 🏋️‍♂️ GymForTMoment – Sistema de Gestión de Gimnasio

## 1. Descripción del proyecto

**GymForTMoment** es una aplicación de escritorio desarrollada en Python con Tkinter y SQLite, centrada en la gestión interna de un gimnasio que funciona 24 horas de lunes a viernes.

El sistema permite administrar:
- Clientes
- Reservas de aparatos
- Pagos mensuales
- Aparatos disponibles

La aplicación está diseñada para ofrecer un flujo sencillo de uso, con una interfaz clara y un menú lateral que permite navegar entre módulos de manera intuitiva.

## 2. Tecnologías utilizadas
- **Python 3.13**
- **Tkinter** (interfaz gráfica)
- **SQLite3** (base de datos integrada)
- **Pillow** (gestión de imágenes)
- **Git / GitHub** (control de versiones)

## 3. Requisitos previos
Para ejecutar la aplicación se necesita:
- Python 3.10 o superior
- Librerías utilizadas (se instalan automáticamente con `requirements.txt`)

**No es necesario crear tablas:**
👉 La aplicación genera la base de datos automáticamente al iniciarse.

## 4. Instalación y ejecución

1️⃣ **Clonar el repositorio**
```bash
git clone https://github.com/DavidLazaro08/GymForTheMoment
```

2️⃣ **Acceder al directorio del proyecto**
```bash
cd GymForTheMoment
```

3️⃣ **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4️⃣ **Ejecutar la aplicación**
```bash
python main.py
```

## 5. Primer inicio de sesión

La aplicación genera automáticamente un usuario administrador si no existe ninguno.

🔐 **Credenciales por defecto:**
- **Usuario:** `admin`
- **Contraseña:** `admin123`

Este usuario tiene acceso completo a todas las funciones del sistema.

> [!NOTE]
> Si olvidas la contraseña o eliminas al usuario `admin`, el sistema vuelve a crearlo automáticamente al iniciar, siempre que no existan usuarios registrados.

## 6. Flujo básico de uso

▶️ **1. Iniciar sesión**
Accede con la cuenta admin para desbloquear la aplicación.

▶️ **2. Gestión de clientes**
Permite crear, modificar y eliminar clientes.

▶️ **3. Gestión de reservas**
Cada aparato puede reservarse en tramos de 30 minutos.
La app permite ver qué aparatos están libres u ocupados en un día concreto.

▶️ **4. Gestión de pagos**
El sistema genera mensualmente los recibos y permite marcar clientes como pagados o morosos.

▶️ **5. Gestión de aparatos**
Creación, modificación y mantenimiento de los aparatos disponibles en el gimnasio.

## 7. Funcionalidades principales
✔️ Inicio de sesión con control de usuario y contraseña
✔️ Gestión completa de clientes
✔️ Generación y control mensual de pagos
✔️ Gestión de reservas por horas y días
✔️ Gestión de aparatos (alta, baja, edición)
✔️ Sistema visual unificado con tema oscuro
✔️ Base de datos SQLite autogenerada
✔️ Enrutado interno entre vistas con menú lateral

## 8. Estructura del proyecto
```
GestionGym_GutierrezDavid/
│
├── controller/          # Controladores de cada módulo
├── data/                # Base de datos, gestor BD y scripts SQL
├── model/               # Modelos (entidades del sistema)
├── view/                # Interfaz Tkinter (vistas)
├── util/                # Funciones auxiliares y validaciones
├── resources/           # Logos, estilos y recursos gráficos
├── excepciones.py       # Excepciones personalizadas
├── main.py              # Punto de entrada del programa
└── requirements.txt     # Dependencias
```

## 9. Mejoras futuras
🔧 Implementar alertas visuales más modernas
📊 Añadir panel de estadísticas del gimnasio
📅 Calendario visual para reservas
🔐 Sistema multicuenta con roles diferenciados
☁️ Migración opcional a base de datos remota (MySQL o PostgreSQL)

## 10. Licencia
Proyecto desarrollado con fines exclusivamente educativos como parte del módulo de Sistemas de Gestión Empresarial.

## 11. Autor
Aplicación desarrollada por:

👤 **David Gutiérrez Ortiz**
Desarrollador del proyecto completo.

---

### 📘 Documentación del proyecto
Incluye memoria, diagramas y diseño de datos:

➡️ **[Documentación Completa (PDF)](docs/Documentación_GFTM_DavidGutierrezRV.pdf)**
