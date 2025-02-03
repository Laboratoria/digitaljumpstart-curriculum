# Introducción al HTML Semántico

HTML semántico se refiere al uso de etiquetas HTML que conllevan significado, ayudando a describir el contenido y su estructura tanto para las desarrolladoras web como para los navegadores. A diferencia de las etiquetas no semánticas como `<div>` y `<span>`, las etiquetas semánticas como `<header>`, `<article>`, y `<footer>` proporcionan más información sobre el contenido que encierran.

## ¿Por qué es importante el HTML Semántico?

1. **Accesibilidad**: Mejora la experiencia de usuarias con discapacidades sensoriales, ya que los lectores de pantalla y otras tecnologías de asistencia pueden interpretar mejor el contenido. Las etiquetas semánticas ayudan a las usuarias a navegar y entender la página de manera más efectiva.
2. **SEO**: Los motores de búsqueda entienden mejor la estructura y el contenido de la página, mejorando el posicionamiento en los resultados de búsqueda. Al utilizar etiquetas semánticas, se proporciona un contexto adicional que los motores de búsqueda pueden usar para indexar y clasificar el contenido.
3. **Mantenimiento**: Facilita la lectura y el mantenimiento del código, ya que su estructura y propósito son más claros. Las desarrolladoras pueden identificar rápidamente las secciones de la página y entender su funcionalidad sin necesidad de leer grandes cantidades de código.

## Etiquetas Semánticas Comunes

#### `<header>`

La etiqueta `<header>` representa el encabezado de una sección o página. Puede contener títulos, logotipos, navegación, etc. Es ideal para agrupar elementos de cabecera y mantener una estructura coherente.

```html
<header>
  <h1>Mi Sitio Web</h1>
  <nav>
    <ul>
      <li><a href="#home">Inicio</a></li>
      <li><a href="#about">Acerca de</a></li>
      <li><a href="#contact">Contacto</a></li>
    </ul>
  </nav>
</header>
```

#### `<nav>`

La etiqueta `<nav>` se utiliza para definir un bloque de enlaces de navegación. Es crucial para crear menús accesibles y fácilmente navegables.

```html
<nav>
  <ul>
    <li><a href="#home">Inicio</a></li>
    <li><a href="#services">Servicios</a></li>
    <li><a href="#contact">Contacto</a></li>
  </ul>
</nav>
```

#### `<main>`

La etiqueta `<main>` representa el contenido principal del documento. Debe ser único y contener la información más relevante de la página. Solo debe haber un `<main>` por documento.

```html
<main>
  <h2>Bienvenidas a Nuestro Sitio</h2>
  <p>Este es el contenido principal de la página.</p>
</main>
```

#### `<article>`

La etiqueta `<article>` se usa para encapsular contenido independiente y auto contenido, como artículos de noticias, publicaciones de blog, etc. Cada `<article>` debe poder ser entendido de manera aislada.

```html
<article>
  <h2>Artículo de Blog</h2>
  <p>Este es un ejemplo de artículo de blog.</p>
</article>
```

#### `<section>`

La etiqueta `<section>` define secciones de un documento, como capítulos, encabezados temáticos, o cualquier agrupación de contenido. Es útil para dividir el contenido en partes más manejables y lógicas.

```html
<section>
  <h2>Sección 1</h2>
  <p>Contenido de la primera sección.</p>
</section>
<section>
  <h2>Sección 2</h2>
  <p>Contenido de la segunda sección.</p>
</section>
```

#### `<aside>`

La etiqueta `<aside>` contiene contenido relacionado tangencialmente al contenido principal. Se suele usar para barras laterales, notas al margen, etc. Los contenidos en `<aside>` son complementarios pero no esenciales para el contenido principal.

```html
<aside>
  <h2>Acerca del Autor</h2>
  <p>Información sobre el autor del artículo.</p>
</aside>
```

#### `<footer>`

La etiqueta `<footer>` representa el pie de página de una sección o documento. Suele contener información sobre el autor, derechos de autor, enlaces de contacto, etc.

```html
<footer>
  <p>© 2024 Mi Sitio Web. Todos los derechos reservados.</p>
</footer>
```

## Beneficios Adicionales del uso de HTML Semántico

1. **Interoperabilidad**: Las etiquetas semánticas facilitan la interoperabilidad entre diferentes plataformas y dispositivos, asegurando que el contenido se presente de manera consistente.
2. **Eficiencia en el Desarrollo**: Al proporcionar una estructura clara, las etiquetas semánticas permiten a los equipos de desarrollo trabajar de manera más eficiente, facilitando la colaboración y la comprensión del código.
3. **Soporte para CSS y JavaScript**: Las etiquetas semánticas mejoran la aplicación de estilos y la manipulación del DOM con JavaScript. Al tener una estructura semántica clara, es más fácil aplicar estilos específicos y scripts a diferentes partes del documento.
4. **Compatibilidad Futura**: El uso de etiquetas semánticas asegura que tu código HTML esté alineado con las mejores prácticas y estándares web actuales, facilitando su actualización y mantenimiento a largo plazo.

## Conclusión

El uso de HTML semántico mejora significativamente la accesibilidad, el SEO y la mantenibilidad del código. Al utilizar etiquetas semánticas, no solo ayudas a los motores de búsqueda y tecnologías asistivas a entender mejor tu contenido, sino que también facilitas la lectura y el mantenimiento del código para ti y otros desarrolladores. Experimenta con estas etiquetas en tus proyectos para ver cómo pueden mejorar la estructura y claridad de tus páginas web.

[📺 Video: semántica y más - minutos 51 - 58](https://www.youtube.com/watch?v=3nYLTiY5skU&t=3230s&pp=ygUSIiBIVE1MIHNlbcOhbnRpY28i)
