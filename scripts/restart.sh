cd ~/resistbotca
source ../python/bin/activate
#export PYTHONUNBUFFERED=1
#kill $(ps -x | grep thesource\.wsgi| awk '{print $1}') ; nohup gunicorn -w 2 thesource.wsgi -R --env PYTHONUNBUFFERED=1 -b 127.0.0.1:8001 >> scripts/nohup.out &
kill $(cat scripts/gunicorn.pid) ; gunicorn -w 3 -t 300 resistbot.wsgi -b 127.0.0.1:8001 -p scripts/gunicorn.pid -D

