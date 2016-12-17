#!/usr/bin/env python
import server

server.db.create_all()
device = server.Device(123456789, "stotv", "First Last", "Address 1", "Address 2, City 12345")
server.db.session.add(device)
server.db.session.add(server.Data(123456789, 1, "12-16-1016 16:00:00", "41.310824", "-67.148437", 3))
server.db.session.add(server.Data(123456789, 2, "12-16-1016 17:00:00", "41.710824", "-65.25437", 3))
server.db.session.add(server.Data(123456789, 2, "12-16-1016 18:00:00", "41.810824", "-64.320437", 3))
server.db.session.commit()