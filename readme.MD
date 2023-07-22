
# Gestión de ingresos gastos
Aplicación web para simular registros de movimientos de criptomonedas con estructura de SPA con python (flask) y js.

# Instalación
1. Copia el fichero `.env_template` e informa FLASK_DEBUG a True o False (en producción False)
2. Deja FLASK_APP como está
3. FLASK_SECRET_KEY: Introducir la secret key. En principio no es necesario ya que no se requiere wtForms
4. PATH_SQLITE : introducir la ruta de la BBDD. Valor por defecto: ```data/cripto.db```
5. API_IO : ir a ```https://www.coinapi.io/```y crear una cuenta para obtener la api key he introducirla en el campo API_IO
6. Instala las dependencias ejecutando 
```
pip install -r requirements.txt
```

# Creación de la BBDD 
La BBDD se crea automáticamnete la primera vez que se ejecuta la aplicación. Cabe la posibilidad de ejecutar la creación de la BBDD de forma manual. Para eso, en la consola, ir a la ruta ``` /data  ``` y ejecutar el archivo createdb.py:

```python createdb.py```

# Ejecución
Ejecuta en el directorio de la aplicación
```
flask run
```










