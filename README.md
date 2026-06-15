# 🛡️ Distributed Rate Limiter

## 📌 Descripción del Proyecto
Este proyecto es una implementación de alto rendimiento de un **Limitador de Tasa Distribuido** (Distributed Rate Limiter). Su objetivo principal es controlar el flujo de tráfico entrante hacia una API o servicio web, protegiendo la infraestructura contra ataques de denegación de servicio (DDoS), abusos o picos inesperados de tráfico.

A diferencia de un limitador local, esta solución está diseñada desde cero para entornos de microservicios y sistemas distribuidos, garantizando que los límites de tráfico se mantengan consistentes a través de múltiples instancias de servidores simultáneos.

## 🎯 Propósito y Contexto
El desarrollo de este sistema responde a un desafío técnico de nivel avanzado ("Hard") orientado a dominar el **Diseño de Sistemas (System Design)**. El proyecto aborda compromisos arquitectónicos (trade-offs) complejos, priorizando la baja latencia sin sacrificar la consistencia en el control de peticiones.

Las principales motivaciones de este desarrollo incluyen:
* Aplicar algoritmos de control de tráfico en tiempo real con una complejidad temporal cercana a **O(1)**.
* Resolver problemas de concurrencia y sincronización en entornos distribuidos.
* Implementar arquitecturas limpias y patrones de diseño modernos que independizan la lógica de negocio del framework y la base de datos.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.13+ (aprovechando las mejoras recientes en el Global Interpreter Lock - GIL y tipado estático).
* **Framework Web:** FastAPI (elegido por su velocidad, ligereza y soporte nativo asíncrono para arquitecturas de microservicios).
* **Caché en Tiempo Real:** Redis (motor principal para el almacenamiento de contadores rápidos y sincronización distribuida).
* **Persistencia de Datos:** SQL (para el registro histórico, análisis de tráfico y persistencia de configuración a largo plazo).
* **Gestión de Entorno:** Herramientas modernas de empaquetado (ej. uv/Vite ecosystem tools) para dependencias consistentes.

## 🧠 Arquitectura y Patrones Implementados

El sistema no depende del framework, sino de una arquitectura robusta que permite escalabilidad horizontal. Se han implementado los siguientes conceptos clave:

* **Sliding Window (Ventana Deslizable):** Algoritmo core seleccionado por su precisión y justicia en el manejo de tráfico continuo, superior a las ventanas fijas de tiempo.
* **Hashing Distribuido:** Mecanismo esencial para enrutar de manera eficiente la identidad de los usuarios/clientes a través del clúster.
* **Patrón Repositorio:** Abstracción de la capa de datos que permite intercambiar motores de almacenamiento (Redis a SQL) sin alterar la lógica central del limitador.
* **Data Transfer Objects (DTOs):** Estructuras limpias para mover información de manera segura entre los controladores de FastAPI y el dominio de la aplicación.
* **Separación de Comando y Consulta (CQS):** Principio de Clean Code mantenido para garantizar la pureza y predictibilidad de las funciones del sistema.
* **Programación Asíncrona (Async/Await):** Gestión no bloqueante del I/O para manejar altos volúmenes de peticiones sin agotar los hilos de ejecución.

## 🗺️ Fases de Desarrollo

El ciclo de vida del proyecto está estructurado en 5 fases de evolución continua:

1. **Fundamentos y Clean Code:** Configuración del entorno en Python 3.13, adopción de principios SOLID y modelado inicial del dominio.
2. **Motor Algorítmico:** Implementación del algoritmo Sliding Window puro, garantizando estructuras de datos óptimas para validaciones O(1).
3. **Concurrencia y API:** Integración de FastAPI y programación asíncrona para exponer el limitador a través de endpoints eficientes.
4. **Persistencia Distribuida:** Conexión del núcleo lógico con clústeres de Redis para escalabilidad horizontal y bases de datos SQL para analítica.
5. **Testing, Tolerancia a Fallos y Documentación:** Pruebas de carga, manejo de fallos de red y documentación técnica arquitectónica basada en decisiones de System Design.
