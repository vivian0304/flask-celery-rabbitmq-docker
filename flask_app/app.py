try:
    from flask import Flask, request
    import boto3
    from celery import Celery
    import pymongo
    
except Exception as e:
    print("Error  :{} ".format(e))

app = Flask(__name__)


simple_app = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='mongodb://mongodb_container:27017/mydb')

# 일을 시키는 함수
@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    first_num = request.args.get('first_num')
    second_num = request.args.get('second_num')
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': first_num, 'y': second_num})
    app.logger.info(r.backend)
    return r.id

# 일이 완료되었는지 상태를 체크하는 함수
@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)

# 결과값을 가져오는 함수
@app.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    # db에 url 저장
    return "Result of the Task " + str(result)
    # 샐러리에서 form-data 형식으로 넘겨준 값을 이용해 db와 s3에 저장

