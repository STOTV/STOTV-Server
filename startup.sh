uwsgi -s /tmp/uwsgi.sock --manage-scripname --mount /=server:app --http :9090
