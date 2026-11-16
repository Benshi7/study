---------------
-- Consultas --
---------------
-- Crear SQL que responda los siguientes pedidos:

-- Listar los pacientes que se atendieron en el servicio de Pediatría.
select dp.Nombre as Paciente, ds.Nombre as Servicio
from DESA_PACIENTE dp
inner join DESA_HISTORIA_CLINICA dhc on dp.Id_Paciente = dhc.Id_Paciente
INNER JOIN DESA_SERVICIO ds ON ds.Id_Servicio = dhc.Id_Servicio 
where ds.Nombre = 'Pediatría';

-- Listar los teléfonos de los Pacientes que pertenezcan a OSDE.
select dp.Nombre as Paciente, dpr.Nombre as Prepaga, dpt.Telefono 
from DESA_PACIENTE dp
inner join DESA_PREPAGA dpr on dpr.Id_Prepaga =dp.Id_Prepaga  
INNER join DESA_PACIENTE_TELEFONO dpt on dp.Id_Paciente = dpt.Id_Paciente 
where dpr.Nombre = 'OSDE';

-- Informar la cantidad de Habitaciones de la Torre 1.
select count(*) Cantidad_Habitaciones
from DESA_HABITACION dh 
where dh.id_torre = 1;

-- Listar el nombre de los pacientes internados con Habitaciones con Ventana.
select dp.Nombre --, dh.Numero, dh.Id_Torre  
from DESA_PACIENTE dp 
inner JOIN DESA_OCUPA do on do.Id_Paciente = dp.Id_Paciente 
inner join DESA_HABITACION dh on dh.Id_Habitacion = do.Id_Habitacion 
where dh.Ventana = 1;

-- Listar los médicos que no son jefes y su especialidad.
select dp.Nombre , de.Nombre as Especialidad
from DESA_PROFESIONAL dp 
inner join DESA_ESPECIALIDAD de on de.Id_Especialidad = dp.Id_Especialidad 
where dp.Id_Jefe is not null

-- Listar los médicos que son supervisados por un médico determinado.
select dp2.Nombre as Medico, dp.Nombre as Jefe
from DESA_PROFESIONAL dp 
inner join DESA_PROFESIONAL dp2 on dp.Id_Profesional = dp2.Id_Jefe 
