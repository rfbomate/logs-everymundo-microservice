from flask import jsonify
import boto3
import os


def statsLogsByFileService(request):
    if('file' not in request.files):
        return jsonify({'message': "No file item founded"}), 400

    fileUploaded = request.files['file']

    if(fileUploaded.filename == ''):
        return jsonify({'message': "Not selected file"}), 400

    if(not _isValidExtension(fileUploaded.filename)):
        return jsonify({'message': "Extension not allowed"}), 400

    # save temporal file
    s3 = boto3.client(
        "s3", aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

    try:
        s3.upload_fileobj(
            fileUploaded,
            os.environ['BUCKET_NAME'],
            fileUploaded.filename,
            ExtraArgs={
                "ContentType": fileUploaded.content_type
            }
        )

        # read temporal file
        textReaded = ''
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

        s3 = session.resource('s3')
        fileObjectRead = s3.Bucket(os.environ['BUCKET_NAME']).Object(
            fileUploaded.filename)  # read a specific file
        if(not fileObjectRead):
            return jsonify({"message": "An error has occured reading the file"}), 400

        body = fileObjectRead.get()['Body'].read().decode('utf-8')
        textReaded = str(body)

        # delete temporal file
        fileObjectRead.delete()

        # processing file
        lines = textReaded.split("\n")
        countErrors = 0
        countSuccess = 0
        isValidFile = True
        counterLineError = 0
        for line in lines:
            columns = line.split("-")  # 0-timestamp 1-application 2-category
            if(len(columns) != 3):
                isValidFile = False
                break

            if(len(columns[2].split(":")) < 1):
                isValidFile = False
                break

            category = columns[2].split(":")[0]

            if('ERROR' in category.upper()):
                countErrors += 1
            if('SUCCESS' in category.upper()):
                countSuccess += 1

            counterLineError += 1

        return jsonify({'ErrorCount': countErrors, 'SuccessCount': countSuccess, 'Total': len(lines)}) if isValidFile else jsonify({message: "The file has errors. Error near line "+str(counterLineError+1)}), 400

    except Exception as e:
        return jsonify({"message": "An error has occurred. Retry later"}), 400


def _isValidExtension(pFilename):
    ALLOWED_EXTENSIONS = {'txt'}
    return '.' in pFilename and \
           pFilename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
