1 SELECT LastName ASC FROM employees



 2 SELECT albums.Title, tracks.name,tracks.Milliseconds FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
WHERE albums.Title LIKE 'Big Ones'  
ORDER by tracks.Name DESC, tracks.Milliseconds DES



3 SELECT tracks.UnitPrice,tracks.name FROM tracks
ORDER by tracks.Name DESC, tracks.UnitPrice LIMIT 10


4 SELECT t.UnitPrice,t.name, a.Title, g.Name FROM albums a 
JOIN tracks t ON a.AlbumId = t.AlbumId 
JOIN genres g ON t.GenreId = g.GenreId 
WHERE t.name AND t.UnitPrice = 0.99


5 SELECT at.name, t.name, t.Milliseconds, a.Title, g.Name FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId 
JOIN genres g ON t.GenreId = g.GenreId 
JOIN artists at ON a.ArtistId = at.ArtistId 
WHERE t.name ORDER BY t.Milliseconds ASC LIMIT 20 

6 
SELECT emp.LastName AS empleado, jefe.LastName AS jefe, COUNT(*)  FROM employees emp
JOIN employees jefe ON emp.ReportsTo = jefe.EmployeeId
JOIN customers cus ON emp.EmployeeId = cus.SupportRepId
GROUP BY emp.EmployeeId
ORDER by jefe ASC

7
SELECT 
    emp.FirstName AS Nombre_Empleado, 
    emp.LastName AS Apellido_Empleado,
    cus.FirstName AS Nombre_Cliente, 
    cus.LastName AS Apellido_Cliente
FROM employees emp
JOIN customers cus ON emp.EmployeeId = cus.SupportRepId
ORDER BY emp.LastName ASC, cus.LastName ASC


8 

SELECT 
    cus.FirstName AS Nombre_Cliente, 
    cus.LastName AS Apellido_Cliente,
	cus.Address AS direccion_Cliente,
	inv.InvoiceDate AS fecha_facturacion
FROM customers cus	
JOIN invoices inv ON cus.CustomerId = inv.CustomerId

9

SELECT 
    gen.name, sum(tra.TrackId) AS cuan_canciones
FROM tracks tra	
JOIN genres gen ON gen.GenreId = tra.GenreId
GROUP BY gen.GenreId
ORDER BY cuan_canciones


10

SELECT 
    c.FirstName AS Nombre_Cliente, 
    c.LastName AS Apellido_Cliente, 
    ar.Name AS Nombre_Artista
FROM customers c
JOIN invoices inv ON c.CustomerId = inv.CustomerId
JOIN invoice_items inv_itm ON inv.InvoiceId = inv_itm.InvoiceId
JOIN tracks tra ON inv_itm.TrackId = tra.TrackId
JOIN albums alb ON tra.AlbumId = alb.AlbumId
JOIN artists ar ON alb.ArtistId = ar.ArtistId
ORDER BY c.FirstName, c.LastName;

11

SELECT 
    c.FirstName AS Nombre_Cliente, 
    c.City AS Ciudad, 
    tra.Name AS Cancion, 
    gen.Name AS Genero
FROM customers c
JOIN invoices inv ON c.CustomerId = inv.CustomerId
JOIN invoice_items inv_itm ON inv.InvoiceId = inv_itm.InvoiceId
JOIN tracks tra ON inv_itm.TrackId = tra.TrackId
JOIN genres gen ON tra.GenreId = gen.GenreId;



12

SELECT *
FROM employees em
JOIN customers cu ON em.EmployeeId = cu.SupportRepId
JOIN invoices inv ON cu.CustomerId = inv.CustomerId
JOIN invoice_items inv_itm ON inv.InvoiceId = inv_itm.InvoiceId
JOIN tracks tra ON inv_itm.TrackId = tra.TrackId
JOIN albums al ON tra.AlbumId = al.AlbumId
JOIN artists ar ON al.ArtistId = ar.ArtistId
JOIN genres gen ON tra.GenreId = gen.GenreId
JOIN media_types med_tip ON tra.MediaTypeId = med_tip.MediaTypeId
JOIN playlist_track pt ON tra.TrackId = pt.TrackId
JOIN playlists p ON pt.PlaylistId = p.PlaylistId;
