---------------
-- Consultas --
---------------


-- Listar los pacientes que se atendieron en el servicio de Pediatría.
select dp.Nombre as Paciente, ds.Nombre as Servicio
from Vista_Paciente dp
inner join Vista_Historia_Clinica dhc on dp.Id_Paciente = dhc.Id_Paciente
INNER JOIN Vista_Servicio ds ON ds.Id_Servicio = dhc.Id_Servicio 
where ds.Nombre = 'Pediatría';

-- Listar los teléfonos de los Pacientes que pertenezcan a OSDE.
select dp.Nombre as Paciente, dpr.Nombre as Prepaga, dpt.Telefono 
from Vista_Paciente dp
inner join Vista_Prepaga dpr on dpr.Id_Prepaga =dp.Id_Prepaga  
INNER join Vista_Paciente_Telefono dpt on dp.Id_Paciente = dpt.Id_Paciente 
where dpr.Nombre = 'OSDE';

-- Informar la cantidad de Habitaciones de la Torre 1.
select count(*) Cantidad_Habitaciones
from Vista_Habitacion dh 
where dh.id_torre = 1;

-- Listar el nombre de los pacientes internados con Habitaciones con Ventana.
select dp.Nombre --, dh.Numero, dh.Id_Torre  
from Vista_Paciente dp 
inner JOIN Vista_Ocupa do on do.Id_Paciente = dp.Id_Paciente 
inner join Vista_Habitacion dh on dh.Id_Habitacion = do.Id_Habitacion 
where dh.Ventana = 1;

-- Listar los médicos que no son jefes y su especialidad.
select dp.Nombre , de.Nombre as Especialidad
from Vista_Profesional dp 
inner join Vista_Especialidad de on de.Id_Especialidad = dp.Id_Especialidad 
where not exists (select 1 from Vista_Profesional dp2 where dp2.Id_Jefe = dp.Id_Profesional);

-- Listar los médicos que son supervisados por un médico determinado.
select dp2.Nombre as Medico, dp.Nombre as Jefe
from Vista_Profesional dp 
inner join Vista_Profesional dp2 on dp.Id_Profesional = dp2.Id_Jefe
where dp.Nombre = 'Alan Guevara' 
