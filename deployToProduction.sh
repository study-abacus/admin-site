COMMAND='cd servers/admin-site && \
source env/bin/activate && \
ps aux | grep student_form | awk {'print $2'} | kill -15 && \
gunicorn student_form.wsgi -b 127.0.0.1:8001 -w 3 --daemon'

ssh studyabacus@srv1.studyabacus.com $COMMAND
