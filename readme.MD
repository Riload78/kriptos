
# Gestión de ingresos gastos
Aplicación web para simular registros de movimientos de criptomonedas con estructura de SPA con python (flask) y js.

# Instalación

## Creación del entorno virtual
Para crear un entorno virtual en Python utilizando venv, sigue los siguientes pasos:

Abre una terminal o línea de comandos en tu sistema operativo.

Navega al directorio donde desees crear el entorno virtual. Puedes utilizar el comando cd en la terminal para cambiar de directorio.

Ejecuta el comando python3 -m venv nombre_del_entorno (en Windows, el comando es python -m venv nombre_del_entorno). Reemplaza nombre_del_entorno con el nombre que desees para tu entorno virtual.

Por ejemplo, si deseas crear un entorno virtual llamado "myenv", en macOS o Linux, el comando sería:

```
python3 -m venv myenv
```
En Windows, el comando sería:

```
python -m venv myenv
```

Una vez que ejecutes el comando, se creará el entorno virtual en el directorio actual. Deberías ver una nueva carpeta llamada "myenv" (o el nombre que hayas elegido) que contiene los archivos y directorios necesarios para el entorno virtual.

Activa el entorno virtual. En macOS y Linux, puedes hacerlo con el siguiente comando:

```
. myenv/bin/activate
```

En Windows, el comando sería:

```
myenv\Scripts\activate
```

Una vez activado el entorno virtual, verás que el nombre del entorno aparece entre paréntesis en la terminal, lo que indica que estás trabajando dentro del entorno virtual.

Ahora puedes instalar paquetes y desarrollar tu proyecto en este entorno virtual sin afectar a otros proyectos o al sistema en general.

## Configuración de la APP
Copia el fichero `.env_template` y renombrarlo como `.env` e indicar los datos requeridos:
    - 1. FLASK_DEBUG a True o False (en producción False)
    - 2. Deja FLASK_APP como está
    - 3. FLASK_SECRET_KEY: Introducir la secret key. En principio no es necesario ya que no se requiere wtForms
    - 4. PATH_SQLITE : introducir la ruta de la BBDD. Valor por defecto: ```data/cripto.db```
    - 5. API_IO : ir a ```https://www.coinapi.io/```y crear una cuenta para obtener la api key he introducirla en el campo API_IO

Instala las dependencias ejecutando 
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










