# ◾ Entendiendo Internet y la Web

**Dificultad:** 🌻

**Aprendizaje:** 🍯

**Tiempo:** ⏱️ 30 min

---

## Introducción

Antes de comenzar, es crucial que tengas una claridad básica de qué es y cómo funciona la Internet y la World Wide Web (WWW), que a menudo, se usan indistintamente, pero son cosas distintas y funciones diferenciadas. También cómo y para qué se comunican las máquinas (servidores / bots) para conseguir diferentes propósitos.

## ¿Qué es Internet?

Internet es la infraestructura global de redes que conecta millones de computadoras y dispositivos en todo el mundo. Es la red física que permite la comunicación y el intercambio de datos entre estos dispositivos. Desde su origen como un proyecto militar, Internet ha evolucionado hasta convertirse en una red global que facilita la comunicación, el acceso a la información y una amplia gama de servicios, desde el correo electrónico hasta el comercio electrónico y las redes sociales.

## ¿Qué es la World Wide Web?

La World Wide Web (WWW), por otro lado, es una parte de Internet que conocemos y usamos a diario. En castellano significa "Red de alcance mundial". Es un sistema de distribución de documentos de hipertexto o hipermedios interconectados y accesibles a través de Internet mediante un navegador web. Cuando visitas un sitio web, estás utilizando la WWW. Puedes ver páginas web que contienen una variedad de contenido, como texto, imágenes, videos y más, y puedes navegar entre ellas a través de enlaces.

## Relación con los motores de búsqueda y navegadores

Los navegadores web son aplicaciones que utilizamos en diferentes dispositivos (PCs, teléfonos, TVs, etc.) para acceder a la WWW a través de Internet. Ejemplos populares incluyen Google Chrome, Mozilla Firefox y Safari. Utilizamos los motores de búsqueda, como Google, Bing o Yahoo, para encontrar información en la WWW. Estos motores cumplen la función de indexar páginas web disponibles en Internet, permitiéndonos buscar y acceder a ellas fácilmente.

## Tráfico de Internet: Humanos vs. máquinas

Aunque solemos pensar en el tráfico de Internet como generado principalmente por personas utilizando sitios web o aplicaciones  para comunicarse, consumir o compartir contenido, etc. No obstante, la realidad es que la mayor parte del tráfico se genera **entre servidores y robots**, aunque esté gatillado por la actividad humana.

Los servidores se conectan entre sí para intercambiar información. Este intercambio ocurre incluso entre servidores de distintos productos/servicios. Por ejemplo:

### Ejemplo 1: Integración de servicios de pago

Un sitio de comercio electrónico necesita procesar pagos de manera segura.

**Comunicación entre Servidores:**

1. **Cliente hace un pago:** Compra y proporciona los detalles de pago.
2. **Servidor del comercio electrónico:** Envía una solicitud al servidor del proveedor de servicios de pago (por ejemplo, Stripe o PayPal) con la información del pago.
3. **Servidor del Proveedor de Pago:** Recibe la solicitud, procesa el pago y devuelve una respuesta al servidor del sitio de comercio electrónico, indicando si el pago fue exitoso o no.
4. **Confirmación de Pago:** El servidor del sitio de comercio electrónico recibe la respuesta y actualiza el estado del pedido del cliente en su base de datos.

### Ejemplo 2: Autenticación de usuarios

Cada vez que usas "Iniciar sesión con mi cuenta de Google" en algún sitio web que usa la autenticación de G.

**Comunicación entre Servidores:**

1. **Usuario inicia sesión con Google:** El usuario selecciona la opción de "Iniciar sesión con Google" en la aplicación web.
2. **Autenticación con Google:** La aplicación web redirige a la usuaria a la página de autenticación de Google, ahí ingresa sus credenciales (correo electrónico y contraseña). se solicita a la usuaria que autorice a la aplicación web para acceder a la información de su cuenta de Google.
3. **Google envía un código de autorización:** Una vez que la usuaria autoriza la aplicación, Google la redirige de vuelta a la aplicación web con un código de autorización.
4. **Servidor de la Aplicación Web:** El servidor de la aplicación web recibe el código de autorización y envía una solicitud al servidor de Google para intercambiar ese código por un *token* de acceso.
5. **Servidor de Google:** El servidor de Google verifica el código de autorización y, si es válido, devuelve un *token* de acceso y un *token* de actualización al servidor de la aplicación web.
6. **Acceso a Recursos Protegidos:** El servidor de la aplicación web utiliza el *token* de acceso para autenticar a la usuaria y permitirle acceder a los recursos protegidos en la aplicación. Además, puede usar el *token* de actualización para obtener un nuevo *token* de acceso cuando el actual expire.
7. **Confirmación de Autenticación:** El servidor de la aplicación web puede almacenar el *token* de acceso y el *token* de actualización en su base de datos para gestionar futuras solicitudes de acceso del usuario.

Como ves en estos dos simples ejemplos, hay todo un "mundo paralelo" de comunicaciones e intercambio de datos entre servidores, es ese el tipo de tráfico que es mayoritario en Internet.

El concepto de ***backend*** se refiere, precisamente, a la parte de una aplicación web o sitio web que no es visible para la usuaria final, pero que es esencial para su funcionamiento.

## La importancia de las API

Una API (Interfaz de Programación de Aplicaciones) es un conjunto de definiciones y protocolos que permiten que una aplicación se comunique con otra de manera predefinida, limitada y segura. 

Una posible metáfora (muy simple) para explicar una API sería un restaurante. El mesero (API) toma los pedidos de los clientes (solicitudes), los lleva a la cocina (backend) y trae la comida (respuesta) de vuelta a los clientes. Eso es muy diferente a lo caótico e inseguro que sería que cada cliente entre a la cocina a decir lo que quiere, etc. etc. Cada aplicación o sitio decide qué datos quiere intercambiar, en qué lenguajes de programación, bajo qué reglas, etc.

Muchas plataformas de no-code, gracias al uso de las API, permiten a sus usuarias integrar diferentes servicios y automatizar tareas complejas sin necesidad de programación. Por ejemplo, herramientas como Zapier utilizan APIs para conectar aplicaciones y automatizar flujos de trabajo.

---

## Actividad

Aprender a hacer preguntas, intentar formular nuestro propio entendimiento, así como incorporar otros puntos de vista, enriquece nuestro entendimiento de cualquier conocimiento recién adquirido.

Investiga brevemente sobre las siguientes preguntas. **Elije 1 o 2 respuestas que más te sorprendieron y comenta al respecto.**

1. ¿Se puede acceder a todos los sitios web Internet, o existen excepciones?

2. ¿Es posible tener acceso a Internet sin poder acceder a la Web? ¿Cómo?

3. Los motores de búsqueda en la Web, ¿son parte de la Web o de Internet?

4. ¿Cuál es la diferencia entre una página web y un sitio web?

5. ¿Es lo mismo un dominio que una URL? ¿Cómo se estructuran?

6. ¿Qué significa que una página web sea dinámica? ¿Cómo se compara con una estática?

7. ¿Podemos considerar las redes sociales como parte de la Web o son algo aparte de Internet?

8. ¿Qué es el Internet de las Cosas (IoT) y cómo cambia nuestra interacción con el mundo físico?

9. ¿Cómo crees que la automatización de tareas mediante APIs y plataformas no-code puede impactar la estructura y funcionamiento de una organización?
   
   Reflexiona sobre los cambios en la gestión de tareas, roles de los empleados y eficiencia operativa.

## Insumos adicionales para tu aprendizaje:

- Dr. Google (siempre)

- AI: ChatGPT, Gemini, Perplexity, Bing, etc.. Recuerda que pueden alucinar y mentirte descaradamente, verifica siempre.

- [📺 Video: ¿Cómo funciona Internet?](https://www.youtube.com/watch?v=-InB0vz_Mec)

## Guía de Autoevaluación

No habrás cumplido con la actividad si:

- [x] No investigaste sobre cada una de las preguntas.
- [x] No comentas en el hilo de Discord sobre 1 o 2 rptas que te parecieron interesantes.

---

Opcional si quieres profundizar por tu cuenta:

[📄 Texto: ¿Qué es una API? - Explicación de interfaz de programación de aplicaciones - AWS](https://aws.amazon.com/es/what-is/api/)

