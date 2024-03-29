create procedure deleteClient 
	@id int
AS
BEGIN
	delete from clients
	where id_client=@id
END;


create procedure deleteBus
	@id int
AS
BEGIN
	delete from buses
	where id_bus=@id
END;


create procedure deleteCity
	@id int
AS
BEGIN
	delete from cities
	where id_city=@id
END

create procedure deleteNonAthUser
	@id int
AS
BEGIN
	delete from non_autorized_users
	where id_user=@id
END


create procedure deleteOrder
	@id int
AS
BEGIN
	delete from orders
	where id_order=@id
END


create procedure deleteTicket
	@id int
AS
BEGIN
	delete from tickets
	where id_ticket=@id
END


create procedure deleteTimetable
	@id int
AS
BEGIN
	delete from timetable
	where id_journey=@id
END

--DROP PROCEDURE IF EXISTS get_income_per_day

create procedure get_income_per_day	
as
begin
	
	DECLARE @time_now datetime,
        @time_start_day datetime,
        @time_finish_day datetime;

	SET @time_now = GETDATE();
	SET @time_start_day = CONVERT(datetime, CONVERT(date, @time_now));
	SET @time_finish_day = DATEADD(second, -1, DATEADD(day, 1, CONVERT(datetime, CONVERT(date, @time_now))));
	SELECT @time_now AS time_now, @time_start_day AS time_start_day, @time_finish_day AS time_finish_day;

	select Sum(orders.cost) as income_per_day  from orders where date_buying between @time_start_day and @time_finish_day and orders.whether_paid=1
end

exec get_income_per_day


--DROP PROCEDURE IF EXISTS get_income_per_month


CREATE PROCEDURE get_income_per_month
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_month datetime,
            @time_finish_month datetime;

    SET @time_now = GETDATE();
    SET @time_start_month = DATEADD(month, DATEDIFF(month, 0, @time_now), 0); 
    SET @time_finish_month = DATEADD(second, -1, DATEADD(month, 1, @time_start_month)); 

    SELECT @time_now AS time_now, @time_start_month AS time_start_month, @time_finish_month AS time_finish_month;

    SELECT SUM(orders.cost) as income_per_month  
    FROM orders 
    WHERE date_buying BETWEEN @time_start_month AND @time_finish_month 
    AND orders.whether_paid = 1;
END;


exec get_income_per_month

--DROP PROCEDURE IF EXISTS get_income_per_year

CREATE PROCEDURE get_income_per_year
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_year datetime,
            @time_finish_year datetime;

    SET @time_now = GETDATE();
    SET @time_start_year = DATEFROMPARTS(YEAR(@time_now), 1, 1); -- Початок поточного року
    SET @time_finish_year = DATEADD(second, -1, DATEADD(year, 1, @time_start_year)); -- Кінець поточного року

    SELECT @time_now AS time_now, @time_start_year AS time_start_year, @time_finish_year AS time_finish_year;

    SELECT SUM(orders.cost) as income_per_year  
    FROM orders 
    WHERE date_buying BETWEEN @time_start_year AND @time_finish_year 
    AND orders.whether_paid = 1;
END;

exec get_income_per_year


--DROP PROCEDURE IF EXISTS get_all_tickets_per_day

CREATE PROCEDURE get_all_tickets_per_day 
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_day datetime,
            @time_finish_day datetime;

    SET @time_now = GETDATE();
    SET @time_start_day = CONVERT(datetime, CONVERT(date, @time_now));
    SET @time_finish_day = DATEADD(second, -1, DATEADD(day, 1, CONVERT(datetime, CONVERT(date, @time_now))));

    SELECT @time_now AS time_now, @time_start_day AS time_start_day, @time_finish_day AS time_finish_day;

    SELECT COUNT(id_ticket) as total_tickets 
    FROM tickets 
    WHERE order_id IS NOT NULL
    AND order_id <> ''; 
END;

exec get_all_tickets_per_day

--DROP PROCEDURE IF EXISTS get_all_tickets_per_month;

CREATE PROCEDURE get_all_tickets_per_month 
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_month datetime,
            @time_finish_month datetime;

    SET @time_now = GETDATE();
    SET @time_start_month = DATEFROMPARTS(YEAR(@time_now), MONTH(@time_now), 1); -- Початок поточного місяця
    SET @time_finish_month = DATEADD(second, -1, DATEADD(month, 1, @time_start_month)); -- Кінець поточного місяця

    SELECT @time_now AS time_now, @time_start_month AS time_start_month, @time_finish_month AS time_finish_month;

    SELECT COUNT(id_ticket) as total_tickets 
    FROM tickets 
    WHERE order_id IS NOT NULL
    AND order_id <> ''
    AND date_buying BETWEEN @time_start_month AND @time_finish_month;
END;

exec get_all_tickets_per_month


--DROP PROCEDURE IF EXISTS get_all_tickets_per_year;

CREATE PROCEDURE get_all_tickets_per_year 
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_year datetime,
            @time_finish_year datetime;

    SET @time_now = GETDATE();
    SET @time_start_year = DATEFROMPARTS(YEAR(@time_now), 1, 1); -- Початок поточного року
    SET @time_finish_year = DATEADD(second, -1, DATEADD(year, 1, @time_start_year)); -- Кінець поточного року

    SELECT @time_now AS time_now, @time_start_year AS time_start_year, @time_finish_year AS time_finish_year;

    SELECT COUNT(id_ticket) as total_tickets 
    FROM tickets 
    WHERE order_id IS NOT NULL
    AND order_id <> ''
    AND date_buying BETWEEN @time_start_year AND @time_finish_year;
END;

exec get_all_tickets_per_year


--DROP PROCEDURE IF EXISTS delete_all_non_active_journeys;

CREATE PROCEDURE get_all_tickets_per_year 
AS
BEGIN
    DECLARE @time_now datetime,
            @time_start_year datetime,
            @time_finish_year datetime;

    SET @time_now = GETDATE();
    SET @time_start_year = DATEFROMPARTS(YEAR(@time_now), 1, 1); -- Початок поточного року
    SET @time_finish_year = DATEADD(second, -1, DATEADD(year, 1, @time_start_year)); -- Кінець поточного року

    SELECT @time_now AS time_now, @time_start_year AS time_start_year, @time_finish_year AS time_finish_year;

    SELECT COUNT(id_ticket) as total_tickets 
    FROM tickets 
    WHERE order_id IS NOT NULL
    AND order_id <> ''
    AND date_buying BETWEEN @time_start_year AND @time_finish_year;
END;

exec get_all_tickets_per_year

