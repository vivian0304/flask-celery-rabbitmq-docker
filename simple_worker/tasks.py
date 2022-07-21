import time
from celery import Celery
from celery.utils.log import get_task_logger
import ai

logger = get_task_logger(__name__)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='mongodb://mongodb_container:27017/mydb')


@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    
    # 다른 함수에서 동영상을 저장하는 과정 진행 후 url return 시켜주면
    # 그 url을 받아서 celery return 값으로 넣어주는 과정 진행해보기
    return ai.fasdf()
    # return 값을 db에 저장
