# logs-everymundo-microservice (Hiring process)
El siguiente código fuente forma parte de la evaluación técnica del proceso de reclutamiento para optar por el puesto de Backend Developer. La solución es un Microservicio que expone un conjunto de Endpoints que dán solución a las problemáticas planteadas. Además de los requisitos obligatorios, se implementaron un conjunto de funciones adicionales, que este servidor vió necesarias para entregar una solución más completa y flexible.

Para dar cumpplimiento a los requisitos solicitados se utilizaron las siguientes tecnologías:
- Python 3.8
- Flask 2.0
- Serverless
- AWS Lambda
- AWS S3

# Install instructions
Para poder desplegar la solución en un entorno sin servidor es necesario tener instalado en la computadora donde se realizará el despliegue las siguientes herramientas:
- NodeJS
- Python 3.8
- Git

Una vez que nos aseguramos que contamos con las herramientas necesarias, debemos seguir los siguientes pasos:

1. Descargar el repositorio hacia un directorio dentro de la computadora donde realizará el desarrollo
2. Colocarse en la carpeta donde se descargó el repositorio y ejecutar:
```bash
npm install
```
Este comando instalará las dependencias de NodeJs que encuentre dentro del fichero package.json, las cuales son necesarias para interactuar con el framework serverless.

3. Si usted no cuenta con el framework serverless instalado en su computadora, debe ingresar el siguiente comando para realizar el proceso de instalación.

```bash
npm install -g serverless
```

4. Si usted no cuenta con un perfil de usuario o credenciales (Clave/Valor) instaladas en su computadora debe escribir el siguiente comando para poder generarlas:
```bash
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```
Una vez completados estos pasos, ya estamos en disposición de manipular el archivo serverless.yaml, con lo cual vamos a realizar los ajustes finales antes de proceder a realizar el "deploy" del servicio a AWS Lambda.


# Execute unit test
