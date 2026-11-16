// =====================================================================
// 01_power_query.m — Consultas de Power Query para el dashboard
// Cómo usarlo: Inicio > Transformar datos > Nueva consulta > Consulta en blanco >
// Editor avanzado, y pegar cada bloque con el nombre indicado.
// Los CSV usan punto decimal y UTF-8: por eso todo se tipa con la cultura "en-US".
// =====================================================================


// ---------- Parámetro: RutaDatos (consulta en blanco, nombre: RutaDatos) ----------
// Carpeta con polizas.csv, siniestros.csv y parametros.csv (la salida de build_mart.py),
// terminada en barra. Ejemplo:  C:\tp\export\
"C:\tp\export\" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]


// ---------- Consulta: polizas ----------
let
    Origen = Csv.Document(File.Contents(RutaDatos & "polizas.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    // franja_bm ('050') y franja_vehage ('00') van como TEXTO: si no, Power BI les saca los ceros.
    Tipos = Table.TransformColumnTypes(Encabezados, {
        {"idpol", Int64.Type}, {"exposure", type number}, {"siniestros", Int64.Type},
        {"monto", type number}, {"monto_topeado", type number}, {"siniestros_grandes", Int64.Type},
        {"drivage", Int64.Type}, {"franja_edad", type text},
        {"bonusmalus", Int64.Type}, {"franja_bm", type text},
        {"vehage", Int64.Type}, {"franja_vehage", type text},
        {"vehpower", Int64.Type}, {"vehbrand", type text}, {"vehgas", type text},
        {"area", type text}, {"density", Int64.Type},
        {"region", type text}, {"region_2016", type text}, {"claimnb_declarado", Int64.Type},
        {"flag_lote_idpol_bajo", Int64.Type}, {"flag_exposure_recortada", Int64.Type},
        {"flag_claimnb_corregido", Int64.Type}
    }, "en-US"),
    // B1, B2, B10... se ordenarían como texto (B1, B10, B11, B2). Columna numérica para ordenar.
    OrdenMarca = Table.AddColumn(Tipos, "vehbrand_orden",
                    each Number.FromText(Text.Middle([vehbrand], 1)), Int64.Type)
in
    OrdenMarca


// ---------- Consulta: siniestros ----------
let
    Origen = Csv.Document(File.Contents(RutaDatos & "siniestros.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {
        {"id_siniestro", Int64.Type}, {"idpol", Int64.Type},
        {"monto", type number}, {"monto_topeado", type number}, {"es_grande", Int64.Type}
    }, "en-US")
in
    Tipos


// ---------- Consulta: parametros ----------
let
    Origen = Csv.Document(File.Contents(RutaDatos & "parametros.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"nombre", type text}, {"valor", type number}}, "en-US")
in
    Tipos


// ---------- Consultas auxiliares (también están en export/, las genera src/etl.py) ----------
// Mismo patrón para cada una; cambian el archivo y los tipos.

// dim_region  (dim_region.csv)
let
    Origen = Csv.Document(File.Contents(RutaDatos & "dim_region.csv"), [Delimiter = ",", Encoding = 65001]),
    Enc = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Enc, {{"region_2016", type text}, {"latitud", type number}, {"longitud", type number}}, "en-US")
in
    Tipos

// pareto  (pareto.csv)
let
    Origen = Csv.Document(File.Contents(RutaDatos & "pareto.csv"), [Delimiter = ",", Encoding = 65001]),
    Enc = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Enc, {{"pct_siniestros", type number}, {"pct_monto_acum", type number}}, "en-US")
in
    Tipos

// calidad_hallazgos  (calidad_hallazgos.csv)
let
    Origen = Csv.Document(File.Contents(RutaDatos & "calidad_hallazgos.csv"), [Delimiter = ",", Encoding = 65001]),
    Enc = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Enc, {{"codigo", type text}, {"problema", type text}, {"accion", type text}, {"registros", Int64.Type}}, "en-US")
in
    Tipos

// calidad_antes_despues  (calidad_antes_despues.csv)
let
    Origen = Csv.Document(File.Contents(RutaDatos & "calidad_antes_despues.csv"), [Delimiter = ",", Encoding = 65001]),
    Enc = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Enc, {{"version", type text}, {"polizas", Int64.Type}, {"exposicion", type number},
                                             {"siniestros", Int64.Type}, {"frecuencia", type number}, {"prima_pura", type number}}, "en-US")
in
    Tipos
