USE [avtovokzal]
GO
drop trigger[when_delete_bus]

go
create TRIGGER when_delete_bus
ON buses
INSTEAD OF DELETE
AS
BEGIN
    PRINT 'Trigger fired';
    DECLARE @id_bus INT;
    SELECT @id_bus = id_bus FROM deleted;
    EXEC drop_FK_timetable_buses @id_bus;
	delete from buses 
	where id_bus=@id_bus
END;

--0->>

create PROCEDURE drop_FK_timetable_buses 
    @id_bus INT
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY
        UPDATE timetable 
        SET bus_id = NULL
        WHERE bus_id = @id_bus; 
        
        
		print ('EXEC delete_null_journey start')
		EXEC delete_null_journey;
        COMMIT TRANSACTION;
    END TRY
	
    BEGIN CATCH
		print ('rollback')
        ROLLBACK TRANSACTION;
		
    END CATCH;
END;

--0->>

create PROCEDURE delete_null_journey
AS
BEGIN
	
    DELETE FROM timetable
    WHERE bus_id IS NULL;
	print ('EXEC delete_null_journey end')
END;

