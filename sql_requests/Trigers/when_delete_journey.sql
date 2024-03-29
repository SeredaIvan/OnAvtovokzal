USE [avtovokzal]
GO

IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'when_delete_journey')
BEGIN
    DROP TRIGGER when_delete_journey;
END
GO

CREATE TRIGGER when_delete_journey
ON timetable
INSTEAD OF DELETE
AS
BEGIN
    PRINT 'Trigger fired';
    DECLARE @id_journey INT;
    SELECT @id_journey = id_journey FROM deleted;
    EXEC drop_FK_tickets_timetable @id_journey;
    DELETE FROM timetable 
    WHERE id_journey = @id_journey;
END;
GO

IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'drop_FK_tickets_timetable')
BEGIN
    DROP PROCEDURE drop_FK_tickets_timetable;
END
GO

CREATE PROCEDURE drop_FK_tickets_timetable
    @id_journey INT
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY
        UPDATE tickets 
        SET journey_id = NULL
        WHERE journey_id = @id_journey; 
        
        PRINT 'EXEC delete_null_journey start';
        EXEC delete_null_tickets;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        PRINT 'Rollback';
        ROLLBACK TRANSACTION;
    END CATCH;
END;
GO


IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'delete_null_tickets')
BEGIN
    DROP PROCEDURE delete_null_tickets;
END
GO


CREATE PROCEDURE delete_null_tickets
AS
BEGIN
    DELETE FROM tickets
    WHERE journey_id IS NULL;
    PRINT 'EXEC delete_null_journey end';
END;
GO
