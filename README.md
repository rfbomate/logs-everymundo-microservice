# logs-everymundo-microservice (Hiring process)
The following source code is part of the technical evaluation of the recruitment process to apply for the position of Backend Developer. The solution is a Microservice that exposes a set of Endpoints that provide a solution to the problems raised. In addition to the mandatory requirements, a set of additional features were implemented, which this server found necessary to deliver a more complete and flexible solution.

To comply with the requested requirements, the following technologies were used:

- Python 3.8
- Flask 2.0
- Serverless
- AWS Lambda
- AWS S3

# Install instructions

To be able to deploy the solution in a serverless environment, it is necessary to have the following tools installed on the computer where the deployment will take place:

- NodeJS
- Python 3.8
- Git

Once we make sure that we have the necessary tools, we must follow the following steps:

1. Download the repository to a directory inside the computer where you will do the development
2. Go to the folder where the repository was downloaded and run:

```bash
npm install
```

This command will install the NodeJs dependencies it finds inside the package.json file, which are necessary to interact with the serverless framework.

3. If you do not have the serverless framework installed on your computer, you must enter the following command to complete the installation process.

```bash
npm install -g serverless
```

4. If you do not have a user profile or credentials (Key/Value) installed on your computer, you must type the following command to generate them:

```bash
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Once these steps are completed, we are ready to manipulate the serverless.yaml file, with which we are going to make the final adjustments before proceeding to "deploy" the service to AWS Lambda.

# Edit file serverless.yaml

Below we will describe the sections of the file that should be edited to achieve a better degree of customization when deploying to AWS.

- service: this section will allow us to put the base name of our Lambda.
- plugins: in this section we are going to define all the plugins that the serverless framework provides us to complete the development correctly.
- custom: the section allows us to configure certain characteristics such as: the Web Server Gateway Interface to manipulate the Server App options, the dosposition or not of the packaging of the requirements, the dockerization of the solution before deploying it (in my case, the platform was developed on a MAC, if the deployment will be done on a machine with a Linux family operating system (Ubuntu for example), the "dockerizePiP" section should have a value of "non-linux"), the apigwBinary allows us to configure the access door to the Lambda for uploading files, as well as configuring the types and extensions allowed.
- Within the "providers" section, the global configurations of the deployment are defined, which are: the destination of the deployment (in our case aws), the compiler or interpreter (as the case may be) that will execute our code, the stage or type where it will be deployed, the region within AWS where the Lambda will be hosted, and the environment variables that will be used within the different sections of the Lambda. It is very important to point out that in the serverless.yaml file that will be downloaded with the project, these variables have dummy values, please do not change the name of the variables, just replace the values with others that make sense for your account.
- functions: here the destination where the requests that arrive through the API Gateway will go is defined.

# Permissions policy
It is important to point out that once the solution is deployed, the Lambda can correctly interact with the resources stored in AWS S3, it is necessary to give the Lambda all the permissions so that it can interact with them. In the Roles section, which is found in the security administration, you must find the role associated with the Lambda and attach a Full Access policy to the S3 resources.

# Execute unit test
The development has 5 unit test files, within which a total of 37 unit tests were implemented, trying to carry out a very complete test of each of the functions that were implemented in this development.

The unit tests were implemented using the Pytest tool.

To run the unit test files, you must open a console at the root of the project and write the following commands, according to the set of tests you want to run.

```bash
pytest -v tests/testNotifyService.py 
```

```bash
pytest -v tests/testGetTokenService.py   
```
```bash
pytest -v tests/testFilterLogService.py     
```
It is important to point out that the last test of this set is based on proving that the process, with all input parameters correctly entered, runs ideally. Within the method, a duplicity validation is performed, which is why if only that case is executed without changing the input parameters, it will fail, which is why before running it, the input parameters in the request must be changed.
```bash
pytest -v tests/testCreateSubscriptionService.py
```
```bash
pytest -v tests/testCreateSingleLog.py
```

# Postman request set
At the root of the project, you will find an exported postman file where you can test all the developed Endpoints, which are available in real time. Within the unit test sets, there is the base URL of the Lambda through its API Gateway, which can be used without any limitation even without deploying and putting this source code into production.

# Functional description
In the root of the project, a .PDF file is left with the functional description of each functionality developed in the exercise.

