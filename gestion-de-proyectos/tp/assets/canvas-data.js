/* ═══════════════════════════════════════════════════════════════════
   Canvas data — SINGLE SOURCE OF TRUTH for the 4 business-model options.

   Used by:
   - tp/canvas-taller.html (interactive workshop, loads this file)
   - compartir/ deliverable (tools/build-compartir.sh inlines this file)

   To change content: edit this file, then run
     tools/build-compartir.sh      (rebuilds compartir/tp-cascada-canvas-y-partes.html)
     tools/test-compartir.sh       (checks that every option still has all 9 blocks)
   Keep every option filled for all 9 blocks; keep option ids a, b, c, d stable.
   Must not contain a closing script tag (it is inlined into an HTML page).
   Works as a browser global (window.CANVAS_DATA) and as a Node module.
   ═══════════════════════════════════════════════════════════════════ */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.CANVAS_DATA = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var data = {
    meta: {
      title: 'Modelo Canvas — Mapa Interactivo de la Ciudad',
      source: 'Clase 1 — Modelo Canvas (Business Model Canvas, Osterwalder & Pigneur).'
    },
    order: [
      'segmentos',
      'pv',
      'canales',
      'relacion',
      'ingresos',
      'recursos',
      'actividades',
      'socios',
      'costos'
    ],
    blocks: {
      pv: {
        n: 1,
        name: 'Propuesta de valor',
        def: 'Conjunto de productos y servicios que crean valor para un segmento de mercado específico. Es la razón por la cual los clientes eligen una empresa en vez de otra.',
        questions: [
          '¿Qué problema del cliente estamos ayudando a resolver?',
          '¿Qué necesidad estamos satisfaciendo?',
          '¿Qué paquetes de productos o servicios ofrecemos a cada segmento de clientes?'
        ],
        types: [
          'Elementos que crean valor: precio, diseño, personalización, ahorro, novedad, marca y reputación',
          'Se desarma en 6 partes: ver el mapa de valor más abajo'
        ],
        src: 'Clase 1, p7–9'
      },
      segmentos: {
        n: 2,
        name: 'Segmentos de mercado',
        def: 'Los diferentes grupos de personas o empresas a los que una organización busca alcanzar y servir.',
        questions: ['¿Para quién estamos creando valor?', '¿Quiénes son nuestros clientes más importantes?'],
        types: [
          'Mercado masivo',
          'Nicho de mercado',
          'Mercado segmentado',
          'Plantilla útil: [quiénes] que [situación] y hoy [dolor]',
          'El ejemplo de la cátedra sugiere priorizar 1 o 2 segmentos'
        ],
        src: 'Clase 1, p11 · Ejemplo Clase, p5'
      },
      canales: {
        n: 3,
        name: 'Canales',
        def: 'Cómo la organización alcanza e interactúa con sus segmentos de mercado para entregar una propuesta de valor. Son puntos de contacto.',
        questions: [
          '¿A través de qué canales prefieren los clientes ser alcanzados?',
          '¿Cómo estamos integrando nuestros canales?'
        ],
        types: [
          'Fase 1 · dar a conocer los productos y servicios',
          'Fase 2 · ayudar a evaluar la propuesta de valor',
          'Fase 3 · permitir comprar o acceder',
          'Fase 4 · entregar la propuesta de valor',
          'Fase 5 · ofrecer atención posventa'
        ],
        src: 'Clase 1, p13–14'
      },
      relacion: {
        n: 4,
        name: 'Relación con el cliente',
        def: 'Los tipos de relaciones que una empresa establece con un segmento de mercado específico, y cómo serán gestionados.',
        questions: [
          '¿Qué tipo de relación esperan nuestros clientes que establezcamos con ellos?',
          '¿Cómo se integran estas relaciones con el resto del modelo de negocio?',
          '¿De qué forma prefieren comunicarse nuestros clientes?'
        ],
        types: [
          'Asistencia personal: hay un representante real',
          'Asistencia personal dedicada: un ejecutivo específico',
          'Autoservicio: se le dan los medios para que se ayude a sí mismo',
          'Comunidades: se facilita la conexión entre clientes y con la empresa'
        ],
        src: 'Clase 1, p16'
      },
      ingresos: {
        n: 5,
        name: 'Modelo de ingresos',
        def: 'Cómo una empresa obtiene dinero de cada uno de sus segmentos de clientes: de qué manera cobra y cómo monetiza su propuesta de valor.',
        questions: [
          '¿Qué valor están dispuestos a pagar nuestros clientes?',
          '¿Cómo prefieren pagar? (pago único, suscripción, cuotas)',
          '¿Cuánto están dispuestos a pagar?'
        ],
        types: [
          'Venta de bienes',
          'Suscripciones',
          'Licencias',
          'Publicidad',
          'Comisiones',
          'Freemium',
          'Alquileres'
        ],
        src: 'Clase 1, p18'
      },
      recursos: {
        n: 6,
        name: 'Recursos clave',
        def: 'Los activos esenciales que la empresa necesita para entregar su propuesta de valor, alcanzar a sus clientes, mantener relaciones y generar ingresos.',
        questions: [
          '¿Qué recursos necesitamos para entregar nuestra propuesta de valor?',
          '¿Qué recursos son esenciales para mantener las relaciones con los clientes?',
          '¿Cómo obtendremos y mantendremos estos recursos?'
        ],
        types: [
          'Físicos: fábricas, vehículos, máquinas, sistemas',
          'Intelectuales: marcas, conocimiento, patentes, derechos de autor',
          'Financieros: dinero en efectivo, líneas de crédito',
          'Humanos: perfiles creativos, intensivos en conocimiento, científicos'
        ],
        src: 'Clase 1, p20–21'
      },
      actividades: {
        n: 7,
        name: 'Actividades clave',
        def: 'Las acciones más importantes que una empresa debe realizar para que su modelo de negocio funcione adecuadamente.',
        questions: [
          '¿Qué actividades pueden ser subcontratadas y cuáles deben mantenerse propias?'
        ],
        types: [
          'Producción de bienes: empresas industriales',
          'Solución de problemas: empresas de servicios',
          'Plataforma: empresas que brindan servicios de plataforma'
        ],
        src: 'Clase 1, p23'
      },
      socios: {
        n: 8,
        name: 'Socios clave',
        def: 'La red de proveedores y socios que no puedo reemplazar fácilmente, y que hacen que nuestro modelo de negocio funcione adecuadamente.',
        questions: [
          '¿Qué actividades clave o recursos no podemos realizar internamente y necesitamos de socios externos?',
          '¿Cómo afectan estos socios a nuestra estructura de costos y nuestras fuentes de ingresos?'
        ],
        types: [
          'Motivo 1: asegurar la disponibilidad de recursos',
          'Motivo 2: reducción de riesgo',
          'Motivo 3: optimizar economías de escala'
        ],
        src: 'Clase 1, p25'
      },
      costos: {
        n: 9,
        name: 'Estructura de costos',
        def: 'Todos los costos incurridos para poder operar el modelo de negocios diseñado en los pasos anteriores.',
        questions: [
          '¿Cuáles son nuestros costos fijos y variables?',
          '¿Cómo afectan estos costos a nuestra estructura de precios y rentabilidad?',
          '¿Qué oportunidades existen para reducir costos sin comprometer la calidad o la propuesta de valor?'
        ],
        types: [
          'Fijos: constantes sin importar el nivel de actividad (alquiler, sueldos fijos, seguros)',
          'Variables: cambian con el nivel de actividad (insumos, costo por unidad, comisiones)',
          'Impulsado por el costo (aerolínea low cost) frente a impulsado por el valor (autos de lujo)'
        ],
        src: 'Clase 1, p27–28'
      }
    },
    options: {
      a: {
        name: 'Servicio público enfocado',
        idea: 'El Mapa se moderniza para resolver un dolor concreto de un grupo de vecinos. Un solo segmento, sin ingreso comercial: el modelo se financia con presupuesto y se justifica por el servicio que presta.',
        cliente: 'Un segmento de vecinos de CABA',
        paga: 'El GCBA, con partida presupuestaria',
        borde: 'Todo mira hacia afuera: el vecino es el cliente y el GCBA es el sponsor que financia.',
        riesgo: 'Van a preguntar por los ingresos. Hay que sostener que un proyecto público se mide por servicio prestado, no por facturación.',
        blocks: {
          segmentos: [
            'Hogares con chicos en edad escolar en CABA que hoy se enteran tarde de la inscripción o la vacunación.',
            'Secundario: el GCBA como sponsor que financia y decide.',
            'Descartados por ahora: turistas, comercios, “toda la población”.'
          ],
          pv: [
            'Saber qué le corresponde a cada vecino en su cuadra, sin tener que saber de antemano qué preguntar ni a qué organismo.',
            'Perfil por hogar: el Mapa avisa (inscripción, vacunación, obra en la vereda) en lugar de esperar la consulta.',
            'Un solo lugar, en vez de un trámite por organismo.'
          ],
          canales: [
            'mapa.buenosaires.gob.ar, el canal actual (v4.1).',
            'Boti, el WhatsApp de la Ciudad.',
            'miBA y notificaciones del perfil.',
            'El 147 como canal de respaldo.'
          ],
          relacion: [
            'Autoservicio: el vecino resuelve solo, con la información encima del mapa.',
            'Proactiva: la notificación llega sin que la pida.',
            'Comunidad: el reclamo queda visible en el mapa con su estado.'
          ],
          ingresos: [
            'Sin ingreso comercial. Financiación: partida presupuestaria del GCBA.',
            'El retorno se mide, no se factura: menos consultas al 147 y más trámites autogestionados.',
            'Es un modelo impulsado por el valor público, no por el precio.'
          ],
          recursos: [
            'Intelectuales: las 14 APIs oficiales del GCBA, BA Data y el geocodificador de USIG.',
            'Intelectuales: la marca “Mapa de la Ciudad”, ya instalada.',
            'Humanos: equipo de producto, desarrollo y diseño.',
            'Financieros: la partida asignada al proyecto.'
          ],
          actividades: [
            'Integrar las APIs de las áreas dueñas del dato.',
            'Diseñar y sostener el perfil por hogar.',
            'Curar las capas temáticas: que el dato esté al día.',
            'Operar el loop de reclamos de punta a punta.'
          ],
          socios: [
            'Áreas dueñas del dato: Educación, Salud, Espacio Público, Movilidad.',
            'USIG, por el geocodificador y la normalización de direcciones.',
            'El equipo de Boti, para llegar por WhatsApp.'
          ],
          costos: [
            'Fijo: sueldos del equipo, el rubro de mayor peso.',
            'Variable: infraestructura cloud y servicio de mapas, por uso.',
            'Fijo: licencias y herramientas.',
            'Por única vez: comunicación del lanzamiento.'
          ]
        },
        flow: [
          ['Sección 4', 'Design Thinking', 'Entrevistás a familias de ese segmento. El problema a validar es uno solo y ya está escrito.'],
          ['Sección 5', 'Project Charter', 'Alcance corto y nítido. El objetivo SMART mide adopción del segmento, no facturación.'],
          ['Sección 6', 'Gantt', 'Pocas integraciones: 3 o 4 capas. El camino crítico pasa por el acuerdo de datos con cada área.'],
          ['Sección 7', 'Stakeholders', 'Pocos, y casi todos internos. La matriz poder-interés queda simple.'],
          ['Sección 9', 'Riesgos', 'El riesgo grande es que un área no entregue el dato a tiempo. Datos personales aparece, pero acotado.'],
          ['Sección 10', 'Presupuesto', 'Sueldos por la duración del Gantt, más cloud. No hay ingresos que proyectar.']
        ]
      },
      b: {
        name: 'Plataforma multilateral',
        suggested: true,
        idea: 'El Mapa crea valor para dos lados distintos al mismo tiempo: el vecino que lo usa y el área de gobierno que lo paga. Osterwalder llama a esto plataforma multilateral, y exige una propuesta de valor por lado.',
        cliente: 'Dos: el vecino elegido y las áreas de gobierno',
        paga: 'GCBA por presupuesto, más convenios con socios',
        borde: 'El borde deja de ser un problema: el lado vecino es la parte externa y el lado áreas es la interna. El Canvas los muestra como dos segmentos rotulados.',
        riesgo: 'Dos propuestas de valor en una sola hoja. Hay que rotularlas bien para que no se lea como desorden.',
        blocks: {
          segmentos: [
            'Lado externo, principal: hogares de la Ciudad, que hoy se enteran tarde de lo que les corresponde.',
            'Beneficiarios secundarios: visitantes y turistas, que consultan el mismo mapa sin reportar.',
            'Lado interno: áreas que hoy mantienen su propio mapa (Educación, Salud, Espacio Público, Movilidad).',
            'Tercer lado, opcional: socios con oferta geolocalizada (Banco Ciudad, Pase Cultural).'
          ],
          pv: [
            'Al vecino: enterarse de lo que le corresponde en su cuadra, sin saber qué preguntar ni a quién.',
            'Al área de gobierno: la vista de gestión —dónde se concentran los reclamos— y una capa geográfica lista para consumir en vez de reconstruirla.',
            'Al socio: llegar al vecino geolocalizado, dentro de un canal oficial.',
            'Son dos propuestas porque son dos segmentos: quien usa no es quien paga.'
          ],
          canales: [
            'Al vecino: web del mapa, Boti, miBA y notificaciones.',
            'Al área: API pública documentada y panel de gestión.',
            'Al socio: convenio y espacio en la capa de beneficios.',
            'Los tres integrados sobre la misma capa de datos.'
          ],
          relacion: [
            'Vecino: autoservicio más comunidad (reclamos con estado visible).',
            'Área de gobierno: asistencia dedicada, un referente técnico por área.',
            'Socio: relación contractual, por convenio.'
          ],
          ingresos: [
            'Principal: presupuesto del GCBA asignado a la plataforma.',
            'Costos evitados: cada área que deja de mantener su mapa libera presupuesto. Es el argumento más fuerte frente al sponsor.',
            'Convenios con socios: comisiones y canjes son fuentes válidas según la cátedra.',
            'Al vecino no se le cobra nunca.'
          ],
          recursos: [
            'Intelectuales: el geocodificador, las 14 APIs y BA Data.',
            'Intelectuales: la marca “Mapa de la Ciudad”.',
            'Humanos: equipo de plataforma más un rol de gestión de convenios.',
            'Financieros: la partida y el compromiso plurianual.'
          ],
          actividades: [
            'Construir y versionar la capa geográfica como producto: es una actividad de plataforma.',
            'Diseñar el perfil por hogar y el loop de reclamos.',
            'Gestionar los acuerdos de datos con cada área.',
            'Negociar y administrar los convenios con socios.'
          ],
          socios: [
            'Las áreas dueñas del dato: son socias y clientas al mismo tiempo.',
            'USIG e Innovación / ASI, por infraestructura y estándares.',
            'Boti y DisfrutemosBA, canales que consumen la capa.',
            'Banco Ciudad y Pase Cultural, para la capa de beneficios.'
          ],
          costos: [
            'Fijo: equipo de plataforma.',
            'Variable: infraestructura y servicio de mapas, crece con el uso.',
            'Fijo: gobierno del dato, el precio de ser plataforma.',
            'Variable: costo de gestionar convenios.'
          ]
        },
        flow: [
          ['Sección 4', 'Design Thinking', 'Dos investigaciones: vecinos y también empleados de las áreas. Más trabajo, bastante mejor historia.'],
          ['Sección 5', 'Project Charter', 'Objetivos SMART por lado: adopción del vecino y adopción interna de la capa.'],
          ['Sección 6', 'Gantt', 'Dos frentes: producto para el vecino y API para las áreas. El camino crítico suele pasar por la API.'],
          ['Sección 7', 'Stakeholders', 'La matriz se llena sola: internos con mucho poder, vecinos con mucho interés y poco poder.'],
          ['Sección 9', 'Riesgos', 'Los tres riesgos jugosos: datos personales (Ley 25.326), que un área no adopte la capa, y dependencia de terceros.'],
          ['Sección 10', 'Presupuesto', 'Dos frentes y una reserva de contingencia más grande, justificada por los EMV de la matriz.']
        ]
      },
      c: {
        name: 'Capa de identidad geográfica',
      tag: 'B2G',
        idea: 'El producto no es la web: es la capa. Una sola identidad geográfica para toda la Ciudad, que cada área consume en lugar de mantener su propio mapa. El cliente es el Estado; el vecino es beneficiario final.',
        cliente: 'Áreas de gobierno y otros productos del GCBA',
        paga: 'Presupuesto central más costo compartido por área',
        borde: 'Todo es interno. Es la opción que responde la pregunta del equipo de la forma más limpia: en este Canvas no hay lado externo.',
        riesgo: 'Se pierde la cara visible del proyecto. El Design Thinking se hace con empleados públicos, no con vecinos, y eso hay que anunciarlo de entrada.',
        blocks: {
          segmentos: [
            'Áreas que hoy mantienen mapas propios: Educación, Salud, Espacio Público, Movilidad.',
            'Productos del GCBA que necesitan geo: Boti, DisfrutemosBA, miBA.',
            'Atención Ciudadana (147), que necesita ubicar cada consulta.',
            'El vecino no es cliente en este modelo: es beneficiario final.'
          ],
          pv: [
            'Una sola identidad geográfica para toda la Ciudad: una dirección significa lo mismo en todos los sistemas.',
            'Que cada área deje de construir y mantener su propio mapa.',
            'Una sola capa de obras, reclamos y equipamiento, versionada y con soporte.'
          ],
          canales: [
            'API y SDK documentados.',
            'Catálogo interno de capas y datasets.',
            'Comité de datos: la mesa donde se acuerda qué se publica.',
            'Onboarding técnico área por área.'
          ],
          relacion: [
            'Asistencia personal dedicada: un referente técnico asignado por área.',
            'Acuerdos de nivel de servicio: disponibilidad y frescura del dato.',
            'Comunidad de práctica entre las áreas que consumen la capa.'
          ],
          ingresos: [
            'Presupuesto central de la Secretaría que opera la plataforma.',
            'Costo compartido: cada área aporta una parte por consumir la capa.',
            'El valor económico real es el ahorro por no duplicar desarrollos, y hay que estimarlo con número.'
          ],
          recursos: [
            'Intelectuales: el geocodificador de USIG, el activo central del modelo.',
            'Intelectuales: BA Data y las 14 APIs publicadas.',
            'Humanos: equipo de plataforma y de gobierno del dato.',
            'Físicos: la infraestructura donde corre la capa.'
          ],
          actividades: [
            'Normalizar direcciones y mantener el geocodificador.',
            'Publicar, versionar y documentar APIs.',
            'Gobernar el dato: quién es dueño de qué y con qué frescura.',
            'Migrar área por área desde su mapa propio.'
          ],
          socios: [
            'USIG, dueña histórica de la información geográfica de la Ciudad.',
            'Innovación / ASI, por infraestructura y estándares.',
            'Las áreas dueñas del dato: socias y clientas a la vez.'
          ],
          costos: [
            'Fijo: equipo de plataforma y de datos.',
            'Fijo: gobierno del dato, comités y documentación.',
            'Variable: infraestructura, por volumen de consultas a la API.',
            'Por única vez: la migración de cada área.'
          ]
        },
        flow: [
          ['Sección 4', 'Design Thinking', 'La investigación se hace con empleados de las áreas: el usuario es quien integra la capa.'],
          ['Sección 5', 'Project Charter', 'El alcance es técnico: qué áreas migran en esta fase y qué APIs se publican.'],
          ['Sección 6', 'Gantt', 'Gantt de migración, área por área. El camino crítico es el geocodificador: sin él no migra nadie.'],
          ['Sección 7', 'Stakeholders', 'Es el corazón del TP: todos internos, todos con poder real de bloquear.'],
          ['Sección 9', 'Riesgos', 'El riesgo dominante es de adopción: que un área no quiera dejar su mapa. Político, no técnico.'],
          ['Sección 10', 'Presupuesto', 'Equipo fijo más infraestructura por consumo. Hay que estimar el ahorro para justificarlo.']
        ]
      },
      d: {
        name: 'Ecosistema con beneficios',
        idea: 'El Mapa deja de ser sólo información y pasa a mostrar qué hay y qué beneficios hay a diez cuadras. Es la única opción que responde de frente la pregunta de los ingresos, y la que más riesgo trae.',
        cliente: 'Vecino consumidor, más comercios y Banco Ciudad',
        paga: 'Comisiones, espacios destacados y convenios',
        borde: 'El borde se corre hacia afuera: entran actores privados al Canvas. Hay que decir explícitamente qué dato nunca sale del Estado.',
        riesgo: 'Publicidad sobre un activo público, y el perfil por hogar implica datos personales (Ley 25.326). Es material de PESTEL y de matriz de riesgos.',
        blocks: {
          segmentos: [
            'Vecinos que consumen en su barrio y buscan qué hacer cerca.',
            'Comercios de proximidad e instituciones culturales con oferta local.',
            'Banco Ciudad y Pase Cultural, socios con beneficios propios.'
          ],
          pv: [
            'Al vecino: descubrir qué hay y qué beneficios le corresponden a diez cuadras, en el mismo mapa donde ya busca cómo llegar.',
            'Al comercio: visibilidad geolocalizada dentro de un canal oficial de la Ciudad.',
            'Al socio: llegar con su beneficio en el momento y el lugar en que el vecino decide.'
          ],
          canales: [
            'Web del mapa y Boti, que ya acumula más de 26 millones de conversaciones.',
            'DisfrutemosBA para la oferta cultural.',
            'Autogestión para que el comercio cargue y actualice su oferta.'
          ],
          relacion: [
            'Vecino: autoservicio, con recomendación según el perfil.',
            'Comercio: autoservicio con soporte.',
            'Socio grande: asistencia dedicada y convenio.'
          ],
          ingresos: [
            'Comisión por beneficio canjeado.',
            'Espacios destacados dentro de las capas temáticas.',
            'Convenios con Banco Ciudad y Pase Cultural.',
            'Licencia de la capa geográfica a terceros.',
            'Al vecino no se le cobra: rompería la legitimidad del canal.'
          ],
          recursos: [
            'Intelectuales: el perfil del vecino, el activo más valioso y el más delicado.',
            'Intelectuales: la marca oficial de la Ciudad, que es lo que hace confiable al beneficio.',
            'Humanos: equipo comercial y de alianzas, que hoy no existe.',
            'Físicos: la plataforma y el sistema de canje.'
          ],
          actividades: [
            'Captar y sostener la oferta de comercios.',
            'Operar el sistema de canje y su liquidación.',
            'Segmentar y personalizar sin cruzar la línea legal.',
            'Auditar qué se publica con marca oficial.'
          ],
          socios: [
            'Banco Ciudad, socio financiero y de beneficios.',
            'Pase Cultural y el sector cultural.',
            'Cámaras de comercio y centros comerciales a cielo abierto.',
            'Medios de pago, para el canje.'
          ],
          costos: [
            'Fijo: equipo comercial y de alianzas.',
            'Variable: costo de adquisición de comercios.',
            'Fijo: cumplimiento legal, auditoría y protección de datos.',
            'Variable: infraestructura y sistema de canje.'
          ]
        },
        flow: [
          ['Sección 4', 'Design Thinking', 'Dos usuarios a investigar: el vecino que canjea y el comercio que publica.'],
          ['Sección 5', 'Project Charter', 'Necesita una restricción explícita: qué dato personal no se usa nunca. Si no está, la defensa se cae.'],
          ['Sección 6', 'Gantt', 'Más largo: además del producto hay que sumar convenios y sistema de canje.'],
          ['Sección 7', 'Stakeholders', 'Aparecen externos con poder: cámaras, medios y la autoridad de protección de datos.'],
          ['Sección 9', 'Riesgos', 'Es la sección estrella: Ley 25.326, percepción de favorecer comercios, dependencia del socio.'],
          ['Sección 10', 'Presupuesto', 'El único con ingresos proyectados. También el que necesita la reserva de contingencia más alta.']
        ]
      }
    },
    comparison: [
      {
        id: 'a',
        segmento: 'Un grupo de vecinos con un dolor concreto',
        plata: 'Partida presupuestaria del GCBA. Sin ingreso comercial.',
        trabajo: {
          texto: 'Bajo',
          nivel: 'ok'
        },
        pregunta: '“¿Un modelo de negocio sin ingresos?”',
        conviene: 'El equipo quiere entregar seguro y a tiempo.'
      },
      {
        id: 'b',
        segmento: 'Vecino y área de gobierno (dos lados)',
        plata: 'Presupuesto + costos evitados + convenios con socios',
        trabajo: {
          texto: 'Medio',
          nivel: 'mid'
        },
        pregunta: '“¿Por qué dos propuestas de valor?”',
        conviene: 'Quieren la nota alta y tienen las tres semanas.'
      },
      {
        id: 'c',
        segmento: 'Áreas de gobierno (B2G interno)',
        plata: 'Presupuesto central + costo compartido por área',
        trabajo: {
          texto: 'Medio',
          nivel: 'mid'
        },
        pregunta: '“¿Y dónde queda el vecino?”',
        conviene: 'Les interesa más la arquitectura que la UX.'
      },
      {
        id: 'd',
        segmento: 'Vecino consumidor + comercios y Banco Ciudad',
        plata: 'Comisiones, espacios destacados, convenios',
        trabajo: {
          texto: 'Alto',
          nivel: 'bad'
        },
        pregunta: '“¿Publicidad en un servicio público? ¿Y la Ley 25.326?”',
        conviene: 'Quieren lucirse en riesgos y PESTEL, y saben defenderlo.'
      }
    ],
    recommendation: {
      titulo: 'Opción B, pero con el segmento de la A.',
      texto: 'Es decir: Canvas multilateral (vecino + GCBA), con un solo segmento de vecinos elegido y nombrado con nombre y apellido. Y mencionar C y D en una línea como alternativas evaluadas y descartadas. Eso vale doble: arregla el problema de foco del borrador y, en la defensa, muestra que hubo criterio y no una sola idea.'
    },
    valueMaps: {
      vecino: {
        who: 'hogares con chicos en edad escolar',
        tareas: [
          'Inscribir a los chicos en la escuela en la fecha que corresponde.',
          'Llevar el calendario de vacunación al día.',
          'Llegar a la escuela, al centro de salud y al trabajo todos los días.',
          'Reclamar cuando algo de la cuadra está roto.'
        ],
        frust: [
          'Hay que saber de antemano qué preguntar, a qué organismo y en qué canal.',
          'Se enteran tarde de lo que tenía fecha de cierre.',
          'Un trámite por organismo, cada uno con su propia web.',
          'El reclamo se hace y después no se sabe qué pasó.'
        ],
        benef: [
          'Que le avisen antes, sin tener que preguntar.',
          'Ver todo lo de su cuadra en un solo lugar.',
          'Saber en qué estado está su reclamo.',
          'Confiar en que el dato es el oficial y está al día.'
        ],
        pv: [
          'El Mapa le dice al vecino qué le corresponde en su cuadra, sin que tenga que saber qué preguntar.',
          'Perfil por hogar: lo que aparece depende de dónde vive el vecino y de con quién.',
          'Reclamos con estado visible sobre el mapa.'
        ],
        alivio: [
          'Aviso proactivo por fecha y por zona: ataca directo el “me enteré tarde”.',
          'Un solo lugar, en vez de un organismo por trámite.',
          'El reclamo con estado en el mapa cierra el loop que hoy queda abierto.',
          'Dato oficial, con fecha de actualización a la vista.'
        ],
        satis: [
          'Llega por Boti, donde el vecino ya habla con la Ciudad.',
          'Funciona sin cuenta para lo básico: el perfil es opcional.',
          'Una sola identidad geográfica: la dirección significa lo mismo en todos lados.'
        ]
      },
      gcba: {
        who: 'el área del GCBA que financia y decide',
        tareas: [
          'Cumplir metas de gestión y poder mostrar resultados.',
          'Atender el volumen de consultas y reclamos con el equipo que tiene.',
          'Coordinar áreas que no se hablan entre sí.',
          'Justificar cada peso del presupuesto.'
        ],
        frust: [
          'Cada área mantiene su propio mapa y su propia versión de la verdad.',
          'No hay una vista única de dónde se concentran los problemas.',
          'El vecino llama al 147 por cosas que podría autogestionar.',
          'Cada iniciativa nueva reconstruye la capa geográfica desde cero.'
        ],
        benef: [
          'Ver en un tablero dónde se concentran los reclamos.',
          'Dejar de pagar cuatro veces el mismo mapa.',
          'Bajar el volumen de consultas evitables.',
          'Poder mostrar el impacto con números.'
        ],
        pv: [
          'La vista de gestión: un tablero geográfico de reclamos y demanda.',
          'Una capa reutilizable que las demás iniciativas consumen en vez de reconstruir.'
        ],
        alivio: [
          'Una sola fuente geográfica: se termina la discusión sobre qué mapa vale.',
          'Costos evitados medibles: cada área que migra libera presupuesto.',
          'Menos consultas al 147 sobre lo que el Mapa ya resuelve.'
        ],
        satis: [
          'La capa la consumen Boti y DisfrutemosBA: el resultado se ve en productos que ya existen.',
          'El Mapa como identidad de la Ciudad, no como una app más.',
          'Datos para decidir dónde intervenir primero.'
        ]
      }
    }
  };

  /* 'Opción B · Plataforma multilateral' (+ ' (B2G)' when the option has a tag). */
  data.titleOf = function (id) {
    var o = data.options[id];
    return 'Opción ' + id.toUpperCase() + ' · ' + o.name + (o.tag ? ' (' + o.tag + ')' : '');
  };

  return data;
});
