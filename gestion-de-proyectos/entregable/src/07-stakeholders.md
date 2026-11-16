# 7. Matriz de stakeholders

Para ejecutar las actividades del Gantt y asegurar la adopción de la plataforma, se identifican los actores que pueden afectar el proyecto, verse afectados por él o decidir sobre él, y se define cómo gestionar a cada uno según su interés e influencia.

## 7.1 Identificación y análisis

| Stakeholder | Tipo | Interés | Influencia | Estrategia |
|---|---|---|---|---|
| Sponsor institucional de Modernización de CABA | Interno | Alto | Alto | Gestionar de cerca |
| Project Manager | Interno | Alto | Alto | Gestionar de cerca |
| Equipo de Tecnología y Desarrollo | Interno | Alto | Alto | Gestionar de cerca |
| Equipo de Datos y GIS | Interno | Alto | Alto | Gestionar de cerca |
| USIG e Innovación/ASI (geocodificador, APIs y estándares) | Interno | Alto | Alto | Gestionar de cerca |
| Áreas dueñas del dato: Secretaría de Transporte (Movilidad) y Ministerio de Cultura | Interno | Alto | Alto | Gestionar de cerca |
| Responsables de canales (Boti, BAX, miBA) | Interno | Alto | Alto | Gestionar de cerca |
| Hacienda / Presupuesto | Interno | Medio | Alto | Mantener satisfechos |
| Comunas y áreas operativas de CABA | Interno | Alto | Medio | Mantener informados |
| Equipo UX/UI | Interno | Alto | Medio | Mantener informados |
| Comunicación institucional | Interno | Alto | Medio | Mantener informados |
| Vecinos y usuarios de la plataforma (reportan y validan) | Externo | Alto | Medio | Mantener informados |
| Prestadores de transporte público | Externo | Medio | Medio | Mantener informados |
| Proveedores tecnológicos | Externo | Medio | Medio | Mantener informados |
| Socios con oferta geolocalizada (Banco Ciudad, Pase Cultural, DisfrutemosBA) | Externo | Medio | Bajo | Monitorear |

## 7.2 Clasificación por interés e influencia

- **Alta influencia / alto interés (gestionar de cerca):** Sponsor institucional, Project Manager, equipos de Tecnología y Desarrollo y de Datos y GIS, USIG/ASI, áreas dueñas del dato (Transporte y Cultura) y responsables de canales. Participan en decisiones, validaciones, seguimiento y resolución de bloqueos.
- **Alta influencia / interés medio (mantener satisfechos):** Hacienda/Presupuesto. Define la partida que financia la plataforma, pero no participa del día a día. Se le informa de costos y desvíos.
- **Influencia media / alto interés (mantener informados):** comunas y áreas operativas, UX/UI, Comunicación institucional y vecinos/usuarios. Requieren información frecuente, participación y retroalimentación.
- **Influencia media / interés medio (mantener informados):** prestadores de transporte público y proveedores tecnológicos, cuya participación depende de integraciones y actividades específicas.
- **Baja influencia / interés medio (monitorear):** socios con oferta geolocalizada, que se incorporan mediante convenios y no son necesarios para el alcance inicial.

El siguiente gráfico ubica a cada stakeholder de la matriz según su interés y su influencia.

![Matriz de interés e influencia de los stakeholders](img/stakeholders.png)

## 7.3 Stakeholders críticos

Son aquellos sin los cuales el proyecto no puede avanzar:

- **Sponsor institucional y Hacienda:** aprueban las decisiones relevantes y sostienen el financiamiento.
- **Project Manager:** coordina cronograma, cambios, riesgos y articulación entre equipos.
- **Tecnología y USIG/ASI:** construyen la plataforma, el geocodificador y las integraciones.
- **Datos y GIS:** desarrollan la capa geográfica común y aseguran la calidad de los datos.
- **Transporte y Cultura:** aportan y validan la información de sus áreas.
- **Responsables de canales:** definen la factibilidad de integrar Boti, BAX y miBA.
- **Vecinos y usuarios:** son los destinatarios principales y alimentan los reportes y validaciones.

## 7.4 Relación con el Canvas y el alcance

La matriz está alineada con el Canvas y el Project Charter, y ampliada con los actores identificados en el análisis de stakeholders: incluye a las áreas dueñas del dato, a USIG e Innovación/ASI, a los canales (Boti, BAX, miBA) y a Hacienda, de quien depende el ingreso principal del proyecto. Transporte y Cultura se destacan por ser las fuentes de datos priorizadas; otras áreas dueñas del dato, como Educación, Salud y Espacio Público, se incorporan con el mismo tratamiento. Los socios con oferta geolocalizada (Banco Ciudad, Pase Cultural, DisfrutemosBA) son un tercer lado opcional que se suma mediante convenios; si se concretan, pasan a «gestionar de cerca». Sus contenidos deberán diferenciarse de la información oficial, y el vecino nunca paga por el servicio.
