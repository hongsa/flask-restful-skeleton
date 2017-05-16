# flask restful skeleton

setting.py에서 db 설정 맞게 바꾸기


### run server
python manage.py runserver

### db init & migrate
python manage.py db init
python manage.py db migrate
python manage.py db upgrade


### db 관련 이슈
- migrate 할 때 alembic에서 타입 변경 detect 못할 때
compare_type=True 추가함 
```
context.configure(connection=connection,
                      target_metadata=target_metadata,
                      compare_type=True,
```                   
                      
