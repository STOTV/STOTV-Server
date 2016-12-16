#!/usr/bin/env python
import server

server.db.create_all();
device=server.Device(123456789012345,"Test1","Donald Trump","123 Where st","New York City, New York 69483")
server.db.session.add(device)
data=server.Data(123456789012345,1,"12-16-1016 16:00:00","41.310824","-67.148437",3)
server.db.session.add(data)
server.db.session.commit()
