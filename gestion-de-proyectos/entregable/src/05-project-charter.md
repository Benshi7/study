# 5. Project Charter

## 5.1 Identificación del proyecto

**Nombre del proyecto:**  
Modernización del Mapa Interactivo de la Ciudad

**Tipo de proyecto:**  
Proyecto de transformación y modernización digital de un servicio público.

**Metodología de gestión:**  
Metodología en cascada (Waterfall), con etapas, actividades y entregables definidos previamente y una secuencia de ejecución planificada.

**Justificación de la metodología:**  
Se adopta cascada porque el alcance puede detallarse desde el inicio, los requisitos están bien definidos, el entorno es regulado y predecible (organismos públicos y sistemas oficiales), los roles están establecidos y la entrega en producción es única al final. Las ventajas buscadas son claridad de requisitos, gestión y seguimiento simples y buena documentación. La desventaja asumida es la poca flexibilidad ante cambios no previstos, que se gestiona con el control de cambios (5.9.2).

**Organización / contexto:**  
Gobierno de la Ciudad de Buenos Aires, en el marco de la modernización de sus servicios digitales y de los canales de acceso a información georreferenciada.

**Equipo responsable:**  
Equipo de proyecto multidisciplinario, integrado por perfiles de gestión de proyectos, tecnología, datos, diseño y comunicación.

**Duración:**  
6 meses (del 01/04 al 30/09/2026; el camino crítico del cronograma suma 126 días hábiles, unas 25 semanas, dentro de una ventana de 131 días hábiles).

**Fecha de inicio:**  
1 de abril de 2026 (inicio de la planificación). El Charter se aprueba el 14 de abril de 2026, primer hito del proyecto.

**Fecha de finalización:**  
30 de septiembre de 2026 (hito final de cierre).

**Descripción breve del proyecto**

A partir de la solución elegida en el proceso de Design Thinking y el Canvas de Plataforma Multilateral, formalizamos el Project Charter:

El proyecto propone modernizar el Mapa Interactivo de la Ciudad mediante la incorporación de una **capa geográfica común**, capaz de centralizar y organizar información proveniente de diferentes áreas y sistemas.

Esta capa permitirá que la información georreferenciada pueda ser utilizada por distintos canales digitales de la Ciudad, incluyendo el Mapa Interactivo y, sujeto a validación técnica, canales conversacionales como **Boti y BAX**.

Además, se propone incorporar un mecanismo de **reportes ciudadanos georreferenciados**, mediante el cual los vecinos puedan informar incidencias de su entorno, como calles cortadas, obstáculos o vehículos detenidos. Estos reportes podrán ser visualizados, validados por otros usuarios y derivados para su gestión, permitiendo actualizar su estado hasta su resolución.

De esta manera, el proyecto busca transformar el mapa de una herramienta principalmente consultiva en una **plataforma geográfica común**, que conecte información oficial, canales digitales y participación ciudadana.

## 5.2 Propósito y justificación

### 5.2.1 Propósito del proyecto

El propósito del proyecto es modernizar el Mapa Interactivo de la Ciudad para convertirlo en una **plataforma geográfica común**, capaz de integrar información proveniente de diferentes áreas y sistemas, facilitar su acceso desde distintos canales digitales y permitir una mayor participación de los vecinos.

La propuesta busca que la ubicación geográfica funcione como un elemento común para organizar y relacionar información de la ciudad. De esta manera, un vecino podrá acceder a información relevante de su entorno sin necesidad de conocer previamente qué área del Gobierno de la Ciudad administra cada servicio ni qué canal debe utilizar para realizar una consulta o un reporte.

El proyecto también busca incorporar un mecanismo de **participación ciudadana georreferenciada**, mediante el cual los vecinos puedan informar incidencias que ocurren en la vía pública y consultar su evolución. Los reportes podrán ser validados por otros usuarios y derivados a las áreas correspondientes para su gestión.

### 5.2.2 Justificación

Durante el proceso de Design Thinking se identificó como problema principal la **dispersión de información entre diferentes canales, áreas y sistemas**, situación que dificulta el acceso rápido del vecino a información relevante de su zona.

Actualmente, una persona puede necesitar consultar información, realizar un reclamo o conocer una situación determinada de su entorno sin saber previamente qué organismo es responsable ni dónde se encuentra disponible esa información. Esta situación genera una experiencia fragmentada y obliga al ciudadano a realizar búsquedas en diferentes canales.

Frente a este problema, el proyecto propone utilizar el componente geográfico como punto de integración. En lugar de desarrollar soluciones independientes para cada área, se plantea una **capa geográfica reutilizable** que permita centralizar información y ponerla a disposición de diferentes servicios y canales digitales.

La incorporación de reportes ciudadanos agrega además una dimensión participativa al proyecto. El vecino no solamente consulta información existente, sino que puede aportar información sobre situaciones que ocurren en su entorno. La posibilidad de validar y actualizar estos reportes permite construir un flujo de información que conecta al ciudadano con las áreas responsables de la gestión.

La integración con canales digitales existentes, como Boti y BAX, se plantea como una posibilidad para ampliar los puntos de acceso a la información sin obligar al ciudadano a utilizar exclusivamente el Mapa Interactivo. La validación técnica y el alcance concreto de estas integraciones deberán definirse durante las etapas iniciales del proyecto.

En consecuencia, el proyecto busca pasar de un modelo de información distribuida hacia un modelo basado en una **identidad geográfica común**, donde el mapa funcione como infraestructura de información y conexión entre ciudadanos, datos, servicios y áreas de gestión.

## 5.3 Problema

La información relacionada con servicios, incidencias y actividades de la Ciudad se encuentra distribuida entre diferentes áreas, sistemas y canales digitales. Esta fragmentación dificulta que los vecinos puedan acceder rápidamente a información relevante de su entorno y, en determinados casos, los obliga a identificar previamente qué organismo es responsable y qué canal deben utilizar.

La situación se vuelve especialmente relevante frente a acontecimientos que cambian rápidamente en el espacio público, como calles cortadas, vehículos detenidos, obstáculos, obras u otras incidencias. En estos casos, la información puede resultar útil tanto para el vecino que necesita conocer qué ocurre en su zona como para las áreas responsables de gestionar la situación.

A su vez, los mecanismos actuales de consulta y reporte no necesariamente comparten una misma referencia geográfica. Esto puede generar información duplicada, dificultades para relacionar datos provenientes de diferentes sistemas y una experiencia fragmentada para el ciudadano.

El problema central identificado es, por lo tanto:

**La falta de una capa geográfica común que permita integrar información de diferentes áreas y canales, dificultando el acceso del vecino a información actualizada y geolocalizada y limitando la posibilidad de conectar los reportes ciudadanos con la gestión de las incidencias.**

### 5.3.1 Consecuencias del problema

La situación identificada puede generar las siguientes consecuencias:

- Dificultad para encontrar información relevante de una zona determinada.

- Necesidad de utilizar diferentes canales para realizar consultas o reportes.

- Falta de visibilidad sobre el estado y evolución de determinadas incidencias.

- Posible duplicación de información o soluciones geográficas desarrolladas de manera independiente por distintas áreas.

- Dificultad para relacionar los reportes ciudadanos con la información oficial disponible.

- Mayor esfuerzo por parte del ciudadano para identificar el canal o área correspondiente.

- Menor aprovechamiento de la información geográfica como recurso transversal entre diferentes servicios digitales.

### 5.3.2 Oportunidad de mejora

El problema identificado representa una oportunidad para utilizar la **ubicación geográfica como elemento común de integración** entre información oficial, canales digitales y participación ciudadana.

La modernización propuesta permitiría avanzar hacia un modelo en el cual una misma capa geográfica pueda ser utilizada por diferentes servicios, mientras que los vecinos puedan consultar información, generar reportes y conocer su estado desde los canales disponibles.

De esta forma, el proyecto no busca únicamente actualizar una interfaz de mapa, sino **transformar la función del mapa dentro del ecosistema digital de la Ciudad**, convirtiéndolo en una fuente común de información georreferenciada.

## 5.4 Objetivos del proyecto

### 5.4.1 Objetivo general

**Modernizar el Mapa Interactivo de la Ciudad mediante el desarrollo de una capa geográfica común que integre información oficial, facilite su acceso desde diferentes canales digitales y permita a los vecinos reportar, validar y consultar incidencias geolocalizadas, mejorando la disponibilidad y trazabilidad de la información relacionada con su entorno.**

### 5.4.2 Objetivos específicos

**1. Centralizar la información georreferenciada**

Diseñar e implementar una estructura de datos geográfica común que permita integrar información proveniente de diferentes áreas y fuentes oficiales, estableciendo criterios de organización, actualización y disponibilidad.

**2. Integrar la información geográfica con distintos canales digitales**

Desarrollar mecanismos de integración mediante APIs que permitan que la información georreferenciada pueda ser consultada y utilizada desde el Mapa Interactivo y otros canales digitales seleccionados, incluyendo Boti y BAX, sujeto a validación técnica.

**3. Implementar un sistema de reportes ciudadanos georreferenciados**

Desarrollar una funcionalidad que permita a los vecinos informar incidencias de la vía pública mediante su ubicación geográfica, categoría, fecha y hora, incorporando información adicional cuando corresponda.

**4. Incorporar mecanismos de validación colaborativa**

Permitir que otros usuarios puedan confirmar, actualizar o informar la desaparición de una incidencia reportada, utilizando la participación ciudadana como mecanismo complementario para mantener actualizada la información.

**5. Implementar un sistema de seguimiento de incidencias**

Definir un flujo que permita registrar y visualizar el estado de cada reporte desde su creación hasta su resolución o cierre, facilitando la trazabilidad de la incidencia.

**6. Facilitar la gestión de información por parte de las áreas responsables**

Proporcionar mecanismos que permitan a las áreas correspondientes acceder a los reportes y a la información geográfica relevante para su ámbito de gestión.

**7. Establecer criterios de calidad y gobernanza de los datos**

Definir responsables, criterios de actualización, fuentes de información y mecanismos de control que permitan mantener la calidad, consistencia y actualidad de los datos utilizados por la plataforma.

**8. Mejorar el acceso del vecino a información relevante de su entorno**

Reducir la necesidad de que el ciudadano conozca previamente qué organismo o canal debe utilizar para acceder a información geolocalizada, centralizando la consulta y facilitando el acceso desde diferentes puntos de interacción.

## 5.5 Alcance del proyecto

### 5.5.1 Alcance incluido

El proyecto comprende la modernización del Mapa Interactivo de la Ciudad como una plataforma geográfica común para integrar información oficial, facilitar el acceso desde diferentes canales digitales y habilitar mecanismos de participación ciudadana.

Dentro del alcance se incluyen las siguientes actividades y componentes:

- **Desarrollo de una capa geográfica común**  
Diseño e implementación de una estructura geográfica que permita relacionar y visualizar información proveniente de diferentes áreas y sistemas de la Ciudad.

- **Integración de información oficial**  
Relevamiento e integración de fuentes de datos y APIs seleccionadas, estableciendo criterios de actualización, responsables y mecanismos básicos de control de calidad.

- **Integración con canales digitales**  
Desarrollo de los mecanismos necesarios para que la información geográfica pueda ser consultada y utilizada desde diferentes canales digitales de la Ciudad, incluyendo el Mapa Interactivo y canales conversacionales seleccionados, como Boti y BAX, sujetos a validación técnica y de alcance.

- **Sistema de reportes ciudadanos georreferenciados**  
Implementación de una funcionalidad que permita a los vecinos informar incidencias de su entorno, como vehículos detenidos, obstrucciones, cortes u otros eventos relevantes, asociando cada reporte con una ubicación geográfica y una categoría.

- **Validación colaborativa de reportes**  
Incorporación de mecanismos para que otros usuarios puedan confirmar, actualizar o indicar que una incidencia ya no se encuentra presente, contribuyendo a mantener actualizada la información.

- **Seguimiento del estado de las incidencias**  
Definición de un flujo que permita registrar el ciclo de vida de un reporte, desde su creación y validación hasta su derivación, resolución y cierre cuando corresponda.

- **Vista de gestión para las áreas responsables**  
Desarrollo de una funcionalidad básica que permita a las áreas correspondientes consultar los reportes asociados a su ámbito de responsabilidad y realizar su seguimiento.

- **Gobernanza y documentación**  
Definición de criterios básicos sobre fuentes de información, responsables, actualización de datos, tratamiento de reportes y documentación necesaria para el mantenimiento de la solución.

### 5.5.2 Alcance excluido

Quedan fuera del alcance del proyecto:

- Desarrollo o reemplazo completo de Boti, BAX u otros canales digitales existentes. La integración se limita a los mecanismos necesarios para utilizar la información y funcionalidades definidas por el proyecto.

- Reemplazo de los sistemas internos utilizados actualmente por las diferentes áreas de la Ciudad.

- Desarrollo de una aplicación de navegación vehicular o de un sistema equivalente a Waze. La funcionalidad de reportes se limita a la identificación, validación y seguimiento de incidencias georreferenciadas.

- Resolución automática de las incidencias reportadas. El proyecto contempla su registro, validación, derivación y seguimiento, pero no la ejecución física de las acciones necesarias para resolverlas.

- Incorporación de todas las fuentes de información existentes en la Ciudad. La integración se realizará sobre las fuentes seleccionadas durante la etapa de análisis.

- Desarrollo de funcionalidades comerciales, publicidad o monetización para usuarios finales, salvo que sean incorporadas posteriormente mediante una decisión formal de alcance.

- Implementación de funcionalidades de perfil personal avanzado o personalización basada en datos sensibles que no sean necesarias para los objetivos definidos.

- Expansión del proyecto a funcionalidades no relacionadas directamente con la integración geográfica, el acceso a información oficial y la gestión de incidencias ciudadanas.

### 5.5.3 Criterio general de alcance

El proyecto se considerará dentro de alcance cuando una funcionalidad contribuya directamente a alguno de los siguientes resultados:

- centralizar información geográfica oficial;

- facilitar su consulta desde diferentes canales;

- permitir reportar incidencias georreferenciadas;

- validar y mantener actualizados esos reportes;

- facilitar su seguimiento por parte de las áreas responsables.

Cualquier nueva funcionalidad que no contribuya directamente a estos resultados deberá ser evaluada como un cambio de alcance y, de corresponder, incorporada mediante el mecanismo de control de cambios definido para el proyecto.

## 5.6 Entregables principales

Como resultado del proyecto se prevé la generación de los siguientes entregables principales:

### 5.6.1 Capa geográfica común

Estructura geográfica centralizada que permita integrar, organizar y visualizar información proveniente de diferentes áreas y fuentes de la Ciudad.

**Incluye:**

- definición de la estructura geográfica;

- integración de fuentes seleccionadas;

- criterios de actualización;

- identificación de responsables de los datos;

- mecanismos básicos de control de calidad.

### 5.6.2 Integraciones con fuentes y canales digitales

Conjunto de integraciones necesarias para permitir el intercambio y consumo de información geográfica desde los sistemas y canales definidos dentro del alcance.

**Incluye:**

- APIs o mecanismos de intercambio seleccionados;

- integración con las fuentes oficiales priorizadas;

- integración con el Mapa Interactivo;

- integración con canales digitales seleccionados, incluyendo Boti y BAX, sujeta a validación técnica;

- documentación de las integraciones implementadas.

### 5.6.3 Módulo de reportes ciudadanos georreferenciados

Funcionalidad que permita a los vecinos registrar incidencias vinculadas a una ubicación determinada.

**Incluye:**

- creación de reportes;

- ubicación geográfica;

- categoría de incidencia;

- fecha y hora;

- información complementaria cuando corresponda;

- visualización del reporte en el mapa.

### 5.6.4 Sistema de validación colaborativa

Mecanismo mediante el cual otros usuarios puedan aportar información sobre una incidencia reportada.

**Incluye:**

- confirmación de una incidencia;

- indicación de que una incidencia continúa presente;

- indicación de que una incidencia ya no se encuentra presente;

- actualización del estado del reporte a partir de las interacciones recibidas.

### 5.6.5 Sistema de seguimiento de incidencias

Flujo de gestión que permita registrar la evolución de cada reporte desde su creación hasta su cierre.

**Estados principales previstos:**

**Reportado → Validado → Derivado → En gestión → Resuelto → Cerrado**

La definición definitiva de los estados podrá ajustarse durante la etapa de análisis y diseño, de acuerdo con los procesos de las áreas responsables.

### 5.6.6 Vista de gestión para áreas responsables

Interfaz básica destinada a las áreas de la Ciudad involucradas en la gestión de incidencias.

**Incluye:**

- consulta de reportes;

- visualización geográfica;

- filtrado por categoría y estado;

- seguimiento de incidencias;

- actualización del estado cuando corresponda.

### 5.6.7 Documentación técnica y funcional

Documentación necesaria para facilitar la implementación, operación y mantenimiento de la solución.

**Incluye:**

- documentación de arquitectura;

- documentación de APIs e integraciones;

- criterios de gobernanza de datos;

- descripción de funcionalidades;

- procedimientos básicos de operación y mantenimiento.

### 5.6.8 Plan de implementación y cierre

Conjunto de documentos y actividades necesarias para preparar la puesta en funcionamiento de la solución y realizar el cierre formal del proyecto.

**Incluye:**

- plan de implementación;

- documentación para las áreas involucradas;

- capacitación o transferencia de conocimientos cuando corresponda;

- registro de pruebas y resultados;

- evaluación inicial de funcionamiento;

- documentación de cierre del proyecto.

## 5.7 Criterios de éxito y aceptación

El éxito del proyecto se evaluará a partir del cumplimiento de los objetivos, entregables y condiciones definidas en el alcance. Los criterios permitirán verificar que la solución desarrollada sea funcional, integrable y utilizable por los actores involucrados.

### 5.7.1 Criterios de éxito

Se considerará que el proyecto alcanzó sus objetivos cuando se cumplan los siguientes criterios:

- **Integración de información geográfica**  
La solución deberá permitir integrar y visualizar información proveniente de las fuentes oficiales seleccionadas, utilizando una estructura geográfica común.

- **Disponibilidad multicanal**  
La información y las funcionalidades definidas para el proyecto deberán poder ser utilizadas desde el Mapa Interactivo y los canales digitales seleccionados, de acuerdo con las posibilidades técnicas de cada integración.

- **Funcionamiento del sistema de reportes**  
Los usuarios deberán poder generar reportes de incidencias asociados a una ubicación geográfica y a una categoría determinada.

- **Validación colaborativa**  
El sistema deberá permitir que otros usuarios interactúen con los reportes para confirmar su existencia o indicar que una incidencia ya no se encuentra presente.

- **Trazabilidad de las incidencias**  
Cada reporte deberá contar con un estado identificable y permitir registrar su evolución desde la creación hasta el cierre.

- **Acceso para las áreas responsables**  
Las áreas involucradas deberán disponer de una vista que permita consultar y realizar el seguimiento de los reportes correspondientes a su ámbito de responsabilidad.

- **Calidad y actualización de la información**  
Deberán estar definidos los responsables de las fuentes incorporadas, los criterios de actualización y los mecanismos básicos de control de calidad.

- **Documentación y transferencia**  
La solución deberá contar con documentación técnica y funcional suficiente para facilitar su implementación, operación y mantenimiento.

### 5.7.2 Criterios de aceptación

Los entregables serán considerados aceptados cuando hayan sido revisados y verificados mediante pruebas definidas durante las etapas de análisis y testing.

La aceptación deberá contemplar como mínimo:

- **Pruebas funcionales:** verificar que las funcionalidades respondan a los requerimientos definidos.

- **Pruebas de integración:** comprobar el correcto intercambio de información entre el mapa, las fuentes seleccionadas y los canales digitales involucrados.

- **Pruebas de reportes:** verificar la creación, geolocalización, visualización y actualización de incidencias.

- **Pruebas de validación:** comprobar el funcionamiento de los mecanismos de confirmación y actualización colaborativa.

- **Pruebas de seguimiento:** verificar que los estados de una incidencia puedan actualizarse y consultarse correctamente.

- **Pruebas de gestión:** comprobar que las áreas responsables puedan acceder a la información correspondiente y realizar el seguimiento definido.

- **Revisión de documentación:** verificar que la documentación técnica y funcional se encuentre completa y actualizada.

### 5.7.3 Condiciones de aceptación final

La aceptación final del proyecto estará condicionada a:

- cumplimiento del alcance aprobado;

- entrega de los componentes y documentos definidos;

- aprobación de las pruebas funcionales y de integración;

- resolución o aceptación formal de los defectos críticos identificados;

- disponibilidad de la documentación necesaria;

- validación por parte de los responsables definidos para el proyecto.

Los criterios específicos de rendimiento, disponibilidad, tiempos de respuesta y otros indicadores técnicos serán definidos durante la etapa de análisis, de acuerdo con los requerimientos no funcionales y las características de la solución.

## 5.8 Recursos y presupuesto preliminar

La ejecución del proyecto requerirá recursos humanos, tecnológicos y financieros destinados al desarrollo, integración, implementación y mantenimiento inicial de la solución.

### 5.8.1 Recursos humanos

El proyecto requerirá, como mínimo, la participación de los siguientes perfiles:

- Responsable o director del proyecto.

- Analistas funcionales.

- Desarrolladores de software.

- Especialistas en datos y APIs.

- Especialistas en sistemas de información geográfica.

- Diseñadores UX/UI.

- Especialistas en infraestructura y seguridad.

- Representantes de las áreas responsables de la información.

- Responsables de los canales digitales integrados.

- Personal destinado a pruebas y control de calidad.

- Personal de soporte y documentación.

La cantidad y dedicación de cada perfil será determinada durante la elaboración del cronograma y presupuesto detallado.

### 5.8.2 Recursos tecnológicos

Entre los principales recursos tecnológicos necesarios se consideran:

- Infraestructura para alojamiento de la solución.

- Bases de datos y servicios de almacenamiento.

- Servicios de mapas y georreferenciación.

- APIs y mecanismos de integración.

- Herramientas de desarrollo y testing.

- Sistemas de monitoreo y registro.

- Infraestructura necesaria para soportar los canales digitales integrados.

- Herramientas de seguridad y control de acceso.

### 5.8.3 Categorías de costos

El presupuesto detallado contemplará, como mínimo, las siguientes categorías:

| **Categoría** | **Conceptos principales** |
|---|---|
| **Desarrollo** | Análisis, programación, integración y testing |
| **Datos y GIS** | Procesamiento, almacenamiento y servicios geográficos |
| **Infraestructura** | Servidores, bases de datos y servicios tecnológicos |
| **Integraciones** | APIs, conexiones con fuentes y canales digitales |
| **Diseño y UX** | Investigación, diseño de interfaces y pruebas de usabilidad |
| **Seguridad** | Controles, auditorías y mecanismos de protección |
| **Implementación** | Puesta en funcionamiento, capacitación y soporte inicial |
| **Mantenimiento inicial** | Correcciones, monitoreo y ajustes posteriores a la implementación |
| **Gestión del proyecto** | Planificación, coordinación, seguimiento y documentación |

### 5.8.4 Modelo de financiamiento

La financiación principal del proyecto se considera inicialmente asociada al presupuesto destinado a la modernización de servicios digitales.

Adicionalmente, se podrá evaluar un modelo complementario de ingresos mediante la incorporación de servicios comerciales de terceros.

En una eventual etapa posterior, restaurantes, comercios y prestadores de servicios particulares podrían contratar espacios de **visibilidad patrocinada** dentro del mapa. Estos contenidos podrían mostrarse de acuerdo con criterios geográficos, por ejemplo, establecimientos ubicados en las proximidades del usuario.

La publicidad deberá diferenciarse claramente de la información oficial y no deberá alterar la información pública, los reportes ciudadanos ni los resultados de gestión.

Este modelo deberá ser evaluado en términos de:

- viabilidad económica;

- reglas de participación de los comercios;

- criterios de transparencia;

- diferenciación entre contenido oficial y patrocinado;

- protección de los datos de los usuarios;

- impacto sobre la experiencia de uso;

- mecanismos de control y moderación.

### 5.8.5 Presupuesto estimado de alto nivel

El presupuesto detallado se desarrolla en el punto 10. Como referencia de alto nivel, el proyecto estima una inversión total de **USD 241.839**, expresada en dólares estadounidenses a un tipo de cambio supuesto de ARS 1.560 por USD:

| **Categoría** | **Presupuesto estimado** |
|---|---|
| Recursos humanos | USD 121.790 |
| Desarrollo y tecnología | USD 22.435 |
| Datos, GIS e integraciones | USD 11.538 |
| Infraestructura y seguridad | USD 19.230 |
| Implementación y capacitación | USD 7.692 |
| Mantenimiento inicial | USD 17.948 |
| **Presupuesto base** | **USD 200.633** |
| Reserva de contingencia (valor esperado de los riesgos, punto 9.7) | USD 41.206 |
| **Presupuesto total estimado** | **USD 241.839** |

Los valores son estimativos y se ajustarán según el alcance aprobado y las cotizaciones al momento de ejecución.

### 5.8.6 Consideración sobre el alcance

La incorporación de publicidad y servicios patrocinados no formará parte del núcleo funcional de la primera implementación, salvo que sea aprobada expresamente como parte del alcance definitivo.

En caso de incorporarse, deberá tratarse como un componente específico del modelo de negocio y generar los correspondientes requerimientos, tareas, costos, riesgos y criterios de aceptación.

Como alternativa, podrá considerarse una **fase posterior de evolución del proyecto**, una vez validado el funcionamiento de la plataforma y su utilización por parte de vecinos, áreas de gobierno y usuarios comerciales.

## 5.9 Riesgos iniciales y gestión del cambio

### 5.9.1 Riesgos iniciales identificados

Durante la definición inicial del proyecto se identifican los siguientes riesgos iniciales. Estos riesgos se analizan, priorizan y amplían en la matriz de riesgos del punto 9, que incorpora los identificados durante la planificación:

| **Riesgo** | **Posible consecuencia** | **Respuesta inicial** |
|---|---|---|
| **Disponibilidad insuficiente de APIs o fuentes de datos** | Retrasos o imposibilidad de integrar determinadas fuentes | Relevar las fuentes durante la etapa de análisis y definir alternativas |
| **Baja calidad o actualización de los datos** | Información incorrecta o desactualizada para los usuarios | Establecer responsables, criterios de actualización y controles de calidad |
| **Dificultades de integración con canales existentes** | Retrasos en la disponibilidad multicanal | Realizar validaciones técnicas tempranas y pruebas de integración |
| **Falta de coordinación entre áreas** | Demoras en decisiones, requerimientos o validaciones | Definir responsables y mecanismos formales de comunicación |
| **Aumento del alcance** | Incremento de costos y plazos | Aplicar un mecanismo formal de control de cambios |
| **Baja participación ciudadana** | Pocos reportes o validaciones colaborativas | Diseñar una experiencia simple y mecanismos de incentivo al uso |
| **Reportes incorrectos o maliciosos** | Información poco confiable | Incorporar mecanismos de validación, moderación y seguimiento |
| **Problemas de rendimiento o disponibilidad** | Dificultades de acceso a la plataforma | Definir requerimientos técnicos y realizar pruebas de rendimiento |
| **Limitaciones presupuestarias** | Reducción o postergación de funcionalidades | Priorizar entregables y controlar costos durante el proyecto |
| **Riesgos relacionados con datos de usuarios** | Incumplimientos o pérdida de confianza | Minimizar datos recolectados y aplicar controles de seguridad y privacidad |
| **Baja adopción por parte de comercios** | Menores ingresos por servicios patrocinados | Evaluar el modelo comercial como una fase posterior y validar su aceptación |
| **Confusión entre contenido oficial y patrocinado** | Pérdida de claridad para los usuarios | Identificar visualmente los contenidos comerciales y establecer reglas de publicación |

### 5.9.2 Gestión de cambios

Debido a que el proyecto será desarrollado bajo una metodología en cascada, cualquier modificación significativa respecto del alcance aprobado deberá ser evaluada antes de su incorporación.

Una solicitud de cambio deberá analizar, como mínimo:

- impacto sobre el alcance;

- impacto sobre el cronograma;

- impacto sobre los costos;

- impacto sobre los recursos necesarios;

- impacto sobre los riesgos;

- impacto sobre los entregables;

- impacto sobre la calidad y los criterios de aceptación.

Los cambios podrán ser:

**Cambios menores:** aquellos que no alteren significativamente los objetivos, entregables, presupuesto o cronograma. Podrán ser gestionados dentro del equipo del proyecto según las responsabilidades definidas.

**Cambios significativos:** aquellos que modifiquen el alcance, agreguen funcionalidades importantes, impliquen nuevos actores o requieran recursos adicionales. Deberán contar con la evaluación y aprobación de los responsables correspondientes.

### 5.9.3 Control del alcance

Para evitar el crecimiento no planificado del proyecto, toda funcionalidad nueva deberá ser evaluada en relación con los objetivos definidos en este Charter.

En particular, funcionalidades como:

- publicidad y contenido patrocinado;

- nuevas categorías de reportes;

- nuevos canales digitales;

- incorporación de nuevas fuentes de datos;

- perfiles personalizados;

- funcionalidades comerciales;

deberán incorporarse únicamente cuando exista una decisión formal sobre su impacto y prioridad.

### 5.9.4 Evolución futura

La plataforma podrá evolucionar posteriormente hacia nuevas funcionalidades, siempre que estas sean compatibles con la arquitectura y los objetivos generales del proyecto.

Entre las posibles líneas de evolución se consideran:

- ampliación de fuentes de información;

- incorporación de nuevos canales digitales;

- nuevos tipos de reportes ciudadanos;

- mayor personalización de la información;

- servicios comerciales geolocalizados;

- recomendaciones de comercios y servicios;

- herramientas de análisis para las áreas de gobierno;

- nuevos mecanismos de participación ciudadana.

Estas funcionalidades se consideran oportunidades de evolución y no forman parte automáticamente del alcance de la primera implementación.

## 5.10 Supuestos y restricciones

### 5.10.1 Supuestos del proyecto

Para la planificación inicial del proyecto se consideran los siguientes supuestos:

- **Disponibilidad de información oficial**  
Las áreas seleccionadas pondrán a disposición las fuentes de información necesarias para la integración, de acuerdo con los permisos y mecanismos de acceso correspondientes.

- **Disponibilidad de APIs y servicios de intercambio**  
Se supone que las fuentes priorizadas cuentan con APIs u otros mecanismos técnicamente viables para permitir el intercambio de información requerido.

- **Participación de las áreas involucradas**  
Las áreas responsables de los datos y de la gestión de incidencias participarán en las etapas de análisis, validación, pruebas e implementación.

- **Disponibilidad de infraestructura tecnológica**  
Se contará con infraestructura suficiente para desarrollar, integrar, probar y poner en funcionamiento los componentes incluidos en el alcance.

- **Disponibilidad del equipo de proyecto**  
Los perfiles necesarios de gestión, tecnología, datos, diseño y comunicación estarán disponibles durante las etapas correspondientes.

- **Continuidad de los canales digitales seleccionados**  
Se supone que los canales digitales seleccionados para la integración estarán disponibles y contarán con mecanismos que permitan su vinculación con la solución, sujeto a validación técnica.

- **Participación de los vecinos**  
Se considera que los usuarios podrán aportar reportes y validaciones sobre incidencias de su entorno, generando información complementaria a las fuentes oficiales.

- **Disponibilidad de referencias geográficas comunes**  
Se supone que las fuentes seleccionadas pueden ser asociadas a una referencia geográfica común o adaptadas para su integración con la capa geográfica definida por el proyecto.

### 5.10.2 Restricciones del proyecto

El proyecto estará condicionado por las siguientes restricciones:

- **Alcance definido**  
El desarrollo deberá limitarse a las funcionalidades y componentes establecidos en el alcance aprobado, evitando incorporar funcionalidades que impliquen una ampliación no planificada.

- **Metodología de desarrollo**  
El proyecto será planificado y ejecutado bajo un enfoque de gestión en cascada, con etapas, entregables y puntos de aprobación definidos previamente.

- **Dependencia de sistemas externos**  
La integración con fuentes, APIs y canales digitales existentes dependerá de sus características técnicas, disponibilidad, permisos y condiciones de acceso.

- **Calidad y actualización de las fuentes**  
La solución dependerá de la calidad, frecuencia de actualización y disponibilidad de los datos proporcionados por las áreas responsables.

- **Presupuesto disponible**  
El desarrollo deberá realizarse dentro del presupuesto aprobado, considerando los costos de desarrollo, infraestructura, integración, mantenimiento inicial y demás recursos necesarios.

- **Plazos del proyecto**  
Las actividades deberán ejecutarse dentro del cronograma aprobado, respetando las dependencias entre etapas y los hitos establecidos.

- **Protección y tratamiento de datos**  
El diseño e implementación deberán contemplar las condiciones aplicables al tratamiento de datos de usuarios y reportes ciudadanos, evitando la incorporación de información que no resulte necesaria para los objetivos del proyecto.

- **Capacidad de los canales existentes**  
Las funcionalidades disponibles a través de canales como Boti y BAX estarán condicionadas por las capacidades técnicas y de integración que estos canales permitan.

### 5.10.3 Relación con la gestión de riesgos

Los supuestos y restricciones identificados deberán ser revisados durante la planificación y el seguimiento del proyecto, ya que cualquier cambio significativo puede afectar el alcance, el cronograma, los costos o la calidad de los entregables.

En particular, los siguientes aspectos serán considerados como fuentes potenciales de riesgo:

- falta de disponibilidad o cambios en las APIs;

- retrasos en la entrega de información por parte de las áreas;

- problemas de calidad o actualización de los datos;

- dificultades de integración con canales digitales existentes;

- disponibilidad limitada del equipo;

- cambios de alcance;

- restricciones presupuestarias;

- retrasos en las etapas de desarrollo, integración o pruebas.

## 5.11 Organización y roles iniciales del proyecto

El proyecto requiere la participación coordinada de perfiles de gestión, tecnología, datos, diseño y representantes de las áreas involucradas. La asignación detallada de responsables podrá ajustarse durante la planificación, pero se establecen inicialmente los siguientes roles:

### 5.11.1 Sponsor del proyecto

Responsable de brindar respaldo institucional al proyecto, validar sus objetivos generales y facilitar la disponibilidad de recursos y participación de las áreas involucradas.

**Responsabilidades principales:**

- aprobar los objetivos y el alcance general;

- facilitar la coordinación entre áreas;

- validar decisiones de alto nivel;

- aprobar cambios significativos de alcance, presupuesto o cronograma;

- participar en la aprobación de los principales hitos.

### 5.11.2 Director o responsable del proyecto

Responsable de la planificación, coordinación y seguimiento integral del proyecto.

**Responsabilidades principales:**

- elaborar y mantener el plan del proyecto;

- coordinar las diferentes etapas;

- realizar el seguimiento del cronograma;

- gestionar alcance, riesgos, recursos y costos;

- coordinar a los equipos involucrados;

- comunicar avances y desvíos;

- gestionar la aprobación de entregables.

**Autoridad asignada:**

- decidir sobre la planificación y la asignación operativa de los recursos del proyecto, dentro del alcance, el presupuesto y el cronograma aprobados;

- aprobar los cambios menores, según lo definido en 5.9.2;

- utilizar la reserva de contingencia ante riesgos que se materialicen, con registro y justificación (punto 10.8);

- elevar al Sponsor los cambios significativos y toda modificación del presupuesto total aprobado.

Los umbrales cuantitativos de estas atribuciones, por ejemplo el monto de contingencia que puede utilizar sin elevarlo al Sponsor, se definirán al aprobar el Charter [a confirmar].

### 5.11.3 Equipo de tecnología y desarrollo

Responsable del diseño técnico, desarrollo e integración de los componentes de la solución.

**Responsabilidades principales:**

- definir la arquitectura;

- desarrollar la capa geográfica;

- desarrollar el sistema de reportes y validación;

- implementar las integraciones;

- realizar pruebas técnicas;

- documentar los componentes desarrollados.

### 5.11.4 Equipo de datos y gobernanza

Responsable de analizar las fuentes de información y establecer criterios para su integración y mantenimiento.

**Responsabilidades principales:**

- relevar las fuentes disponibles;

- evaluar calidad y actualización de los datos;

- definir criterios de integración;

- establecer responsables de cada fuente;

- colaborar en la definición de estándares y controles de calidad;

- supervisar aspectos relacionados con la gobernanza de datos.

### 5.11.5 Equipo de diseño y experiencia de usuario

Responsable de diseñar la interacción de los usuarios con la solución y asegurar que las funcionalidades sean comprensibles y utilizables.

**Responsabilidades principales:**

- diseñar las interfaces;

- definir los flujos de consulta y reporte;

- incorporar las necesidades identificadas durante Design Thinking;

- realizar validaciones de usabilidad;

- colaborar en las pruebas con usuarios.

### 5.11.6 Representantes de las áreas de la Ciudad

Responsables de aportar conocimiento sobre los procesos, fuentes de información y gestión de incidencias correspondientes a cada área.

**Responsabilidades principales:**

- aportar información sobre procesos y sistemas existentes;

- validar requerimientos;

- identificar fuentes de datos relevantes;

- participar en las pruebas;

- validar el funcionamiento de las funcionalidades asociadas a su ámbito;

- colaborar en la definición de los circuitos de atención y cierre de incidencias.

### 5.11.7 Res.ponsables de canales digitales

Participantes vinculados con los canales seleccionados para la integración, como el Mapa Interactivo y los canales conversacionales definidos para el proyecto.

**Responsabilidades principales:**

- evaluar la factibilidad de las integraciones;

- definir mecanismos de intercambio de información;

- validar requerimientos técnicos;

- participar en las pruebas de integración;

- coordinar la implementación de los componentes correspondientes.

### 5.11.8 Usuarios y comunidad

Los vecinos constituyen los usuarios finales de la solución y, a través del sistema de reportes, también una fuente de información complementaria.

**Participación prevista:**

- consultar información georreferenciada;

- generar reportes;

- validar incidencias informadas por otros usuarios;

- aportar información sobre el estado de las incidencias;

- participar en pruebas de usabilidad cuando corresponda.

### 5.11.9 Estructura general de responsabilidad

La estructura inicial del proyecto puede representarse de la siguiente manera:

**Sponsor**  
↓  
**Responsable del proyecto**  
↓  
**Equipos especializados**  
→ Tecnología y desarrollo  
→ Datos y gobernanza  
→ Diseño y experiencia de usuario  
↓  
**Áreas responsables y canales digitales**  
↓  
**Usuarios y comunidad**

Esta estructura será utilizada como base para desarrollar posteriormente la matriz de stakeholders, donde se analizarán el nivel de interés, influencia, impacto y estrategia de comunicación de cada actor.

## 5.12 Cronograma e hitos principales

El proyecto se desarrollará bajo una metodología en cascada, organizando el trabajo en etapas secuenciales con entregables y puntos de aprobación definidos. El cronograma detallado será desarrollado posteriormente mediante el Gantt del proyecto.

### 5.12.1 Etapas principales

| **Etapa** | **Objetivo principal** | **Resultado esperado** |
|---|---|---|
| **1. Inicio** | Definir formalmente el proyecto, alcance, actores y condiciones iniciales | Proyecto definido y aprobado |
| **2. Análisis** | Relevar necesidades, fuentes, sistemas y requerimientos | Requerimientos funcionales y no funcionales |
| **3. Diseño** | Diseñar la arquitectura, capa geográfica y funcionalidades | Diseño funcional y técnico aprobado |
| **4. Desarrollo** | Construir los componentes definidos | Componentes desarrollados |
| **5. Integración** | Conectar fuentes, sistemas y canales seleccionados | Integraciones implementadas |
| **6. Pruebas** | Verificar funcionamiento, integración y usabilidad | Solución validada y correcciones realizadas |
| **7. Implementación** | Preparar y realizar la puesta en funcionamiento | Solución implementada |
| **8. Cierre** | Evaluar resultados, documentar y formalizar el cierre | Proyecto cerrado y documentación final |

### 5.12.2 Hitos principales

Se establecen inicialmente los siguientes hitos:

**Hito 1. Aprobación del Project Charter**  
Marca la aprobación formal del objetivo, alcance, entregables y condiciones generales del proyecto.

**Hito 2. Aprobación de requerimientos**  
Confirma las necesidades funcionales y no funcionales que deberán ser atendidas por la solución.

**Hito 3. Aprobación del diseño**  
Valida la arquitectura, la capa geográfica, el sistema de reportes y los mecanismos de integración.

**Hito 4. Finalización del desarrollo**  
Confirma que los componentes principales definidos en el alcance se encuentran construidos.

**Hito 5. Finalización de integraciones**  
Verifica que las fuentes y canales seleccionados se encuentren integrados de acuerdo con los requerimientos establecidos.

**Hito 6. Aprobación de pruebas**  
Confirma el cumplimiento de los criterios de aceptación y la resolución de los defectos críticos identificados.

**Hito 7. Puesta en funcionamiento**  
Marca la implementación de la solución en el entorno definido para su utilización.

**Hito 8. Cierre del proyecto**  
Formaliza la finalización del proyecto, incluyendo documentación, evaluación inicial y transferencia a los responsables de operación.

### 5.12.3 Dependencias principales

La planificación deberá respetar las siguientes dependencias:

**Inicio → Análisis → Diseño → Desarrollo → Integración → Pruebas → Implementación → Cierre**

Dentro de estas etapas podrán existir actividades paralelas cuando no exista una dependencia directa. Por ejemplo, determinadas tareas de diseño de la capa geográfica y del sistema de reportes podrán desarrollarse en paralelo una vez aprobados los requerimientos correspondientes.

La duración específica de cada etapa y actividad será definida en el Gantt, considerando recursos disponibles, dependencias técnicas, puntos de aprobación y posibles riesgos identificados.

## 5.13 Aprobación del Charter

**Requisitos de aprobación.** El Charter se considera aprobado (Gate 1 del punto 6.5, hito «Charter aprobado») cuando el Sponsor valida los objetivos, el alcance y los entregables (5.4 a 5.6), los criterios de éxito y aceptación (5.7), el presupuesto estimado de alto nivel (5.8.5), los riesgos iniciales (5.9) y el cronograma con sus 8 hitos (5.12). Con la aprobación se autoriza el inicio de la fase de análisis y se otorga al Director del proyecto la autoridad descrita en 5.11.2.

**Firmas.**

| **Rol** | **Nombre y apellido** | **Firma** | **Fecha** |
|---|---|---|---|
| Sponsor del proyecto | [a completar] |  |  |
| Director o responsable del proyecto | [a completar] |  |  |
