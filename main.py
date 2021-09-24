from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from grade_mention import get_grade, store_grade, load_grade, semester_dict_change, send_qq_mail
from config import username, password, mail_config

GRADE_FILE_PATH = 'grade.json'

def mention():
    logger.info('get scores')
    oldsems = load_grade(GRADE_FILE_PATH)
    overview, newsems = get_grade(username, password)
    change = semester_dict_change(oldsems, newsems)
    if change:
        title = '新出{:d}门成绩\n'.format(len(change))
        msg = '新成绩：\n' + '\n'.join(
            '{}  成绩：{} 绩点：{}'.format(score.courseNameCh, score.score, score.gp)
            for score in change)
        msg += '\n\n目前已获学分：{:.1f}，总GPA：{:.2f}，加权平均分：{:.2f}'.format(
            overview['passedCredits'], overview['gpa'], overview['weightedScore'])
        send_qq_mail(title=title, message=msg, **mail_config)
        store_grade(allsems=newsems, filename=GRADE_FILE_PATH)


sched = BlockingScheduler(standalone=True)
sched.add_job(mention, 'cron', minute='0,10,20,30,40,50')
try:
    logger.info('Scheduler start')
    sched.start()
except KeyboardInterrupt:
    exit()
