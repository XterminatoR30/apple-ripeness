#Karena website adalah folder dgn python extension
from website import create_app

app=create_app()
#Run webserver
#Debug= Tiap kali code python nya berubah, akan restart servernya otomatis

if __name__=='__main__':
    app.run(debug=True)