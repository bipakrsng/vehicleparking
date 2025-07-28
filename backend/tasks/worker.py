from celery import Celery,Task
#creating celery Instance
def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args:object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args,**kwargs)
            
    celery_app = Celery(app.name, task_cls = FlaskTask)
    celery_app.config_from_object("celeryconfig") #integrating the celery config 
    return celery_app
