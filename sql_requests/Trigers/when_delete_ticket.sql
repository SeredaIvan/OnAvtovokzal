USE [avtovokzal]
GO

IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'when_delete_ticket')
BEGIN
    DROP TRIGGER when_delete_ticket;
END
GO


create TRIGGER when_delete_ticket
ON tickets
INSTEAD OF DELETE
AS
BEGIN
    PRINT 'Trigger fired';
    DECLARE @id_ticket INT,@id_order int;
    SELECT @id_ticket = id_ticket FROM deleted;
	SELECT @id_order = order_id FROM deleted;
    
    DELETE FROM tickets 
    WHERE id_ticket = @id_ticket;
	exec delete_order @id_order
END;
GO


IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'delete_order')
BEGIN
    DROP PROCEDURE delete_order;
END
GO
create procedure delete_order
@id_order int
as
begin
	DELETE FROM orders
    WHERE id_order = @id_order;
end
